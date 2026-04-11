import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_port_data():
    """Scrapes a list of common network ports to augment our intrusion data."""
    url = "https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers"
    print(f"Scraping port information from {url}...")
    

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    

    table = soup.find('table', {'class': 'wikitable'})
    df_ports = pd.read_html(str(table))[0]
    

    df_ports = df_ports[['Port', 'Description']].head(20)
    return df_ports