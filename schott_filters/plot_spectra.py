from load_spectra import load_spectra
import matplotlib.pyplot as plt


spectra = load_spectra()

for name in spectra:
    spectrum = spectra[name]

    plt.plot(spectrum.wavelengths, spectrum.transmittance, label=name)

plt.show()