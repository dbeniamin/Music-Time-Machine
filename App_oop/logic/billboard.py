import requests
from bs4 import BeautifulSoup


def get_songs(date: str):
    url = f"https://www.billboard.com/charts/hot-100/{date}/"
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/91.0.4472.124 Safari/537.36'
        )
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Could not fetch Billboard data for {date}")

    soup = BeautifulSoup(response.text, "html.parser")
    titles = [h3.get_text(strip=True) for h3 in soup.select("li ul li h3")]

    if not titles:
        raise Exception("No songs found. Try a different date.")

    return titles[:100]  # ensure max 100 songs