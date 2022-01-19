import asyncio
import requests

from discord import Activity, ActivityType, Client, errors
from datetime import datetime as dt

################################################################################
token_name = 'dpx'
contract = token_name + '-ssov'
epoch = 3
epoch_end = '28-Jan'
################################################################################

################################################################################
# Your bot's token goes here. This can be found on the Discord developers
# portal.
################################################################################
BOT_TOKEN = ""
################################################################################

print(f"\n---------- V3 Flim's {contract.upper()} Discord Bot ----------\n")

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
                            f"https://api.dopex.io/api/v1/tvl?include={contract}"
                        )
            tvl = round(float(response.json()["tvl"])/1000000,2)
            print(f"{dt.utcnow()} | response status code: {response.status_code}.")
            print(f"{dt.utcnow()} | {contract} tvl: ${tvl:,}M.")
            for guild in client.guilds:
                try:
                    await guild.me.edit(nick=f"{token_name.upper()} ${tvl:,}M")
                    await client.change_presence(
                        activity=Activity(
                            name=f"Epoch: {epoch} | End: {epoch_end}", type=ActivityType.watching
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
