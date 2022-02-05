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
    else:
        r = requests.get(f"https://api.coingecko.com/api/v3/coins/{attributes[i][0]}")
        token_name = r.json()["symbol"].upper()
    time.sleep(0.3)
    if r.status_code > 400:
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
                        f"{dt.utcnow()} | {tickers[i]} 7d avg. price: Ξ{round(pctchng,2)}\n."
                    )
                elif attributes[i][3] == "btc":
                    print(
                        f"{dt.utcnow()} | {tickers[i]}/{attributes[i][3].upper()}: ₿{price:,}."
                    )
                    print(
                        f"{dt.utcnow()} | {tickers[i]} 24hr % change: {round(pctchng,2)}%.\n"
                    )
                else:
                    print(f"{dt.utcnow()} | {tickers[i]} price: ${price:,}.")
                    print(
                        f"{dt.utcnow()} | {tickers[i]} 24hr % change: {round(pctchng,2)}%.\n"
                    )
                for guild in clients[i].guilds:
                    try:
                        # handle different logic for bot name
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
