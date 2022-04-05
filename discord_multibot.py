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
import tokens  # gitignore dictionary, holds Discord API tokens & attributes
import time
import ssl
import json
import math

# import logging

# if __name__ == "__main__":
#     logging.basicConfig(
#         level=logging.DEBUG,
#         filename="logfile",
#         filemode="a+",
#         format="%(levelname)-8s %(message)s",
#     )

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
# API & response code sanity check; also create list of tickers
################################################################################
print(f"{dt.utcnow()} | Checking CoinGecko & Opensea for market IDs.")
logging.info(f"{dt.utcnow()} | Checking CoinGecko & Opensea for market IDs.")
tickers = []
status_code = 0

for i in range(len(bot_tokens)):
    if attributes[i][1] == "opensea":
        r = requests.get(
            f"https://api.opensea.io/api/v1/collection/{attributes[i][0]}/"
        )
        token_name = r.json()["collection"]["primary_asset_contracts"][0][
            "symbol"
        ].upper()
        status_code = r.status_code
    elif attributes[i][1] == "larvalabs":
        r = requests.get(f"https://www.larvalabs.com/cryptopunks")
        token_name = attributes[i][0].upper()
        status_code = r.status_code
    elif attributes[i][1] == "tofunft":
        hdr = {"User-Agent": "Mozilla/5.0"}
        site = f"https://tofunft.com/collection/{attributes[i][0]}/items"
        context = ssl._create_unverified_context()
        r = Request(site, headers=hdr)
        page = urlopen(r, context=context)
        token_name = attributes[i][2].title()
        status_code = page.getcode()
    elif attributes[i][1] == "dopexapi":
        r = requests.get(f"https://api.dopex.io/api/v1/tvl?include={attributes[i][0]}")
        temp = attributes[i][0].split("-")
        token_name = temp[0].upper()
        status_code = r.status_code
    elif attributes[i][1] == "beaconchain":
        r = requests.get(f"https://beaconcha.in/validator/{attributes[i][0]}")
        token_name = attributes[i][2].upper()
        status_code = r.status_code
    elif attributes[i][0] == "gas":
        r = requests.get(
            "https://api.etherscan.io/api"
            "?module=gastracke"
            "r&action=gasorac"
            f"le&apikey={attributes[i][2]}"
        )
        token_name = attributes[i][0].upper()
        status_code = r.status_code
    elif attributes[i][1] == "defillama":
        r = requests.get(f"https://api.llama.fi/{attributes[i][2]}/{attributes[i][0]}")
        token_name = attributes[i][2].upper()
    else:
        r = requests.get(f"https://api.coingecko.com/api/v3/coins/{attributes[i][0]}")
        token_name = r.json()["symbol"].upper()
        status_code = r.status_code
    time.sleep(0.3)
    if status_code > 400:
        print(r.status_code)
        # logging.info(r.status_code)
        print(f"{dt.utcnow()} | Could not find {attributes[i][0]}. Exiting...\n")
        # logging.info(f"{dt.utcnow()} | Could not find {attributes[i][0]}. Exiting...\n")
        exit()
    else:
        print(f"{dt.utcnow()} | Found {token_name}/{attributes[i][3].upper()}.")
        # logging.info(f"{dt.utcnow()} | Found {token_name}/{attributes[i][3].upper()}.")
        tickers.append(token_name)
