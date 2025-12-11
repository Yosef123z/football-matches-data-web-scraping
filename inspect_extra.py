import requests
from datetime import datetime, timedelta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def save_html(url, filename):
    print(f"Fetching {url}...")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"Saved to {filename}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")

def main():
    # Yesterday's date
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%m/%d/%Y")
    save_html(f"https://www.yallakora.com/match-center?date={yesterday}", "matches_yesterday.html")
    
    # Standings page
    save_html("https://www.yallakora.com/group-standing/160/standings", "standings_real.html")

if __name__ == "__main__":
    main()
