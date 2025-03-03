from load_spectra import load_spectra, SchottSpectrum
import re
from collections import defaultdict

spectra = load_spectra(include_small_values=False)
groups = defaultdict(dict[str, SchottSpectrum])

for name in spectra:
    # get string start
    matches = re.findall(r'^([A-Z-]*)', name)

    group_name = matches[0]
    groups[group_name][name] = spectra[name]

if __name__ == "__main__":
    
    import matplotlib.pyplot as plt

    for group_name in groups:
        plt.figure(group_name)
        group = groups[group_name]
        for name in group:
            spectrum = group[name]
            plt.plot(spectrum.wavelengths, spectrum.absorbance, label=name)

        plt.xlim([200, 800])
        plt.legend()

    plt.show()