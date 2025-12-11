# Yallakora Web Scraper 🏆⚽

A beautiful and functional web scraping application built with Streamlit to extract football/soccer data from Yallakora.com.

## Features

- **Match Scraping**: Get live match scores, schedules, and results
  - Scrape today's matches or select a custom date
  - View team names, scores, and match times
  - Filter by tournament/league

- **News Scraping**: Extract latest football news
  - Get headlines and links
  - Customize the number of articles to scrape

- **League Standings**: Fetch league tables
  - Support for multiple leagues (Egyptian League, Premier League, La Liga, etc.)
  - View complete standings with stats

- **Data Export**: Download scraped data
  - Export to CSV format
  - Export to JSON format

## Installation

1. Install Python 3.8 or higher

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:
```bash
streamlit run yallakora_scraper.py
```

The application will open in your default web browser at `http://localhost:8501`

## How to Use

1. **Select Scraping Type**: Choose from the sidebar whether you want to scrape:
   - Matches
   - News
   - League Standings

2. **Configure Options**: 
   - For matches: Select today or a custom date
   - For news: Choose how many articles to scrape
   - For standings: Select the league

3. **Scrape Data**: Click the scrape button to fetch data

4. **Export Data**: Download the results as CSV or JSON

## Features in Detail

### Match Scraping
- Retrieves match information including:
  - Tournament name
  - Home and away teams
  - Current score
  - Match time
  
### News Scraping
- Extracts news articles with:
  - Article title
  - Publication date
  - Article link

### League Standings
- Displays league tables with:
  - Team position
  - Matches played
  - Wins, draws, losses
  - Total points

## Technical Details

- **Web Scraping**: BeautifulSoup4 for HTML parsing
- **HTTP Requests**: requests library with custom headers
- **UI Framework**: Streamlit
- **Data Processing**: pandas for data manipulation
- **Rate Limiting**: Built-in delays to respect server resources

## Important Notes

⚠️ **Ethical Scraping**:
- This tool includes rate limiting to avoid overwhelming the server
- Please respect Yallakora.com's terms of service
- Use responsibly and for personal/educational purposes only
- Check the website's robots.txt file

## Troubleshooting

**Issue**: No data appears after scraping
- **Solution**: The website structure may have changed. Check the website manually and update the CSS selectors in the code.

**Issue**: Connection timeout
- **Solution**: Check your internet connection or try again later. The website might be temporarily unavailable.

**Issue**: Installation errors
- **Solution**: Make sure you have Python 3.8+ and try updating pip: `pip install --upgrade pip`

## Requirements

- Python 3.8+
- streamlit 1.29.0
- requests 2.31.0
- beautifulsoup4 4.12.2
- pandas 2.1.4
- lxml 4.9.3

## License

This project is for educational purposes only.

## Disclaimer

This tool is not affiliated with Yallakora.com. All data belongs to their respective owners.
