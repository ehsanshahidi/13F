import requests
from bs4 import BeautifulSoup


def get_cik_by_fund_name(fund_name):
    search_url = f"https://www.sec.gov/cgi-bin/browse-edgar?company={fund_name}&owner=exclude&action=getcompany"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, "html.parser")

    cik = None
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) > 0 and "CIK" in cells[0].text:
            cik = cells[1].text.strip()
            break

    if cik:
        return cik
    else:
        raise ValueError(f"No CIK found for fund name: {fund_name}")


def download_13f_filings(cik, start_date, end_date):
    base_url = "https://www.sec.gov/cgi-bin/browse-edgar"
    params = {
        "action": "getcompany",
        "CIK": cik,
        "type": "13F-HR",
        "dateb": end_date,
        "owner": "include",
        "count": "100",
    }
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.content, "html.parser")
    filings = []

    for link in soup.find_all("a", {"id": "documentsbutton"}):
        href = link.get("href")
        filing_url = f"https://www.sec.gov{href}"
        filings.append(filing_url)

    return filings
