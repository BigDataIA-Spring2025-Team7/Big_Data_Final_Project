import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
import re

class AmazonReviewScraper:
    def __init__(self):
        """
        Initialize Amazon Review Scraper
        """
        # Create output directories
        os.makedirs('data', exist_ok=True)
        os.makedirs('visualizations', exist_ok=True)
        
        # Sophisticated User Agent Rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]

    def _get_request_headers(self):
        """
        Generate headers to mimic browser request
        
        :return: Dictionary of headers
        """
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def scrape_amazon_reviews(self, product_url, max_pages=5):
        """
        Comprehensive Amazon review scraping method
        
        :param product_url: Amazon product URL
        :param max_pages: Maximum number of review pages to scrape
        :return: DataFrame with reviews
        """
        # Multiple URL variants for reviews
        review_url_variants = [
            # Standard review URL formats
            f"{product_url.split('/dp/')[0]}/product-reviews/{product_url.split('/dp/')[1].split('/')[0]}",
            f"{product_url}/reviews",
            f"{product_url.split('/dp/')[0]}/product-reviews"
        ]
        
        all_reviews = []
        
        for base_url in review_url_variants:
            for page in range(1, max_pages + 1):
                try:
                    # Construct page URL
                    page_url = f"{base_url}?pageNumber={page}"
                    
                    # Random delay to avoid rate limiting
                    time.sleep(random.uniform(2, 5))
                    
                    # Send request
                    response = requests.get(
                        page_url, 
                        headers=self._get_request_headers()
                    )
                    
                    # Check for successful request
                    response.raise_for_status()
                    
                    # Parse HTML
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Enhanced review finding
                    review_elements = (
                        soup.find_all('div', {'data-hook': 'review'}) or
                        soup.find_all('div', class_=re.compile(r'review')) or
                        soup.find_all('div', id=re.compile(r'review'))
                    )
                    
                    # If no reviews found in this variant, try next
                    if not review_elements:
                        break
                    
                    # Extract reviews
                    for review in review_elements:
                        try:
                            # Multiple rating extraction methods
                            rating_elem = (
                                review.find('i', {'data-hook': 'review-star-rating'}) or
                                review.find('span', class_=re.compile(r'a-icon-alt'))
                            )
                            
                            # Extract rating
                            rating = float(rating_elem.text.split()[0]) if rating_elem else None
                            
                            # Multiple text extraction methods
                            text_elem = (
                                review.find('span', {'data-hook': 'review-body'}) or
                                review.find('div', class_=re.compile(r'review-text'))
                            )
                            review_text = text_elem.text.strip() if text_elem else ''
                            
                            # Date extraction
                            date_elem = (
                                review.find('span', {'data-hook': 'review-date'}) or
                                review.find('span', class_=re.compile(r'review-date'))
                            )
                            review_date = date_elem.text.strip() if date_elem else ''
                            
                            # Reviewer name
                            name_elem = (
                                review.find('span', {'class': 'a-profile-name'}) or
                                review.find('span', class_=re.compile(r'profile-name'))
                            )
                            reviewer_name = name_elem.text.strip() if name_elem else ''
                            
                            # Add to reviews if valid
                            if rating and review_text:
                                all_reviews.append({
                                    'rating': rating,
                                    'review_text': review_text,
                                    'date': review_date,
                                    'reviewer': reviewer_name
                                })
                        
                        except Exception as review_error:
                            print(f"Error parsing individual review: {review_error}")
                    
                    # Check for more pages
                    next_page = soup.find('li', {'class': 'a-last'})
                    if not next_page or 'a-disabled' in next_page.get('class', []):
                        break
                
                except requests.RequestException as e:
                    print(f"Error scraping page {page}: {e}")
                    break
            
            # If reviews found, stop trying variants
            if all_reviews:
                break
        
        # Convert to DataFrame
        reviews_df = pd.DataFrame(all_reviews)
        
        return reviews_df

    def analyze_reviews(self, reviews_df, product_name):
        """
        Analyze and save scraped reviews
        
        :param reviews_df: DataFrame with reviews
        :param product_name: Name of the product
        """
        if reviews_df.empty:
            print(f"No reviews found for {product_name}")
            return
        
        # Save reviews to CSV
        csv_path = os.path.join('data', f'{product_name.replace(" ", "_")}_reviews.csv')
        reviews_df.to_csv(csv_path, index=False)
        print(f"Saved {len(reviews_df)} reviews for {product_name}")
        
        # Basic analysis
        print(f"\nReview Analysis for {product_name}")
        print(f"Total Reviews: {len(reviews_df)}")
        
        # Rating distribution
        print("\nRating Distribution:")
        rating_dist = reviews_df['rating'].value_counts().sort_index()
        print(rating_dist)
        
        # Average rating
        avg_rating = reviews_df['rating'].mean()
        print(f"\nAverage Rating: {avg_rating:.2f}")
        
        # Optional: Save basic stats to JSON
        stats = {
            'total_reviews': len(reviews_df),
            'average_rating': avg_rating,
            'rating_distribution': rating_dist.to_dict()
        }
        
        with open(os.path.join('data', f'{product_name.replace(" ", "_")}_stats.json'), 'w') as f:
            json.dump(stats, f, indent=4)

def main():
    # Updated with specific, full Amazon product URLs
    products = [
        {
            'name': 'MacBook Pro M2',
            'url': 'https://www.amazon.com/Apple-MacBook-Chip-256GB-Silver/dp/B0B3DPLDD5'
        },
        {
            'name': 'iPhone 14 Pro',
            'url': 'https://www.amazon.com/Apple-iPhone-Pro-128GB-Silver/dp/B0BDHX8Z63'
        }
    ]
    
    # Initialize scraper
    scraper = AmazonReviewScraper()
    
    # Scrape and analyze reviews for each product
    for product in products:
        print(f"\n🔍 Scraping reviews for: {product['name']}")
        
        try:
            # Scrape reviews
            reviews = scraper.scrape_amazon_reviews(product['url'], max_pages=5)
            
            # Analyze reviews
            scraper.analyze_reviews(reviews, product['name'])
        
        except Exception as e:
            print(f"Error processing {product['name']}: {e}")

if __name__ == "__main__":
    main()