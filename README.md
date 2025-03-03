schott-filters
==============

Grab the Schott filter datasheets from the Schott website and parse into a useful form.


Data files
----------

The following files are created by interpreting the published datasheets 

* `data_with_small_values.csv` Data with the 1e-5 entered when only the upper bound specified
* `simple_data.csv` Data where only exactly reported numbers are given
* `detailed/*` Individual data, with three columns, the last saying whether the value was specified as a bound.
* `reference_thicknesses.csv` Thickness of glass for which it is measured


When transmittance is low, the datasheets report `< 1,000E-5`, the way this is dealt with
affects the files here. The wavelengths are always the same, but sometimes the data is 
not present for all of them.


Code
----

The code to scrape the website is included, but not the downloaded files themselves.

Workflow
--------

pip install everything in `requirements.txt`

There is a sequence of scripts to rebuild the data (run from the repo root)...

 1) `download_landing` - download the landing page
 2) `pull_json` - grabs the JSON object containing all the links for the landing page
 3) `compile_downloads` - turns the JSON data into a list of downloads
 4) `download_datasheets` - downloads the datasheets in .pdf form
 5) `extract_text` - gets the text from the .pdfs
 6) `parse_text` - parses the text and extracts the data, and
    `reference_thicknesses` - generates a file with the thicknesses of the samples

Other useful things

 * `load_spectra` has a method to load in spectra as a dict of dataclasses
 * `file_data` contains a list (also called `file_data`) that contains name, pdf file, and url
