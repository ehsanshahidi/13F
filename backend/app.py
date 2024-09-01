import datetime

import pandas as pd
from flask import Flask, jsonify, request
from sqlalchemy import create_engine

from backend.downloader import download_13f_filings, get_cik_by_fund_name
from backend.parser import parse_13f_filing, save_to_db

app = Flask(__name__)
engine = create_engine("sqlite:///13f_filings.db")


@app.route("/api/fetch-filings", methods=["POST"])
def fetch_filings():
    fund_name = request.json.get("fund_name")
    if not fund_name:
        return jsonify({"error": "Fund name is required"}), 400

    try:
        cik = get_cik_by_fund_name(fund_name)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    end_date = datetime.datetime.now().strftime("%Y%m%d")
    start_date = (datetime.datetime.now() - datetime.timedelta(days=5 * 365)).strftime(
        "%Y%m%d"
    )

    filings = download_13f_filings(cik, start_date, end_date)

    for filing_url in filings:
        data = parse_13f_filing(filing_url)
        save_to_db(data)

    return jsonify({"message": "13F filings fetched and saved successfully"}), 200


@app.route("/api/filings", methods=["GET"])
def get_filings():
    query = "SELECT * FROM filings"
    data = pd.read_sql(query, engine)
    return jsonify(data.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)
