import requests
import os

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
    save_html("https://www.yallakora.com/match-center", "matches.html")
    save_html("https://www.yallakora.com/news", "news.html")
    save_html("https://www.yallakora.com/league-standings/egyptian-league", "standings.html")

if __name__ == "__main__":
    main()
