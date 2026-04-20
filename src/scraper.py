import pandas as pd
import requests
from bs4 import BeautifulSoup
import io
def scrape_port_data():
    """Scrapes a security-focused port list from StationX."""
    url = "https://www.stationx.net/common-ports-cheat-sheet/"
    print(f"Scraping port information from {url}...")
    
    try:
        # We use a header because some sites block 'bots'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        
        # This site uses standard HTML tables
        import io
        df_list = pd.read_html(io.StringIO(response.text))
        
        # The first table [0] is usually the 'Well-known Ports'
        df_ports = df_list[0]
        
        # Standardizing column names
        df_ports = df_ports.iloc[:, [0, 2]].head(20) # Grab port and description
        df_ports.columns = ['Port', 'Description']
        
        return df_ports
    
    except Exception as e:
        return f"Could not scrape StationX: {e}"
if __name__ == "__main__":
    result = scrape_port_data()
    print(result) 