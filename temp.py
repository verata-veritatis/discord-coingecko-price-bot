import asyncio
import requests  # pip install requests

# import cfscrape
from bs4 import BeautifulSoup  # pip install beatifulsoup4
import pandas as pd  # pip install pandas

from discord import Activity, ActivityType, Client, errors
from datetime import datetime as dt

print("\n---------- Flim's DPX Bridgoor Discord Bot ----------\n")

token_name = "bridgoor"
# token_name = "halloween"

url = f"https://tofunft.com/collection/dopex-{token_name}/items"

tables = pd.read_html(url)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.contetn, "html.parser")

print(soup)

# scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
# # Or: scraper = cfscrape.CloudflareScraper()  # CloudflareScraper inherits from requests.Session
# soup = scraper.get(
#     f"https://tofunft.com/collection/dopex-{token_name}/items"
# ).content  # => "<!DOCTYPE html><html><head>..."

# print(soup)

# response = requests.get(f"https://tofunft.com/collection/dopex-{token_name}/items")
# print(f"{dt.utcnow()} | response status code: {response.status_code}.")
# soup = BeautifulSoup(
#     response.content, "html5lib"
# )  # If this line causes an error, run 'pip install html5lib' or install html5lib

# print(soup)

# blocks = soup.find("span", attrs={"id": "blockCount"})
# block_stats = blocks.attrs["title"].split("Blocks (")[1]
# b_prop = block_stats.split(", ")[0].split(": ")
# b_miss = block_stats.split(", ")[1].split(": ")
# b_orph = block_stats.split(", ")[2].split(": ")
# b_sche = block_stats.split(", ")[3].split(": ")

# print(f"{dt.utcnow()} | blocks: {block_stats}.")
# print(f"{dt.utcnow()} | b_prop: {b_prop}.")
