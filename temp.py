import asyncio
import requests
from bs4 import BeautifulSoup

from discord import Activity, ActivityType, Client, errors
from datetime import datetime as dt


print("\n---------- Flim's DPX Bridgoor Discord Bot ----------\n")

token_name = "bridgoor"
# token_name = "halloween"

response = requests.get(f"https://tofunft.com/collection/dopex-{token_name}/items")
print(f"{dt.utcnow()} | response status code: {response.status_code}.")
soup = BeautifulSoup(
    response.content, "html5lib"
)  # If this line causes an error, run 'pip install html5lib' or install html5lib

print(soup)

# blocks = soup.find("span", attrs={"id": "blockCount"})
# block_stats = blocks.attrs["title"].split("Blocks (")[1]
# b_prop = block_stats.split(", ")[0].split(": ")
# b_miss = block_stats.split(", ")[1].split(": ")
# b_orph = block_stats.split(", ")[2].split(": ")
# b_sche = block_stats.split(", ")[3].split(": ")

# print(f"{dt.utcnow()} | blocks: {block_stats}.")
# print(f"{dt.utcnow()} | b_prop: {b_prop}.")
