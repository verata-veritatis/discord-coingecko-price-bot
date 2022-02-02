import asyncio
import requests
import tokens  # gitignore dictionary, holds CG API names & Discord API tokens
import time

from discord import Activity, ActivityType, Client, errors
from datetime import datetime as dt

################################################################################
# List of Market IDs goes here. This can be found by going to the token's page on
# CoinGecko ex. --> https://www.coingecko.com/en/coins/<id>.
################################################################################
MARKET_IDS = list(tokens.tokens_dict.keys())
print(MARKET_IDS)
################################################################################

print("\n---------- V4 Flim's DISCORD x COINGECKO BOT ----------\n")

################################################################################
# Sanity check for market IDs.
################################################################################
print(f"{dt.utcnow()} | Checking CoinGecko for market IDs.")
print(MARKET_IDS)
tickers = []

for i in range(len(MARKET_IDS)):
    r = requests.get(f"https://api.coingecko.com/api/v3/coins/{MARKET_IDS[i]}")
    if r.status_code > 400:
        print(f"{dt.utcnow()} | Could not find {MARKET_IDS[i]}. Exiting...\n")
        exit()
    else:
        token_name = r.json()["symbol"].upper()
        print(f"{dt.utcnow()} | Found {token_name}.")
        tickers.append(token_name)
        print(f"{dt.utcnow()} | Tickers {tickers}.")
    time.sleep(0.3)
################################################################################


################################################################################
# Your bot's token goes here. This can be found on the Discord developers
# portal.
################################################################################
# BOT_TOKEN = ""
# BOT_TOKEN = tokens.tokens_dict[MARKET_IDS]
################################################################################

################################################################################
# Start clients.
################################################################################
print(f"{dt.utcnow()} | Starting Discord bot army of {len(MARKET_IDS)}.")
clients = []

for i in range(len(MARKET_IDS)):
    clients.append(Client())
    print(f"{dt.utcnow()} | Started {MARKET_IDS[i]} bot.")
    time.sleep(0.3)
################################################################################

print(clients)

################################################################################
# Client's on_ready event function. We do everything here.
################################################################################
for i in range(len(clients)):
    client = clients[i]

    @client.event
    async def on_ready():
        errored_guilds = []
        print(f"{dt.utcnow()} | Discord client is running.\n")
        should_restart = True
        while should_restart:
            should_restart = False
            for i in range(len(clients)):
                try:
                    response = requests.get(
                        f"https://api.coingecko.com/api/v3/coins/{MARKET_IDS[i]}"
                    )
                    print(
                        f"{dt.utcnow()} | response status code: {response.status_code}."
                    )
                    price = response.json()["market_data"]["current_price"]["usd"]
                    print(f"{dt.utcnow()} | {tickers[i]} price: {price}.")
                    print(f"{dt.utcnow()} | client: {clients[i]}.")
                    # print(range(len(clients)))
                    # print(len(clients))
                    # print(i)
                    pctchng = response.json()["market_data"][
                        "price_change_percentage_24h_in_currency"
                    ]["usd"]
                    print(
                        f"{dt.utcnow()} | {tickers[i]} 24hr % change: {round(pctchng,2)}%."
                    )
                    for guild in client.guilds:
                        try:
                            await guild.me.edit(
                                nick=f"{tickers[i]} ${round(price,2):,}"
                            )
                            await client.change_presence(
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
                    await asyncio.sleep(5)
                if i + 1 == len(clients):
                    should_restart = True
                    break


################################################################################

################################################################################
# Run the clients.
################################################################################
for i in range(len(clients)):
    BOT_TOKEN = tokens.tokens_dict[MARKET_IDS[i]]
    clients[i].run(BOT_TOKEN)
    # client = clients[i]
    # print(client)

    time.sleep(0.3)
################################################################################
