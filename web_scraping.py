import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate  # for pretty printing

def rating_to_int(rating_str):
    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    return rating_map.get(rating_str, 0)  # return 0 if not found

base_url = "http://books.toscrape.com/catalogue/page-{}.html"
all_books = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                  " AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/58.0.3029.110 Safari/537.3"
}

for page in range(1, 6):
    url = base_url.format(page)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve page {page}: {e}")
        continue

    soup = BeautifulSoup(response.content, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]
        price_text = book.find("p", class_="price_color").text.strip()
        price = float(price_text.lstrip('£'))  # convert to float
        availability = book.find("p", class_="instock availability").text.strip()
        rating_str = book.p["class"][1]
        rating = rating_to_int(rating_str)
        link = "http://books.toscrape.com/catalogue/" + book.h3.a["href"]

        all_books.append({
            "Title": title,
            "Price (£)": price,
            "Availability": availability,
            "Rating (1-5)": rating,
            "Link": link
        })

df = pd.DataFrame(all_books)
df.to_csv("books_data.csv", index=False)
print("✅ Web scraping completed!")

# Pretty print first 4 rows of dataframe
print(tabulate(df.head(4), headers='keys', tablefmt='fancy_grid', showindex=False))
