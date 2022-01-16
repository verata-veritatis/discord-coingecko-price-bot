import asyncio
import requests
import json
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from discord import Activity, ActivityType, Client, errors
from datetime import datetime as dt

################################################################################
# Your bot's token goes here. This can be found on the Discord developers
# portal.
################################################################################
BOT_TOKEN = ""
################################################################################
token_name = "bridgoor"
# token_name = "halloween"

print(f"\n---------- Flim's DPX {token_name.title()} Discord Bot ----------\n")
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

            site = f"https://tofunft.com/collection/dopex-{token_name}/items"
            hdr = {"User-Agent": "Mozilla/5.0"}
            req = Request(site, headers=hdr)
            page = urlopen(req)
            soup = BeautifulSoup(page, "html5lib")
            script = soup.find(id="__NEXT_DATA__").string
            json_data = json.loads(script)
            floor = json_data["props"]["pageProps"]["data"]["contract"]["stats"][
                "market_floor_price"
            ]
            vol = json_data["props"]["pageProps"]["data"]["contract"]["stats"][
                "market_vol"
            ]
            print(f"{dt.utcnow()} | floor: {floor}.")
            print(f"{dt.utcnow()} | volume: {vol}.")

            for guild in client.guilds:
                try:
                    await guild.me.edit(nick=f"{token_name.title()}: Ξ{floor}")
                    await client.change_presence(
                        activity=Activity(
                            name=f"Volume: Ξ{vol}",
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
            await asyncio.sleep(30)


################################################################################

################################################################################
# Run the client.
################################################################################
client.run(BOT_TOKEN)
################################################################################
