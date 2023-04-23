import requests
import os
from bs4 import BeautifulSoup

def search_libgen(query):
    url = "https://libgen.is/search.php"
    params = {"req": query, "lg_topic": "libgen", "open": "0", "view": "simple", "res": "25", "phrase": "1", "column": "def"}

    response = requests.get(url, params=params)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    return soup.find_all("tr", {"valign": "top"})[1:6]


def download_book(row):
    base_url = "https://libgen.is/"
    title_cell = row.find_all("td")[2]
    book_page_link = title_cell.a["href"]
    book_page_url = base_url + book_page_link

    response = requests.get(book_page_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    first_mirror_link = soup.select_one("table tr:nth-child(18) td:nth-child(2) table tr td:nth-child(1) a")["href"]

    response = requests.get(first_mirror_link)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    download_link = soup.select_one("body table tr td:nth-child(2) div:nth-child(1) h2:nth-child(1) a")["href"]

    response = requests.get(download_link, stream=True)
    response.raise_for_status()

    filename = os.path.basename(download_link)
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print(f"Book downloaded as {filename}")




