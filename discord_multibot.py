################################################################################
# originally forked from
# https://github.com/verata-veritatis/discord-coingecko-price-bot
#
# rebuilt & refactored with <3 by:
# flim.eth
#
# questions? reach out
# twitter.com/0xflim
# 0xflim@pm.me
#
# if this is helpful to you, please consider donating:
# 0x8d6fc57487ade3738c2baf3437b63d35420db74d (or flim.eth)
################################################################################
import asyncio
import requests
import tokens  # gitignore dictionary, holds CG API names & Discord API tokens
import time
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

from discord import Activity, ActivityType, Client, errors
from datetime import datetime as dt

################################################################################
# I keep a gitignore file (tokens.py) which contains a simple dictionary:
#
# Values represent Discord API tokens
# Token info here: https://discord.com/developers/docs/topics/oauth2#bots
#
# Keys represent a list of attributes including for example coingecko market id:
# ex. --> https://www.coingecko.com/en/coins/<id>.
#
# I store them both in lists here:
################################################################################
bot_tokens = list(tokens.tokens_dict.keys())
attributes = list(tokens.tokens_dict.values())
################################################################################

print("\n---------- V5 flim.eth's Discord Multibot ----------\n")

################################################################################
# Sanity check for APIs.
################################################################################
print(f"{dt.utcnow()} | Checking CoinGecko & Opensea for market IDs.")
tickers = []

for i in range(len(bot_tokens)):
    if attributes[i][1] == "opensea":
        r = requests.get(
            f"https://api.opensea.io/api/v1/collection/{attributes[i][0]}/"
        )
        token_name = r.json()["collection"]["primary_asset_contracts"][0][
            "symbol"
        ].upper()
    elif attributes[i][1] == "larvalabs":
        r = requests.get(f"https://www.larvalabs.com/cryptopunks")
        token_name = attributes[i][0].upper()
    elif attributes[i][1] == "dopexnft":
        hdr = {"User-Agent": "Mozilla/5.0"}
        site = f"https://tofunft.com/collection/dopex-{attributes[i][0]}/items"
        r = Request(site, headers=hdr)
        token_name = attributes[i][0].upper()
    elif attributes[i][1] == "dopexapi":
        r = requests.get(f"https://api.dopex.io/api/v1/tvl?include={attributes[i][0]}")
        temp = attributes[i][0].split("-")
        token_name = temp[0].upper()
    else:
        r = requests.get(f"https://api.coingecko.com/api/v3/coins/{attributes[i][0]}")
        token_name = r.json()["symbol"].upper()
    time.sleep(0.3)
    if attributes[i][1] == "dopexnft":
        print(
            f"{dt.utcnow()} | Skipping {token_name}/{attributes[i][3].upper()} check."
        )
        tickers.append(token_name)
    elif r.status_code > 400:
        print(r.status_code)
        print(f"{dt.utcnow()} | Could not find {attributes[i][0]}. Exiting...\n")
        exit()
    else:
        print(f"{dt.utcnow()} | Found {token_name}/{attributes[i][3].upper()}.")
        tickers.append(token_name)
################################################################################
# Start clients.
################################################################################
print(f"\n{dt.utcnow()} | Starting Discord bot army of {len(bot_tokens)}.\n")
clients = []

for i in range(len(bot_tokens)):
    clients.append(Client())
################################################################################
# Client's on_ready event function. We do everything here.
################################################################################
client = clients[i]


