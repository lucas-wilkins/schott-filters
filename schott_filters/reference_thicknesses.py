""" Find the reference thickness field"""
import re

from file_data import file_data

with open("spectra/reference_thickness.csv", 'w') as output_file:
    output_file.write('"id", "thickness /mm"\n')


    for id, _, _ in file_data:
        print(id,"", end="")

        size = None

        with open(f"data/datasheet-text/{id}.txt", 'r') as file:
            lines = [line.strip() for line in file.readlines()]
            for i, line in enumerate(lines):
                if line.startswith("d"):

                    # Sometimes the value is grouped with equals, sometimes not


                    if lines[i+1] == "=":
                        size = lines[i+2]
                        n = 2
                    else:
                        size = lines[i+1][1:].strip()
                        n = 1

                    try:
                        int(size)
                        size += " " + lines[i+n+1]

                    except:
                        pass

        print(size)

        # Parse the number

        parts = size.split(" ")
        englished = re.sub(",", ".", parts[0])
        size_float = float(englished)

        output_file.write(f'"{id}", {size_float}\n')

