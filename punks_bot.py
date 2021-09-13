import requests
from bs4 import BeautifulSoup

URL = "https://www.larvalabs.com/cryptopunks"
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib

# print(soup.prettify())
# punk_stats = []

punk_stats = soup.findAll('div', attrs = {'class':'col-md-4 punk-stat'})

# print(punk_stats[0])
# print(punk_stats[0].text)
# for index, stat in enumerate(punk_stats):
# 	print(punk_stats[index].text)

floor = punk_stats[0].b

split = floor.string.split(' ETH ')

eth_floor = 'Ξ'+split[0]
usd_floor = split[1].lstrip('(').rstrip(' USD)')

# print(floor.string)
# print(split)
print(eth_floor)
print(usd_floor)

# print(punk_stats.prettify())