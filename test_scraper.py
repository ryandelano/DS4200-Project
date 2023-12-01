from bs4 import BeautifulSoup as bs
import requests
import random as rnd

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"
]

header = {
    'User-Agent': rnd.choice(user_agents),
    'Accept-Language': 'en-US, en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8,*/*;q=0.7,*/*;q=0.5',
    'Referer': 'https://www.mass.gov',
    'DNT': '1'
}
# url = "https://masscannabiscontrol.com/open-data/data-catalog/"
# r = requests.get(url, headers=header)
# print(r.text)
contents = bs(requests.get("https://masscannabiscontrol.com/open-data/data-catalog/", headers=header).content, "html.parser", from_encoding="utf-8")

for strong in contents.find_all('strong'):
    print(strong.text)
