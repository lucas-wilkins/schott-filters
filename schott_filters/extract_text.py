import fitz

from file_data import file_data

for id, filename, url in file_data:

    # Open the PDF file
    doc = fitz.open("data/datasheets/"+filename)

    # Extract text from all pages
    text = "\n".join([page.get_text() for page in doc])

    with open(f"data/datasheet-text/{id}.txt", 'w', encoding="utf-8") as file:
        file.write(text)