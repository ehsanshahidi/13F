import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine

def parse_13f_filing(filing_url):
    response = requests.get(filing_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Example logic to extract relevant data from the filing
    data = []
    # Parse the filing to extract data
    return pd.DataFrame(data)

def save_to_db(data, db_url='sqlite:///13f_filings.db'):
    engine = create_engine(db_url)
    data.to_sql('filings', engine, if_exists='append', index=False)
