import asyncio
import requests
import math

from discord import Activity, ActivityType, Client, errors
from datetime import datetime as dt

################################################################################
# Your bot's token & Etherscan API Key go here.
################################################################################
BOT_TOKEN = ""
apikey = ""
################################################################################

print("\n---------- Flim's Etherscan Gas Bot ----------\n")

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
            r = requests.get(
                "https://api.etherscan.io/api"
                "?module=gastracke"
                "r&action=gasorac"
                f"le&apikey={apikey}"
            )

            # parse response
            fastGas = int(r.json()["result"]["FastGasPrice"])
            rawSuggestedBase = r.json()["result"]["suggestBaseFee"]
            suggestedBase = math.floor(float(r.json()["result"]["suggestBaseFee"]))

            # check values
            print(f"{dt.utcnow()} | status code: {r.status_code}.")
            print(f"{dt.utcnow()} | suggested base fee: {suggestedBase}.")
            print(f"{dt.utcnow()} | fast gas: {fastGas}.")

            # convert gwei to wei
            fastGasWei = fastGas * 1e9
            print(f"{dt.utcnow()} | fast gas wei : {fastGasWei}.")

            # get priority fees
            fastPriority = fastGas % suggestedBase
            print(f"{dt.utcnow()} | fast priority: {fastPriority}.")

            r2 = requests.get(
                "https://api.etherscan.io/api"
                "?module=gastracker"
                "&action=gasestimate"
                f"&gasprice={str(round(fastGasWei))}"
                f"&apikey={apikey}"
            )

            fastGasTime = r2.json()["result"]
            print(f"{dt.utcnow()} | fast gas confirmation in seconds: {fastGasTime}.")
            for guild in client.guilds:
                try:
                    await guild.me.edit(nick=f"{fastGas:,} gwei ~{fastGasTime} sec")
                    await client.change_presence(
                        activity=Activity(
                            # emoji=f'⛽',
                            name=f"Base: {suggestedBase} Priority: {fastPriority}",
                            # type=ActivityType.custom
                            # type=ActivityType.playing,
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
        except requests.exceptions.HTTPError as e:
            print(f"{dt.utcnow()} | HTTP error: {e}.")
        finally:
            await asyncio.sleep(60)


################################################################################

################################################################################
# Run the client.
################################################################################
client.run(BOT_TOKEN)
################################################################################
