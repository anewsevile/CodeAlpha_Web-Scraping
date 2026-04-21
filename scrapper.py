import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {"User-Agent": "Mozilla/5.0"}

data = []

# Scrape 5 pages
for page in range(1, 6):
    url = f"http://books.toscrape.com/catalogue/page-{page}.html"
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        rating = book.p["class"][1]

        data.append([title, price, rating])

# Create DataFrame
df = pd.DataFrame(data, columns=["Title", "Price", "Rating"])

# Clean price (remove £ and convert to float)
df["Price"] = df["Price"].str.replace("£", "").astype(float)

# Save CSV
df.to_csv("books_data.csv", index=False)

print(df.head())
