import asyncio
import requests
import json
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from discord import Activity, ActivityType, Client, errors
from datetime import datetime as dt

################################################################################
# token_name = "bridgoor"
# token_name = "halloween"
################################################################################

contract = 'dpx-ssov'

response = requests.get(
                f"https://api.dopex.io/api/v1/tvl?include={contract}"
            )
tvl = round(float(response.json()["tvl"])/1000000,2)

print(f"{dt.utcnow()} | response: {response.json()}.")
print(f"{dt.utcnow()} | response status code: {response.status_code}.")
print(f"{dt.utcnow()} | {contract} tvl: ${tvl:,}M.")

# site = f"https://tofunft.com/collection/dopex-{token_name}/items"
# hdr = {"User-Agent": "Mozilla/5.0"}
# req = Request(site, headers=hdr)
# page = urlopen(req)
# soup = BeautifulSoup(page, "html5lib")
# script = soup.find(id="__NEXT_DATA__").string
# json_data = json.loads(script)
# floor_dict = json_data["props"]["pageProps"]["data"]["contract"]["stats"][
#     "market_floor_price"
# ]
# vol = json_data["props"]["pageProps"]["data"]["contract"]["stats"][
#     "market_vol"
# ]

# floor = floor_dict.pop('0x0000000000000000000000000000000000000000')

# print(f"{dt.utcnow()} | floor: {floor}.")
# print(f"{dt.utcnow()} | volume: {vol}.")