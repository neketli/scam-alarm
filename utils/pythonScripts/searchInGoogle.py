import urllib
import requests
import argparse
import sys
import string
from bs4 import BeautifulSoup

index = 0 # ответ
parser = str(sys.argv[1])


try:
    if parser.find( 'www.')>-1:
        n = parser.find('www.')+4
        parser = parser[n:]


    if parser.find( '//')>-1:
        n = parser.find('//')+2
        parser = parser[n:]


    if parser.find( '/')>-1:
        n = parser.find('/')
        parser = parser[:n]




    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent

    query = str(parser)
    query = str( str(query.replace(' ', '+'))+"||")
    URL = f"https://google.com/search?q={query}"

    headers = {"user-agent": USER_AGENT}
    resp = requests.get(URL, headers=headers)


    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")

        for g in soup.find_all('div', class_='g'):
            divs = g.find_all('div',recursive=False)
            anchor = divs[0].find('a')
            link = anchor['href']

            if link.find(str(parser))>-1:
                index = 1


    print(index)

except Exception:
    print(1)
