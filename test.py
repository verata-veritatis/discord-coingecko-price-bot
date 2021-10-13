import asyncio
import requests
import ssl

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

from discord import (
    Activity,
    ActivityType,
    Client,
    errors,
)
from datetime import datetime as dt

ssl._create_default_https_context = ssl._create_unverified_context

name = 'Fidenza'
collection = 'art-blocks'
hdr = {'User-Agent': 'Mozilla/5.0'}
url = 'https://opensea.io/assets/'+collection+'?search[sortAscending]=true&search[sortBy]=PRICE&search[stringTraits][0][name]='+name+'&search[stringTraits][0][values][0]=All%20'+name+'s'

req = Request(url, headers=hdr)
# req = requests.get(url, headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page, 'html5lib')
lowest = soup.findAll('div', attrs = {'class':'Overflowreact__OverflowContainer-sc-10mm0lu-0 gjwKJf Price--amount'})
floor = lowest[0]
            
print(f'{dt.utcnow()} | floor is: {floor}.')