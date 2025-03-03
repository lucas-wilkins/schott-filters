import requests
import pickle
import time

import numpy as np

with open("data/english_datasheet_urls.pickle", 'rb') as file:
    data = pickle.load(file)

for id, filename, url in data:

    print(id)
    response = requests.get(url)

    if response.status_code == 200:
        with open("data/datasheets/"+filename, "wb") as file:
            for chunk in response.iter_content(1024):  # Download in chunks
                file.write(chunk)

        print("Downloaded", id)

    else:
        print("Download failed", response.status_code)

    t = 20 + np.random.random() * 30
    print(f"Waiting {t} seconds")
    time.sleep(t)