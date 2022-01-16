import asyncio
import requests
import json
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from discord import Activity, ActivityType, Client, errors
from datetime import datetime as dt

print("\n---------- Flim's DPX Bridgoor Discord Bot ----------\n")

token_name = "bridgoor"
# token_name = "halloween"

site = f"https://tofunft.com/collection/dopex-{token_name}/items"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site, headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page, "html5lib")
script = soup.find(id="__NEXT_DATA__").string
json_data = json.loads(script)
floor = json_data['props']['pageProps']['data']['contract']['stats']['market_floor_price']
vol = json_data['props']['pageProps']['data']['contract']['stats']['market_vol']
print(floor)
print(vol)