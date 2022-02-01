import asyncio
import requests

from discord import Activity, ActivityType, Client, errors
from datetime import datetime as dt

################################################################################
# Your bot's token goes here. This can be found on the Discord developers
# portal.
################################################################################
BOT_TOKEN = ""
################################################################################
ticker = "MAYC"
collection = "mutant-ape-yacht-club"
print(f"\n---------- Flim's {ticker} Discord Bot ----------\n")

url = f"https://api.opensea.io/api/v1/collection/{collection}/stats"
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
            response = requests.request("GET", url)
            floor_price = response.json()["stats"]["floor_price"]
            pctchng = response.json()["stats"]["seven_day_average_price"]
            print(f"{dt.utcnow()} | response status code: {response.status_code}.")
            print(f"{dt.utcnow()} | {ticker} floor price: Ξ{floor_price}.")
            print(f"{dt.utcnow()} | {ticker} 7d avg. price: Ξ{round(pctchng,2)}.")
            for guild in client.guilds:
                try:
                    await guild.me.edit(nick=f"{ticker} Ξ{round(floor_price,2):,}")
                    await client.change_presence(
                        activity=Activity(
                            name=f"7d avg.: Ξ{round(pctchng,2)}",
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
        except requests.exceptions.HTTPError as e:
            print(f"{dt.utcnow()} | HTTP error: {e}.")
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
