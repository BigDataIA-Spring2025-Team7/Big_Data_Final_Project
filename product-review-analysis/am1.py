from serpapi import GoogleSearch
import pandas as pd
import matplotlib.pyplot as plt

def search_laptops_serpapi(api_key, query="best laptops under $1000"):
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "gl": "us",
        "hl": "en",
        "tbm": "shop"  # Ensures Google Shopping results
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    laptops = []
    for item in results.get("shopping_results", []):
        try:
            price = float(item.get("price", "$0").replace("$", "").replace(",", ""))
        except:
            price = None
        laptops.append({
            "title": item.get("title"),
            "price": price,
            "rating": float(item.get("rating", 0)),
            "reviews": int(item.get("reviews", 0)),
            "source": item.get("source"),
            "link": item.get("link")
        })

    df = pd.DataFrame(laptops)
    return df

# === MAIN EXECUTION ===
if __name__ == "__main__":
    api_key = "YOUR_SERPAPI_KEY"  # Replace with your key
    df = search_laptops_serpapi(api_key)

    if df.empty:
        print("❌ No data returned from SerpAPI. Try a different query or check your API key/usage.")
    else:
        print(f"✅ Scraped {len(df)} laptops.")

        # Visualization 1: Ratings comparison
        df.plot(kind="bar", x="title", y="rating", title="Laptop Ratings Comparison", legend=False, figsize=(10,5))
        plt.ylabel("Rating")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

        # Visualization 2: Price vs. Number of Reviews
        df.plot(kind="scatter", x="price", y="reviews", title="Price vs. Reviews", figsize=(10,5))
        plt.grid(True)
        plt.tight_layout()
        plt.show()