@client.event
async def on_ready():
    errored_guilds = []
    print(f"{dt.utcnow()} | Multibot is running.\n")
    while True:
        for i in range(len(clients)):
            try:
                # pick which operation / API
                if attributes[i][1] == "opensea":
                    response = requests.get(
                        f"https://api.opensea.io/api/v1/collection/{attributes[i][0]}/stats"
                    )
                elif attributes[i][1] == "larvalabs":
                    response = requests.get(f"https://www.larvalabs.com/cryptopunks")
                elif attributes[i][1] == "dopexnft":
                    response = Request(site, headers=hdr)
                elif attributes[i][1] == "dopexapi":
                    response = requests.get(
                        f"https://api.dopex.io/api/v1/tvl?include={attributes[i][0]}"
                    )
                else:
                    response = requests.get(
                        f"https://api.coingecko.com/api/v3/coins/{attributes[i][0]}"
                    )
                # handle for different use cases
                if attributes[i][2] == "market_cap":
                    price = response.json()["market_data"][attributes[i][2]][
                        attributes[i][3]
                    ]
                    pctchng = response.json()["market_data"]["fully_diluted_valuation"][
                        attributes[i][3]
                    ]
                elif attributes[i][1] == "opensea":
                    floor_price = response.json()["stats"][attributes[i][2]]
                    pctchng = response.json()["stats"]["seven_day_average_price"]
                elif attributes[i][1] == "larvalabs":
                    soup = BeautifulSoup(
                        response.content, "html5lib"
                    )  # If this line causes an error, run 'pip install html5lib' or install html5lib
                    punk_stats = soup.findAll(
                        "div", attrs={"class": "col-md-4 punk-stat"}
                    )
                    floor = punk_stats[0].b
                    split = floor.string.split(" ETH ")
                    eth_floor = "Ξ" + split[0]
                    usd_floor = split[1].lstrip("(").rstrip(" USD)")
                elif attributes[i][1] == "dopexnft":
                    page = urlopen(response)
                    soup = BeautifulSoup(page, "html5lib")
                    script = soup.find(id="__NEXT_DATA__").string
                    json_data = json.loads(script)
                    floor_dict = json_data["props"]["pageProps"]["data"]["contract"][
                        "stats"
                    ]["market_floor_price"]
                    vol = json_data["props"]["pageProps"]["data"]["contract"]["stats"][
                        "market_vol"
                    ]
                    floor = floor_dict.pop("0x0000000000000000000000000000000000000000")
                elif attributes[i][1] == "dopexapi":
                    tvl = round(float(response.json()[attributes[i][2]]) / 1000000, 2)
                    epoch = 4
                    epoch_month = "Feb 2022"
                else:
                    price = response.json()["market_data"][attributes[i][2]][
                        attributes[i][3]
                    ]
                    pctchng = response.json()["market_data"][
                        "price_change_percentage_24h_in_currency"
                    ][attributes[i][3]]
                # print status code
                print(f"{dt.utcnow()} | response status code: {response.status_code}.")
                # console printing logic
                if attributes[i][2] == "market_cap":
                    print(f"{dt.utcnow()} | {tickers[i]} Mcap: ${price:,}.")
                    print(f"{dt.utcnow()} | JONES FDV: ${pctchng:,}.\n")
                elif attributes[i][1] == "opensea":
                    print(f"{dt.utcnow()} | {tickers[i]} floor price: Ξ{floor_price}.")
                    print(
                        f"{dt.utcnow()} | {tickers[i]} 7d avg. price: Ξ{round(pctchng,2)}.\n"
                    )
                elif attributes[i][3] == "btc":
                    print(
                        f"{dt.utcnow()} | {tickers[i]}/{attributes[i][3].upper()}: ₿{price:,}."
                    )
                    print(
                        f"{dt.utcnow()} | {tickers[i]} 24hr % change: {round(pctchng,2)}%.\n"
                    )
                elif attributes[i][1] == "larvalabs":
                    print(f"{dt.utcnow()} | {tickers[i]} floor: {eth_floor}.")
                    print(f"{dt.utcnow()} | {tickers[i]} floor: {usd_floor}.\n")
                elif attributes[i][1] == "dopexnft":
                    print(f"{dt.utcnow()} | bridgoor floor: {floor}.")
                    print(f"{dt.utcnow()} | volume: {vol}.\n")
                elif attributes[i][1] == "dopexapi":
                    print(f"{dt.utcnow()} | {attributes[i][0]} tvl: ${tvl:,}M.")
                    print(
                        f"{dt.utcnow()} | {attributes[i][0]} epoch: {epoch} | {epoch_month}.\n"
                    )
                else:
                    print(f"{dt.utcnow()} | {tickers[i]} price: ${price:,}.")
                    print(
                        f"{dt.utcnow()} | {tickers[i]} 24hr % change: {round(pctchng,2)}%.\n"
                    )
                for guild in clients[i].guilds:
                    try:
                        # handle different logic
                        if attributes[i][3] == "btc":
                            await guild.me.edit(
                                nick=f"{tickers[i]}/{attributes[i][3].upper()} ₿{round(float(price), 4)}"
                            )
                        elif attributes[i][2] == "market_cap":
                            await guild.me.edit(nick=f"Mcap ${round(price,2):,}")
                        elif attributes[i][1] == "opensea":
                            await guild.me.edit(
                                nick=f"{tickers[i]} Ξ{round(floor_price,2):,}"
                            )
                        elif attributes[i][1] == "larvalabs":
                            await guild.me.edit(nick=f"{tickers[i]} {eth_floor}")
                        elif attributes[i][1] == "dopexnft":
                            # await guild.me.edit(nick=f"{token_name.title()}: Ξ{floor}")
                            await guild.me.edit(nick=f"{tickers[i]}: Ξ{floor}")
                        elif attributes[i][1] == "dopexapi":
                            await guild.me.edit(nick=f"{tickers[i]} ${tvl:,}M")
                        elif price < 1:
                            await guild.me.edit(
                                nick=f"{tickers[i]} ${round(price,4):,}"
                            )
                        else:
                            await guild.me.edit(
                                nick=f"{tickers[i]} ${round(price,2):,}"
                            )
                        # handle different logic for bot activity
                        if attributes[i][2] == "market_cap":
                            await clients[i].change_presence(
                                activity=Activity(
                                    name=f"FDV: ${round(pctchng,2):,}",
                                    type=ActivityType.watching,
                                )
                            )
                        elif attributes[i][1] == "opensea":
                            await clients[i].change_presence(
                                activity=Activity(
                                    name=f"7d avg.: Ξ{round(pctchng,2)}",
                                    type=ActivityType.watching,
                                )
                            )
                        elif attributes[i][1] == "larvalabs":
                            await clients[i].change_presence(
                                activity=Activity(
                                    name=f"in USD: {usd_floor}",
                                    type=ActivityType.watching,
                                )
                            )
                        elif attributes[i][1] == "dopexnft":
                            await clients[i].change_presence(
                                activity=Activity(
                                    name=f"Volume: Ξ{vol}",
                                    type=ActivityType.watching,
                                )
                            )
                        elif attributes[i][1] == "dopexapi":
                            await clients[i].change_presence(
                                activity=Activity(
                                    name=f"Epoch: {epoch} | {epoch_month}",
                                    type=ActivityType.watching,
                                )
                            )
                        else:
                            await clients[i].change_presence(
                                activity=Activity(
                                    name=f"24h: {round(pctchng,2)}%",
                                    type=ActivityType.watching,
                                )
                            )
                    except errors.Forbidden:
                        if guild not in errored_guilds:
                            print(
                                f"{dt.utcnow()} | {guild}:{guild.id} hasn't set "
                                "nickname permissions for the bot!"
                            )
                        errored_guilds.append(guild)
                    except Exception as e:
                        print(f"{dt.utcnow()} | Unknown error: {e}.")
            except ValueError as e:
                print(f"{dt.utcnow()} | ValueError: {e}.")
            except TypeError as e:
                print(f"{dt.utcnow()} | TypeError: {e}.")
            except OSError as e:
                print(f"{dt.utcnow()} | OSError: {e}.")
            except Exception as e:
                print(f"{dt.utcnow()} | Unknown error: {e}.")
            finally:
                await asyncio.sleep(3)


################################################################################
# Run the clients.
################################################################################
loop = asyncio.get_event_loop()
for i in range(len(clients)):
    loop.create_task(clients[i].start(bot_tokens[i]))
loop.run_forever()
################################################################################
