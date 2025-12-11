import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Yallakora Web Scraper",
    page_icon="⚽",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem;
        font-size: 16px;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    h1 {
        color: #2E7D32;
        text-align: center;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

class YallakoraScraper:
    def __init__(self):
        self.base_url = "https://www.yallakora.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_matches(self, date=None):
        """Scrape matches for a specific date."""
        if date is None:
            date = datetime.now().strftime("%m/%d/%Y")
        else:
            # Ensure date is in correct format
            try:
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                date = date_obj.strftime("%m/%d/%Y")
            except ValueError:
                pass # Assume it's already in the right format or let the URL handle it

        url = f"https://www.yallakora.com/match-center?date={date}"
        print(f"Fetching matches from: {url}")
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')
            
            matches = []
            
            # The structure is: Championships are in div.matchCard
            # Matches are in div.liItem inside the matchCard
            
            championships = soup.find_all('div', class_='matchCard')
            
            if not championships:
                return []

            for championship in championships:
                title_elem = championship.find('div', class_='title')
                championship_title = title_elem.find('h2').text.strip() if title_elem and title_elem.find('h2') else "Unknown Championship"
                
                match_items = championship.find_all('div', class_='liItem')
                
                for item in match_items:
                    match_data = {'Championship': championship_title}
                    
                    # Team A
                    team_a_div = item.find('div', class_='teamA')
                    match_data['Team A'] = team_a_div.find('p').text.strip() if team_a_div and team_a_div.find('p') else "Unknown"
                    
                    # Team B
                    team_b_div = item.find('div', class_='teamB')
                    match_data['Team B'] = team_b_div.find('p').text.strip() if team_b_div and team_b_div.find('p') else "Unknown"
                    
                    # Score & Time
                    m_result = item.find('div', class_='MResult')
                    if m_result:
                        scores = m_result.find_all('span', class_='score')
                        if len(scores) >= 2:
                            match_data['Score'] = f"{scores[0].text.strip()} - {scores[1].text.strip()}"
                        else:
                            match_data['Score'] = "-"
                            
                        time_span = m_result.find('span', class_='time')
                        match_data['Time'] = time_span.text.strip() if time_span else "Unknown"
                    else:
                        match_data['Score'] = "-"
                        match_data['Time'] = "Unknown"
                        
                    # Status
                    status_div = item.find('div', class_='matchStatus')
                    match_data['Status'] = status_div.find('span').text.strip() if status_div and status_div.find('span') else "Unknown"
                    
                    matches.append(match_data)
            
            return matches

        except Exception as e:
            st.error(f"Error scraping matches: {e}")
            return []

    def scrape_news(self, limit=10):
        """Scrape latest news."""
        url = "https://www.yallakora.com/newslisting"
        print(f"Fetching news from: {url}")
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')
            
            news_list = []
            
            # News items are in div.cnts ul li
            articles = soup.select('div.cnts ul li')
            
            for article in articles[:limit]:
                news_item = {}
                
                # Link and Title
                link_tag = article.find('a', class_='link')
                if link_tag:
                    news_item['Link'] = "https://www.yallakora.com" + link_tag['href']
                    news_item['Title'] = link_tag.get('title', '').strip()
                    
                    # Image
                    img_tag = link_tag.find('img')
                    if img_tag:
                        news_item['Image'] = img_tag.get('src') or img_tag.get('data-src')
                else:
                    # Fallback if structure is slightly different
                    a_tag = article.find('a')
                    if a_tag:
                        news_item['Link'] = "https://www.yallakora.com" + a_tag['href']
                        p_tag = article.find('p')
                        news_item['Title'] = p_tag.text.strip() if p_tag else "No Title"
                
                # Date
                date_div = article.find('div', class_='time') or article.find('p', class_='date')
                if date_div:
                    news_item['Date'] = date_div.text.strip()
                else:
                    news_item['Date'] = "Unknown"
                
                if news_item.get('Title'):
                    news_list.append(news_item)
            
            return news_list

        except Exception as e:
            st.error(f"Error scraping news: {e}")
            return []

    def scrape_league_table(self, league_id=160):
        """Scrape league standings."""
        url = f"https://www.yallakora.com/group-standing/{league_id}/standings"
        print(f"Fetching standings from: {url}")
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')
            
            standings = []
            
            # Standings are in div.wRow
            rows = soup.find_all('div', class_='wRow')
            
            for row in rows:
                team_data = {}
                
                # Rank
                rank_div = row.find('div', class_='arrng')
                team_data['Rank'] = rank_div.text.strip() if rank_div else "-"
                
                # Team
                team_div = row.find('div', class_='team')
                if team_div:
                    team_p = team_div.find('p')
                    team_data['Team'] = team_p.text.strip() if team_p else "Unknown"
                else:
                    team_data['Team'] = "Unknown"
                
                # Stats (Played, Won, Drawn, Lost, GF, GA, GD, Points)
                dtls = row.find_all('div', class_='dtls')
                if len(dtls) >= 8:
                    team_data['Played'] = dtls[0].text.strip()
                    team_data['Won'] = dtls[1].text.strip()
                    team_data['Drawn'] = dtls[2].text.strip()
                    team_data['Lost'] = dtls[3].text.strip()
                    team_data['GF'] = dtls[4].text.strip()
                    team_data['GA'] = dtls[5].text.strip()
                    team_data['GD'] = dtls[6].text.strip()
                    team_data['Points'] = dtls[7].text.strip()
                
                standings.append(team_data)
            
            return standings

        except Exception as e:
            st.error(f"Error scraping standings: {e}")
            return []

def main():
    st.title("⚽ Yallakora Web Scraper")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("Scraping Options")
    scrape_type = st.sidebar.selectbox(
        "Select what to scrape:",
        ["Matches", "News", "League Standings"]
    )
    
    scraper = YallakoraScraper()
    
    if scrape_type == "Matches":
        st.header("🏆 Match Center")
        
        col1, col2 = st.columns(2)
        with col1:
            date_option = st.radio("Select Date:", ["Today", "Custom Date"])
        
        selected_date = None
        if date_option == "Custom Date":
            with col2:
                date_input = st.date_input("Choose a date:")
                selected_date = date_input.strftime("%Y-%m-%d")
        
        if st.button("Scrape Matches", key="matches_btn"):
            with st.spinner("Scraping matches... Please wait"):
                time.sleep(1)  # Rate limiting
                matches = scraper.scrape_matches(selected_date)
                
                if matches:
                    st.success(f"✅ Successfully scraped {len(matches)} matches!")
                    
                    # Display as dataframe
                    df = pd.DataFrame(matches)
                    st.dataframe(df, use_container_width=True)
                    
                    # Export options
                    st.subheader("📥 Export Options")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        csv = df.to_csv(index=False).encode('utf-8-sig')
                        st.download_button(
                            label="Download as CSV",
                            data=csv,
                            file_name=f"yallakora_matches_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        json_str = df.to_json(orient='records', indent=2, force_ascii=False)
                        st.download_button(
                            label="Download as JSON",
                            data=json_str,
                            file_name=f"yallakora_matches_{datetime.now().strftime('%Y%m%d')}.json",
                            mime="application/json"
                        )
                else:
                    st.warning("⚠️ No matches found or error occurred.")
    
    elif scrape_type == "News":
        st.header("📰 Latest News")
        
        news_limit = st.slider("Number of news articles:", min_value=5, max_value=50, value=10)
        
        if st.button("Scrape News", key="news_btn"):
            with st.spinner("Scraping news... Please wait"):
                time.sleep(1)  # Rate limiting
                news = scraper.scrape_news(news_limit)
                
                if news:
                    st.success(f"✅ Successfully scraped {len(news)} news articles!")
                    
                    df = pd.DataFrame(news)
                    st.dataframe(df, use_container_width=True)
                    
                    # Export options
                    st.subheader("📥 Export Options")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        csv = df.to_csv(index=False).encode('utf-8-sig')
                        st.download_button(
                            label="Download as CSV",
                            data=csv,
                            file_name=f"yallakora_news_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        json_str = df.to_json(orient='records', indent=2, force_ascii=False)
                        st.download_button(
                            label="Download as JSON",
                            data=json_str,
                            file_name=f"yallakora_news_{datetime.now().strftime('%Y%m%d')}.json",
                            mime="application/json"
                        )
                else:
                    st.warning("⚠️ No news found or error occurred.")
    
    elif scrape_type == "League Standings":
        st.header("📊 League Standings")
        
        leagues = {
            "Egyptian League": 160,
            "English Premier League": 93,
            "Spanish League": 101,
            "Italian League": 100,
            "German League": 98,
            "French League": 95,
            "Saudi League": 102
        }
        
        selected_league = st.selectbox("Select League", list(leagues.keys()))
        
        if st.button("Get Standings"):
            with st.spinner("Fetching standings..."):
                standings = scraper.scrape_league_table(leagues[selected_league])
                
                if standings:
                    df = pd.DataFrame(standings)
                    st.dataframe(df, use_container_width=True)
                    
                    # Export options
                    col1, col2 = st.columns(2)
                    with col1:
                        csv = df.to_csv(index=False).encode('utf-8-sig')
                        st.download_button(
                            "Download CSV",
                            csv,
                            f"{selected_league}_standings.csv",
                            "text/csv",
                            key='download-csv'
                        )
                    with col2:
                        json_str = df.to_json(orient="records", force_ascii=False)
                        st.download_button(
                            "Download JSON",
                            json_str,
                            f"{selected_league}_standings.json",
                            "application/json",
                            key='download-json'
                        )
                else:
                    st.warning("No standings found or error occurred.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            <p>Built with ❤️ using Streamlit | Data from Yallakora.com</p>
            <p style='font-size: 12px;'>Note: Please respect the website's robots.txt and terms of service</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
