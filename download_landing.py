import requests

url = "https://www.schott.com/en-gb/special-selection-tools/interactive-filter-diagram"  # Replace with the URL you want to download
response = requests.get(url)

if response.status_code == 200:
    with open("data/landing_page.html", "w", encoding="utf-8") as file:
        file.write(response.text)

    print("Downloaded")

else:
    print("Download failed", response.status_code)