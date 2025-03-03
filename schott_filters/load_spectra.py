import numpy as np
from dataclasses import dataclass

@dataclass
class SchottSpectrum:
    """ Spectrum of a Schott filter

    :param name: filter name
    :param wavelengths: in nm
    :param reference_thickness: in mm
    :param transmittance: dimensionless

    """
    name: str
    reference_thickness: float
    wavelengths: np.ndarray
    transmittance: np.ndarray

    @property
    def absorbance(self):
        return -np.log10(self.transmittance) / self.reference_thickness

def load_spectra(include_small_values=True) -> dict[str, SchottSpectrum]:
    if include_small_values:
        filename = "spectra/data_with_small_values.csv"
    else:
        filename = "spectra/simple_data.csv"

    with open(filename, 'r') as file:
        line = file.readline()
        names = [part.strip() for part in line.split(",")][1:]
        names = [name[1:-1] for name in names]

        data = [[] for _ in names]

        for line in file:
            parts = [part.strip() for part in line.split(",")]
            wavelength = float(parts[0])

            for dataset, s in zip(data, parts[1:]):
                if s != "":
                    dataset.append((wavelength, float(s)))

    thicknesses = {}
    # Load in the thicknesses
    with open("spectra/reference_thickness.csv", 'r') as file:
        file.readline() # skip first line
        for line in file:
            parts = line.split(",")
            name = parts[0].strip()[1:-1]
            thickness = float(parts[1])

            thicknesses[name] = thickness

    output = {}

    for name, dataset in zip(names, data):
        array = np.array(dataset)
        output[name] = SchottSpectrum(
            name=name,
            reference_thickness=thicknesses[name],
            wavelengths=array[:,0],
            transmittance=array[:, 1])

    return output

if __name__ == "__main__":
    print(load_spectra())

