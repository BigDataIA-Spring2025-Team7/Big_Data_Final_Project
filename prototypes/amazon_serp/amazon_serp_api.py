import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Access the key securely
API_KEY = os.getenv("SERP_API")

params = {
    "engine": "google_shopping",
    "q": "laptop",
    "api_key": API_KEY,
    "hl": "en",      # language
    "gl": "us"       # location
}

response = requests.get("https://serpapi.com/search.json", params=params)

if response.status_code == 200:
    results = response.json()
    products = []

    for item in results.get("shopping_results", []):
        products.append({
            "title": item.get("title"),
            "price": item.get("price"),
            "source": item.get("source"),
            "rating": item.get("rating"),
            "reviews": item.get("reviews"),
            "link": item.get("link"),
            "image": item.get("thumbnail")
        })

    df = pd.DataFrame(products)
    df.to_csv("google_shopping_laptops.csv", index=False)
    print("✅ Saved data to google_shopping_laptops.csv")

else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
