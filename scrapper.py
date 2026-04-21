import requests
from bs4 import BeautifulSoup
import pandas as pd
import random

headers = {"User-Agent": "Mozilla/5.0"}

data = []

# Scrape multiple pages
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

# ---- UPGRADE STARTS HERE ----

# Rename column
df.rename(columns={"Title": "Product_Name"}, inplace=True)

# Clean price
df["Price"] = df["Price"].str.replace("£", "").astype(float)

# Add fake brands
brands = ["Zara", "H&M", "Nike", "Urbanic", "Forever21"]
df["Brand"] = [random.choice(brands) for _ in range(len(df))]

# Add category
df["Category"] = "Clothing"

# Save file
df.to_csv("products_data.csv", index=False)

print(df.head())