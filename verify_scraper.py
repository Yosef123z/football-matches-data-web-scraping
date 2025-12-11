from yallakora_scraper import YallakoraScraper
import pandas as pd
import sys

# Force UTF-8 for stdout
sys.stdout.reconfigure(encoding='utf-8')

def test_scraper():
    print("Testing Yallakora Scraper...")
    scraper = YallakoraScraper()

    # Test Matches
    print("\n1. Testing Match Scraping...")
    matches = scraper.scrape_matches()
    if matches:
        print(f"[OK] Found {len(matches)} matches")
        print("Sample match:", matches[0])
    else:
        print("[WARN] No matches found. Checking raw response...")
        # Debugging
        import requests
        try:
            response = requests.get("https://www.yallakora.com/match-center", headers=scraper.headers)
            print(f"Status Code: {response.status_code}")
            print(f"Content Length: {len(response.content)}")
            print("First 500 chars of HTML:")
            print(response.text[:500])
        except Exception as e:
            print(f"Error fetching debug info: {e}")
        
        # Try yesterday
        from datetime import datetime, timedelta
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%m/%d/%Y")
        print(f"\n[INFO] Trying yesterday's matches ({yesterday})...")
        matches_y = scraper.scrape_matches(yesterday)
        if matches_y:
             print(f"[OK] Found {len(matches_y)} matches for yesterday")
             print("Sample match:", matches_y[0])
        else:
             print("[WARN] No matches found for yesterday either.")

    # Test News
    print("\n2. Testing News Scraping...")
    news = scraper.scrape_news(limit=3)
    if news:
        print(f"[OK] Found {len(news)} news articles")
        print("Sample news:", news[0])
    else:
        print("[FAIL] Failed to scrape news")

    # Test Standings
    print("\n3. Testing Standings Scraping (Egyptian League - ID 160)...")
    standings = scraper.scrape_league_table(160)
    if standings:
        print(f"[OK] Found {len(standings)} teams in standings")
        print("Top team:", standings[0])
    else:
        print("[FAIL] Failed to scrape standings")

if __name__ == "__main__":
    test_scraper()
