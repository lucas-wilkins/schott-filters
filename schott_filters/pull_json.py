from bs4 import BeautifulSoup

with open("data/landing_page.html", 'r') as fid:
    html = fid.read()

soup = BeautifulSoup(html, "html.parser")

# Find the first tag with class "content"
tag = soup.find(class_="interactivefilterdiagram")

print(tag.attrs["data-config"])

with open("data/index.json", 'w') as fid:
    fid.write(tag.attrs["data-config"])

