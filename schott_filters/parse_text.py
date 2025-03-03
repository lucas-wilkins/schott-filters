from file_data import file_data
import re
import numpy as np

class Empty:
    text = "E"

class LessThanFlag:
    text = "<"

class LessThanValue:
    text = "L"
    def __init__(self, value):
        self.value = value

class Value:
    text = "V"
    def __init__(self, value):
        self.value = value

class Wavelength:
    text = "W"
    def __init__(self, value):
        self.value = value


def parse_text(id, verbose=False, write=True):
    filename = f"data/datasheet-text/{id}.txt"

    with open(filename, 'r') as fid:
        lines = [line.strip() for line in fid.readlines()]

    start = None
    end = None
    for i, line in enumerate(lines):

        # Some of the "en" datasheets are in German

        if line.startswith("The internal") or line.startswith("Die Reintransmissionsgrade"):
            start = i

        # All pages have something like this, data not always on the last page
        if start is not None:
            if line.startswith("Status") or line.startswith("Stand"):
                end = i
                break

    if verbose:
        print()
        print(" "*(6-len(id)) + id, start, "-", end)

    # Assume for now that all of these have 5 columns

    n_offset = 13

    data_section = lines[start+n_offset:end]

    if verbose:
        print("     Before:", lines[start+n_offset-1])
        print("      First:", data_section[0])
        print("       Last:", data_section[-1])
        print("      After:", lines[end])

    # Now convert the data into values, assume that it is arranged in rows
    # How do we know if its a wavelength, or transmittance
    # different kinds of line:
    #   an integer, in a multiple of 5
    #   a float
    #   "<"
    #   "<" followed by a float
    #
    # As there are always the same wavelengths present, floats will always
    #  be preceded (and followed) by ints - but not the other way round
    #
    #

    tokens = []
    for line_no, line in enumerate(data_section):

        line = line.strip()

        if line == "" or line == "-":
            entry = Empty()


        elif line == "<":
            entry = LessThanFlag()

        else:

            try:
                int_value = int(line)

                if int_value % 5 == 0:
                    entry = Wavelength(int_value)
                else:
                    raise ValueError("int but not wavelength")

            except:

                if line.startswith("<"):
                    value_type = LessThanValue
                    line = line[1:].strip()

                else:
                    value_type = Value

                line = re.sub(r",", r".", line) # Turn from German decimal separator to English

                try:

                    float_value = float(line.lower())
                    entry = value_type(float_value)

                except:
                    print(f"{id}: Line {line_no+1} - Failed to parse '{line}'")

                    n = 5
                    low = max([0,line_no - n])
                    high = min([line_no+n, len(data_section)])
                    around = data_section[low:high]
                    nums = [i for i in range(len(data_section))][low:high]

                    for num, a_line in zip(nums, around):
                        print(f"   {num+1}: {a_line}")

        tokens.append(entry)

    # Now we do some operations on the tokens
    # 1: map pairs of less than flags and values to less than values
    # 2: Insert empties between pairs of wavelengths

    # 1...
    new_tokens = [tokens[0]]
    for prev, this in zip(tokens, tokens[1:]):
        if isinstance(this, LessThanFlag):
            # Don't add these
            continue

        if isinstance(prev, LessThanFlag):
            assert isinstance(this, Value)

            new_tokens.append(LessThanValue(this.value))

            continue

        # otherwise, just add the token
        new_tokens.append(this)


    tokens = new_tokens

    # 2...
    new_tokens = [tokens[0]]
    for prev, this in zip(tokens, tokens[1:]):
        if isinstance(this, Wavelength) and isinstance(prev, Wavelength):
            new_tokens.append(Empty())

        # otherwise, just add the token
        new_tokens.append(this)

    # Don't forget the last one too!
    if isinstance(new_tokens[-1], Wavelength):
        new_tokens.append(Empty())

    tokens = new_tokens

    # We should now have a list that alternates between wavelengths and values
    # ... check this

    wavelengths = []
    values = []
    less_than_flag = []

    for i, token in enumerate(tokens):
        if i % 2 == 0:
            assert isinstance(token, Wavelength)

            wavelengths.append(token.value)

        else:
            assert isinstance(token, (Empty, Value, LessThanValue))

            # Value
            if isinstance(token, Empty):
                values.append(None)
            else:
                values.append(token.value)

            # Less than
            if isinstance(token, LessThanValue):
                less_than_flag.append(True)
            else:
                less_than_flag.append(False)

    parsed_data = [tup for tup in zip(wavelengths, values, less_than_flag)]
    parsed_data.sort(key=lambda x: x[0])

    # Write out csv files
    if write:
        with open(f"spectra/detailed/{id}.csv", 'w') as file:
            file.write('"Wavelength /nm", "Transmittance", "Is upper bound"\n')
            for wavelength, value, is_upper_bound in parsed_data:
                file.write(f"{wavelength}, {value}, {is_upper_bound}\n")

    return [wl for wl, _, _ in parsed_data], \
            [val for _, val, _ in parsed_data], \
            [bound for _, _, bound in parsed_data]


#
# Main parsing
#

last_wavelengths = None # for checking

titles = ["Wavelength"]
rows = []

for id, _, _ in file_data:
    wavelengths, values, is_less_than = parse_text(id, verbose=False)

    titles.append(id) # title row

    if last_wavelengths is None: # First data entry
        for wavelength in wavelengths:
            rows.append([str(wavelength)])

    for i, (value, less_than) in enumerate(zip(values, is_less_than)):
        if value is None or less_than:
            rows[i].append("")

        else:
            rows[i].append(str(value))


    # Check all files have the same wavelengths

    wavelengths = np.array(wavelengths)

    if last_wavelengths is not None:
        assert np.all(wavelengths - last_wavelengths == 0)

    last_wavelengths = wavelengths

# Write to big table
titles = ['"'+title+'"' for title in titles]
rows = [titles] + rows

max_length = max([max([len(s) for s in row]) for row in rows])
spaces = [[""] + [" "*(max_length - len(s)) for s in row[:-1]] for row in rows]
rows = [[space + entry for space, entry in zip(space_row, row)] for space_row, row in zip(spaces, rows)]

with open("spectra/simple_data.csv", 'w') as file:
    for row in rows:
        file.write(",".join(row))
        file.write("\n")


#
# Another run through, but write the table with less than values included
#


last_wavelengths = None # for checking

titles = ["Wavelength"]
rows = []

for id, _, _ in file_data:
    wavelengths, values, is_less_than = parse_text(id, verbose=False, write=False)

    titles.append(id) # title row

    if last_wavelengths is None: # First data entry
        for wavelength in wavelengths:
            rows.append([str(wavelength)])

    for i, (value, less_than) in enumerate(zip(values, is_less_than)):
        if value is None: # <<< Only difference here
            rows[i].append("")

        else:
            rows[i].append(str(value))


    # Check all files have the same wavelengths

    wavelengths = np.array(wavelengths)

    if last_wavelengths is not None:
        assert np.all(wavelengths - last_wavelengths == 0)

    last_wavelengths = wavelengths

# Write to big table
titles = ['"'+title+'"' for title in titles]
rows = [titles] + rows

max_length = max([max([len(s) for s in row]) for row in rows])
spaces = [[""] + [" "*(max_length - len(s)) for s in row[:-1]] for row in rows]
rows = [[space + entry for space, entry in zip(space_row, row)] for space_row, row in zip(spaces, rows)]

with open("spectra/data_with_small_values.csv", 'w') as file:
    for row in rows:
        file.write(",".join(row))
        file.write("\n")
