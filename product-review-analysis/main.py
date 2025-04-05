import os
import requests
import pandas as pd
import random
import time
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ProductReviewCollector:
    def __init__(self):
        """
        Initialize Product Review Collector
        """
        # Create output directories
        os.makedirs('data', exist_ok=True)
        os.makedirs('visualizations', exist_ok=True)
        
        # Detailed User Agent Rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        
        # SERP API Key and Configuration
        self.serp_api_key = os.getenv('SERP_API_KEY')
        
        # Alternative Review Sources
        self.alternative_sources = [
            self._fetch_rapid_api_reviews,
            self._generate_mock_reviews
        ]

    def _fetch_rapid_api_reviews(self, product_name):
        """
        Fetch reviews from RapidAPI (example implementation)
        
        :param product_name: Name of the product
        :return: DataFrame with reviews
        """
        # This is a placeholder - you'd need to replace with actual RapidAPI endpoint
        # Note: This requires a RapidAPI subscription
        rapid_api_key = os.getenv('RAPID_API_KEY')
        if not rapid_api_key:
            print("RapidAPI key not found.")
            return pd.DataFrame()
        
        url = "https://example-review-api.p.rapidapi.com/reviews"
        headers = {
            "X-RapidAPI-Key": rapid_api_key,
            "X-RapidAPI-Host": "example-review-api.p.rapidapi.com"
        }
        
        try:
            response = requests.get(url, headers=headers, params={'product': product_name})
            response.raise_for_status()
            
            data = response.json()
            reviews = []
            for review in data.get('reviews', []):
                reviews.append({
                    'rating': review.get('rating', 0),
                    'review_text': review.get('text', ''),
                    'source': 'RapidAPI'
                })
            
            return pd.DataFrame(reviews)
        except requests.RequestException as e:
            print(f"RapidAPI error: {e}")
            return pd.DataFrame()

    def _generate_mock_reviews(self, product_name):
        """
        Generate mock reviews when no real data is available
        
        :param product_name: Name of the product
        :return: DataFrame with mock reviews
        """
        # Generate synthetic reviews
        mock_reviews = []
        ratings = random.choices([1, 2, 3, 4, 5], 
                                 weights=[0.1, 0.2, 0.3, 0.3, 0.1], 
                                 k=50)
        
        for rating in ratings:
            mock_reviews.append({
                'rating': rating,
                'review_text': f"Mock review for {product_name} with rating {rating}",
                'source': 'Mock Generator'
            })
        
        return pd.DataFrame(mock_reviews)

    def get_serp_reviews(self, product_name):
        """
        Fetch product reviews using SERP API with enhanced error handling
        
        :param product_name: Name of the product
        :return: DataFrame with reviews
        """
        if not self.serp_api_key:
            print("SERP API key not found.")
            return pd.DataFrame()
        
        try:
            # SERP API endpoint
            url = "https://serpapi.com/search"
            
            # Comprehensive parameters
            params = {
                "engine": "google_product_reviews",
                "q": product_name,
                "api_key": self.serp_api_key,
                "num": 100  # Request more reviews
            }
            
            # Add random delay
            time.sleep(random.uniform(1, 3))
            
            # Send API request with enhanced headers
            response = requests.get(url, 
                                    params=params, 
                                    headers={'User-Agent': random.choice(self.user_agents)})
            
            # Enhanced error handling
            if response.status_code != 200:
                print(f"SERP API Error: {response.status_code}")
                print(f"Response Content: {response.text}")
                return pd.DataFrame()
            
            # Parse API response
            data = response.json()
            
            # Extract reviews
            reviews = []
            for review in data.get('reviews', []):
                reviews.append({
                    'rating': review.get('rating', 0),
                    'review_text': review.get('text', ''),
                    'source': 'SERP API'
                })
            
            return pd.DataFrame(reviews)
        
        except requests.RequestException as e:
            print(f"SERP API Request Error: {e}")
            return pd.DataFrame()
        except json.JSONDecodeError:
            print("Failed to parse SERP API response")
            return pd.DataFrame()

    def collect_reviews(self, product_name):
        """
        Collect reviews using multiple sources
        
        :param product_name: Name of the product
        :return: DataFrame with reviews
        """
        # Primary sources
        review_sources = [
            (self.get_serp_reviews, f"Fetching SERP API reviews for {product_name}"),
        ]
        
        # Add alternative sources
        review_sources.extend(
            [(source, f"Trying alternative source: {source.__name__}") 
             for source in self.alternative_sources]
        )
        
        # Try each source
        for source, message in review_sources:
            print(message)
            reviews = source(product_name)
            
            if not reviews.empty:
                return reviews
        
        print(f"No reviews found for {product_name}")
        return pd.DataFrame()

def main():
    # List of products to collect reviews for
    products = [
        'MacBook Pro',
        'iPhone 14',
        'Samsung Galaxy'
    ]
    
    # Initialize collector
    collector = ProductReviewCollector()
    
    # Collect and analyze reviews for each product
    for product in products:
        print(f"\n🔍 Collecting reviews for: {product}")
        
        # Collect reviews
        reviews = collector.collect_reviews(product)
        
        # Basic analysis if reviews found
        if not reviews.empty:
            # Save to CSV
            csv_path = os.path.join('data', f'{product.replace(" ", "_")}_reviews.csv')
            reviews.to_csv(csv_path, index=False)
            
            # Print basic stats
            print(f"\n📊 Review Analysis for {product}")
            print(f"Total Reviews: {len(reviews)}")
            print("\nRating Distribution:")
            print(reviews['rating'].value_counts().sort_index())
        else:
            print(f"❌ No reviews collected for {product}")

if __name__ == "__main__":
    main()