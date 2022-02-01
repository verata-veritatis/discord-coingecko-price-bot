import asyncio
import requests

from discord import Activity, ActivityType, Client, errors
from datetime import datetime as dt

################################################################################
# Market ID goes here. This can be found by going to the token's page on
# CoinGecko ex. --> https://www.coingecko.com/en/coins/<id>.
################################################################################
MARKET_ID = "bitcoin"
################################################################################

################################################################################
# Your bot's token goes here. This can be found on the Discord developers
# portal.
################################################################################
BOT_TOKEN = ""
################################################################################

print("\n---------- V3 DISCORD x COINGECKO BOT ----------\n")

################################################################################
# Sanity check for market ID.
################################################################################
print(f"{dt.utcnow()} | Checking CoinGecko for market ID.")
r = requests.get(f"https://api.coingecko.com/api/v3/coins/{MARKET_ID}")
if r.status_code > 400:
    print(f"{dt.utcnow()} | Could not find market. Exiting...\n")
    exit()
else:
    token_name = r.json()["symbol"].upper()
    print(f"{dt.utcnow()} | Found {token_name}.")
################################################################################

################################################################################
# Start client.
################################################################################
print(f"{dt.utcnow()} | Starting Discord client.")
client = Client()
################################################################################


################################################################################
# Client's on_ready event function. We do everything here.
################################################################################
@client.event
async def on_ready():
    errored_guilds = []
    print(f"{dt.utcnow()} | Discord client is running.\n")
    while True:
        try:
            response = requests.get(
                f"https://api.coingecko.com/api/v3/coins/{MARKET_ID}"
            )
            print(f"{dt.utcnow()} | response status code: {response.status_code}.")
            price = response.json()["market_data"]["current_price"]["usd"]
            print(f"{dt.utcnow()} | {token_name} price: {price}.")
            pctchng = response.json()["market_data"][
                "price_change_percentage_24h_in_currency"
            ]["usd"]
            print(f"{dt.utcnow()} | {token_name} 24hr % change: {round(pctchng,2)}%.")
            for guild in client.guilds:
                try:
                    await guild.me.edit(nick=f"{token_name} ${round(price,2):,}")
                    await client.change_presence(
                        activity=Activity(
                            name=f"24h: {round(pctchng,2)}%", type=ActivityType.watching
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
            await asyncio.sleep(60)


################################################################################

################################################################################
# Run the client.
################################################################################
client.run(BOT_TOKEN)
################################################################################
