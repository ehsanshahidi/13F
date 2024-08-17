import datetime
from flask import Flask, jsonify
from sqlalchemy import create_engine
import pandas as pd
from backend.downloader import download_13f_filings
from backend.parser import parse_13f_filing, save_to_db

app = Flask(__name__)
engine = create_engine('sqlite:///13f_filings.db')

def main():
    cik = "0001166559"  # Example CIK
    end_date = datetime.datetime.now().strftime('%Y%m%d')
    start_date = (datetime.datetime.now() - datetime.timedelta(days=5*365)).strftime('%Y%m%d')
    filings = download_13f_filings(cik, start_date, end_date)
    
    for filing_url in filings:
        data = parse_13f_filing(filing_url)
        save_to_db(data)

@app.route('/api/filings', methods=['GET'])
def get_filings():
    query = "SELECT * FROM filings"
    data = pd.read_sql(query, engine)
    return jsonify(data.to_dict(orient='records'))

if __name__ == "__main__":
    main()
    app.run(debug=True)
