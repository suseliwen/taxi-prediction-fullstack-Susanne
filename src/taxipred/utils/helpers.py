import requests
from urllib.parse import urljoin #En helper-funktion som hjälper oss att läsa olika endpoints


def read_api_endpoint(endpoint = "/", base_url = "http://127.0.0.1:8000/taxi"):
    url = urljoin(base_url, endpoint)
    response = requests.get(url)
    return response

# statisk valutakurs
FX_USDSEK = 11.05