import asyncio
import requests
import json
import ssl
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from discord import Activity, ActivityType, Client, errors
from datetime import datetime as dt

################################################################################
token_name = "bridgoor"
# token_name = "halloween"
################################################################################


### Opensea
# r = requests.get(
#     # f"https://api.opensea.io/api/v1/collection/{attributes[i][0]}/stats"
#     f"https://api.opensea.io/api/v1/collection/boredapeyachtclub/"
# )
# temp = r.json()["collection"]["primary_asset_contracts"][0]["symbol"]
# print(temp)

### Dopex SSOV
# contract = "dpx-ssov"

# response = requests.get(
#                 f"https://api.dopex.io/api/v1/tvl?include={contract}"
#             )
# tvl = round(float(response.json()["tvl"])/1000000,2)

# print(f"{dt.utcnow()} | response: {response.json()}.")
# print(f"{dt.utcnow()} | response status code: {response.status_code}.")
# print(f"{dt.utcnow()} | {contract} tvl: ${tvl:,}M.")


### TofuNFT using urllib request
site = f"https://tofunft.com/collection/dopex-{token_name}/items"
hdr = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0"
}
context = ssl._create_unverified_context()
req = Request(site, headers=hdr)
page = urlopen(req, context=context)
print(page.getcode())
soup = BeautifulSoup(page, "html5lib")
script = soup.find(id="__NEXT_DATA__").string
json_data = json.loads(script)
floor_dict = json_data["props"]["pageProps"]["data"]["contract"]["stats"][
    "market_floor_price"
]

vol = json_data["props"]["pageProps"]["data"]["contract"]["stats"]["market_vol"]
floor = floor_dict.pop("0x0000000000000000000000000000000000000000")

print(f"{dt.utcnow()} | {token_name} floor: {floor}.")
print(f"{dt.utcnow()} | {token_name} volume: {vol}.")

### TofuNFT using requests

# hdr = {"User-Agent": "Mozilla/5.0"}
# r = requests.get(f"https://tofunft.com/collection/dopex-{token_name}/items")
# print(type(r))

# page = urlopen(r)
# soup = BeautifulSoup(page, "html5lib")
# script = soup.find(id="__NEXT_DATA__").string
# json_data = json.loads(script)
# floor_dict = json_data["props"]["pageProps"]["data"]["contract"]["stats"][
#     "market_floor_price"
# ]
# vol = json_data["props"]["pageProps"]["data"]["contract"]["stats"]["market_vol"]

# floor = floor_dict.pop("0x0000000000000000000000000000000000000000")

# print(f"{dt.utcnow()} | floor: {floor}.")
# print(f"{dt.utcnow()} | volume: {vol}.")
