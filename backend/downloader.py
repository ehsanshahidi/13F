import requests
from bs4 import BeautifulSoup

def download_13f_filings(cik, start_date, end_date):
    base_url = "https://www.sec.gov/cgi-bin/browse-edgar"
    params = {
        "action": "getcompany",
        "CIK": cik,
        "type": "13F-HR",
        "dateb": end_date,
        "owner": "include",
        "count": "100"
    }
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')
    filings = []
    
    for link in soup.find_all('a', {'id': 'documentsbutton'}):
        href = link.get('href')
        filing_url = f"https://www.sec.gov{href}"
        filings.append(filing_url)
    
    return filings