################################################################################
# Start clients.
################################################################################
print(f"\n{dt.utcnow()} | Starting Discord bot army of {len(bot_tokens)}.\n")
# logging.info(f"\n{dt.utcnow()} | Starting Discord bot army of {len(bot_tokens)}.\n")
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
    # logging.info(f"{dt.utcnow()} | Multibot is running.\n")
    while True:
        for i in range(len(clients)):
            try:
                # pick which operation / API
                if attributes[i][1] == "opensea":
                    r = requests.get(
                        f"https://api.opensea.io/api/v1/collection/{attributes[i][0]}/stats"
                    )
                    status_code = r.status_code
                elif attributes[i][1] == "defillama":
                    r = requests.get(
                        f"https://api.llama.fi/{attributes[i][2]}/{attributes[i][0]}"
                    )
                    status_code = r.status_code
                elif attributes[i][1] == "larvalabs":
                    r = requests.get(f"https://www.larvalabs.com/cryptopunks")
                    status_code = r.status_code
                elif attributes[i][1] == "beaconchain":
                    r = requests.get(
                        f"https://beaconcha.in/validator/{attributes[i][0]}"
                    )
                    status_code = r.status_code
                elif attributes[i][1] == "tofunft":
                    site = f"https://tofunft.com/collection/{attributes[i][0]}/items"
                    r = Request(site, headers=hdr)
                    page = urlopen(r, context=context)
                    status_code = page.getcode()
                elif attributes[i][1] == "dopexapi":
                    r = requests.get(
                        f"https://api.dopex.io/api/v1/tvl?include={attributes[i][0]}"
                    )
                    status_code = r.status_code
                elif attributes[i][1] == "etherscan":
                    r = requests.get(
                        "https://api.etherscan.io/api"
                        "?module=gastracke"
                        "r&action=gasorac"
                        f"le&apikey={attributes[i][2]}"
                    )
                    fastGas = int(r.json()["result"]["FastGasPrice"])
                    rawSuggestedBase = r.json()["result"]["suggestBaseFee"]
                    suggestedBase = math.floor(
                        float(r.json()["result"]["suggestBaseFee"])
                    )

                    # convert gwei to wei
                    fastGasWei = fastGas * 1e9

                    # get priority fees
                    fastPriority = fastGas % suggestedBase
                else:
                    r = requests.get(
                        f"https://api.coingecko.com/api/v3/coins/{attributes[i][0]}"
                    )
                    status_code = r.status_code
                # handle for different use cases
                if attributes[i][2] == "market_cap":
                    price = r.json()["market_data"][attributes[i][2]][attributes[i][3]]
                    pctchng = r.json()["market_data"]["fully_diluted_valuation"][
                        attributes[i][3]
                    ]
                elif attributes[i][1] == "defillama":
                    tvl = r.json()
                elif attributes[i][1] == "opensea":
                    floor_price = r.json()["stats"][attributes[i][2]]
                    pctchng = r.json()["stats"]["seven_day_average_price"]
                elif attributes[i][1] == "larvalabs":
                    soup = BeautifulSoup(
                        r.content, "html5lib"
                    )  # If this line causes an error, run 'pip install html5lib' or install html5lib
                    punk_stats = soup.findAll(
                        "div", attrs={"class": "col-md-4 punk-stat"}
                    )
                    floor = punk_stats[0].b
                    split = floor.string.split(" ETH ")
                    eth_floor = "Ξ" + split[0]
                    usd_floor = split[1].lstrip("(").rstrip(" USD)")
                elif attributes[i][1] == "beaconchain":
                    soup = BeautifulSoup(
                        r.content, "html5lib"
                    )  # If this line causes an error, run 'pip install html5lib' or install html5lib

                    blocks = soup.find("span", attrs={"id": "blockCount"})
                    block_stats = blocks.attrs["title"].split("Blocks (")[1]
                    b_prop = block_stats.split(", ")[0].split(": ")
                    b_miss = block_stats.split(", ")[1].split(": ")
                    b_orph = block_stats.split(", ")[2].split(": ")
                    b_sche = block_stats.split(", ")[3].split(": ")

                    attestations = soup.find("span", attrs={"id": "attestationCount"})
                    attestation_stats = attestations.attrs["title"].split(
                        "Attestation Assignments ("
                    )[1]
                    a_exec = attestation_stats.split(", ")[0].split(": ")
                    a_miss = attestation_stats.split(", ")[1].split(": ")
                    a_orph = attestation_stats.split(", ")[2].split(": ")
                elif attributes[i][1] == "tofunft":
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
                    tvl = round(float(r.json()[attributes[i][2]]) / 1000000, 2)
                    # per witherblock these values should be added to Dopex API, but not yet
                    epoch = attributes[i][4]
                    epoch_month = attributes[i][5]
                elif attributes[i][1] == "etherscan":
                    r2 = requests.get(
                        "https://api.etherscan.io/api"
                        "?module=gastracker"
                        "&action=gasestimate"
                        f"&gasprice={str(round(fastGasWei))}"
                        f"&apikey={attributes[i][2]}"
                    )

                    fastGasTime = r2.json()["result"]
                    status_code = r2.status_code
                else:
                    price = r.json()["market_data"][attributes[i][2]][attributes[i][3]]
                    pctchng = r.json()["market_data"][
                        "price_change_percentage_24h_in_currency"
                    ][attributes[i][3]]

                # print status code & bot number
                print(f"{dt.utcnow()} | Discord bot: {i+1} of {len(bot_tokens)}.")
                print(f"{dt.utcnow()} | response status code: {status_code}.")
                # logging.info(
                #     f"{dt.utcnow()} | Discord bot: {i+1} of {len(bot_tokens)}."
                # )
                # logging.info(f"{dt.utcnow()} | response status code: {status_code}.")

                # console printing logic
                consolePrint = ""
                if attributes[i][2] == "market_cap":
                    consolePrint = (
                        f"{dt.utcnow()} | {tickers[i]} Mcap: ${price:,}.\n"
                        f"{dt.utcnow()} | JONES FDV: ${pctchng:,}.\n"
                    )
                elif attributes[i][1] == "defillama":
                    consolePrint = (
                        f"{dt.utcnow()} | {attributes[i][0]} {tickers[i]}: ${tvl:,}m.\n"
                    )
                elif attributes[i][1] == "opensea":
                    consolePrint = (
                        f"{dt.utcnow()} | {tickers[i]} floor price: Ξ{floor_price}.\n"
                        f"{dt.utcnow()} | {tickers[i]} 7d avg. price: Ξ{round(pctchng,2)}.\n"
                    )
                elif attributes[i][3] == "btc":
                    consolePrint = (
                        f"{dt.utcnow()} | {tickers[i]}/{attributes[i][3].upper()}: ₿{price:,}.\n"
                        f"{dt.utcnow()} | {tickers[i]} 24hr % change: {round(pctchng,2)}%.\n"
                    )
                elif attributes[i][1] == "larvalabs":
                    consolePrint = (
                        f"{dt.utcnow()} | {tickers[i]} floor: {eth_floor}.\n"
                        f"{dt.utcnow()} | {tickers[i]} floor: {usd_floor}.\n"
                    )
                elif attributes[i][1] == "beaconchain":
                    consolePrint = (
                        f"{dt.utcnow()} | blocks: {block_stats}.\n"
                        f"{dt.utcnow()} | attestations: {attestation_stats}.\n"
                    )
                elif attributes[i][1] == "tofunft":
                    consolePrint = (
                        f"{dt.utcnow()} | {tickers[i]} floor: Ξ{floor}.\n"
                        f"{dt.utcnow()} | {tickers[i]} volume: Ξ{vol}.\n"
                    )
                elif attributes[i][1] == "dopexapi":
                    consolePrint = (
                        f"{dt.utcnow()} | {tickers[i]} tvl: ${tvl:,}m.\n"
                        f"{dt.utcnow()} | {tickers[i]} epoch: {epoch} | {epoch_month}.\n"
                    )
                elif attributes[i][1] == "etherscan":
                    consolePrint = (
                        f"{dt.utcnow()} | status code: {r.status_code}.\n"
                        f"{dt.utcnow()} | suggested base fee: {suggestedBase}.\n"
                        f"{dt.utcnow()} | fast gas: {fastGas}.\n"
                        f"{dt.utcnow()} | fast gas wei : {fastGasWei}.\n"
                        f"{dt.utcnow()} | fast priority: {fastPriority}.\n"
                        f"{dt.utcnow()} | fast gas confirmation in seconds: {fastGasTime}.\n"
                    )
                else:
                    consolePrint = (
                        f"{dt.utcnow()} | {tickers[i]} price: ${price:,}.\n"
                        f"{dt.utcnow()} | {tickers[i]} 24hr % change: {round(pctchng,2)}%.\n"
                    )

                print(consolePrint)
                # logging.info(consolePrint)

                for guild in clients[i].guilds:
                    try:
                        # handle different logic for bot nicknaming & data display
                        if attributes[i][3] == "btc":
                            await guild.me.edit(
                                nick=f"{tickers[i]}/{attributes[i][3].upper()} ₿{round(float(price), 4)}"
                            )
                        elif attributes[i][1] == "defillama":
                            await guild.me.edit(nick=f"{tickers[i]} ${tvl:,}m")
                        elif attributes[i][2] == "market_cap":
                            await guild.me.edit(nick=f"MCAP ${price:,}m")
                        elif attributes[i][1] == "opensea":
                            await guild.me.edit(
                                nick=f"{tickers[i]} Ξ{round(floor_price,2):,}"
                            )
                        elif attributes[i][1] == "larvalabs":
                            await guild.me.edit(nick=f"{tickers[i]} {eth_floor}")
                        elif attributes[i][1] == "beaconchain":
                            await guild.me.edit(
                                nick=f"{tickers[i].lower()} blocks: {b_prop[1]}"
                            )
                        elif attributes[i][1] == "tofunft":
                            await guild.me.edit(nick=f"{tickers[i]}: Ξ{floor}")
                        elif attributes[i][1] == "dopexapi":
                            await guild.me.edit(nick=f"{tickers[i]} ${tvl:,}m")
                        elif attributes[i][1] == "etherscan":
                            await guild.me.edit(
                                nick=f"{fastGas:,} gwei ~{fastGasTime} sec"
                            )
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
                        elif attributes[i][1] == "beaconchain":
                            await clients[i].change_presence(
                                activity=Activity(
                                    name=f"attestations: {a_exec[1]}",
                                    type=ActivityType.watching,
                                )
                            )
                        elif attributes[i][1] == "tofunft":
                            await clients[i].change_presence(
                                activity=Activity(
                                    name=f"Volume: Ξ{vol}",
                                    type=ActivityType.watching,
                                )
                            )
                        elif attributes[i][1] == "defillama":
                            await clients[i].change_presence(
                                activity=Activity(
                                    name=f"Vaults",
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
                        elif attributes[i][1] == "etherscan":
                            await clients[i].change_presence(
                                activity=Activity(
                                    name=f"Base: {suggestedBase} Priority: {fastPriority}",
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
                            # logging.info(
                            #     f"{dt.utcnow()} | {guild}:{guild.id} hasn't set nickname permissions for the bot!"
                            # )
                        errored_guilds.append(guild)
                    except Exception as e:
                        print(f"{dt.utcnow()} | Unknown error: {e}.")
                        # logging.info(f"{dt.utcnow()} | Unknown error: {e}.")
            except ValueError as e:
                print(f"{dt.utcnow()} | ValueError: {e}.")
                # logging.info(f"{dt.utcnow()} | ValueError: {e}.")
            except TypeError as e:
                print(f"{dt.utcnow()} | TypeError: {e}.")
                # logging.info(f"{dt.utcnow()} | TypeError: {e}.")
            except OSError as e:
                print(f"{dt.utcnow()} | OSError: {e}.")
                # logging.info(f"{dt.utcnow()} | OSError: {e}.")
            except Exception as e:
                print(f"{dt.utcnow()} | Unknown error: {e}.")
                # logging.info(f"{dt.utcnow()} | Unknown error: {e}.")
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
