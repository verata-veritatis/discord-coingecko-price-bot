import asyncio
import requests
from bs4 import BeautifulSoup

from discord import Activity, ActivityType, Client, errors
from datetime import datetime as dt

################################################################################
# Your bot's token goes here. This can be found on the Discord developers
# portal.
################################################################################
BOT_TOKEN = ""
################################################################################

print("\n---------- Flim's ETH2 Validator Discord Bot ----------\n")

token_name = "flimnode"
val_id = "195271"

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

            response = requests.get(f"https://beaconcha.in/validator/{val_id}")
            print(f"{dt.utcnow()} | response status code: {response.status_code}.")
            soup = BeautifulSoup(
                response.content, "html5lib"
            )  # If this line causes an error, run 'pip install html5lib' or install html5lib

            blocks = soup.find("span", attrs={"id": "blockCount"})
            block_stats = blocks.attrs["title"].split("Blocks (")[1]
            b_prop = block_stats.split(", ")[0].split(": ")
            b_miss = block_stats.split(", ")[1].split(": ")
            b_orph = block_stats.split(", ")[2].split(": ")
            b_sche = block_stats.split(", ")[3].split(": ")

            print(f"{dt.utcnow()} | blocks: {block_stats}.")
            # print(f"{dt.utcnow()} | b_prop: {b_prop}.")

            attestations = soup.find("span", attrs={"id": "attestationCount"})
            attestation_stats = attestations.attrs["title"].split(
                "Attestation Assignments ("
            )[1]
            a_exec = attestation_stats.split(", ")[0].split(": ")
            a_miss = attestation_stats.split(", ")[1].split(": ")
            a_orph = attestation_stats.split(", ")[2].split(": ")

            print(f"{dt.utcnow()} | attestations: {attestation_stats}.")
            # print(f"{dt.utcnow()} | a_exec: {a_exec}.\n")

            for guild in client.guilds:
                try:
                    await guild.me.edit(nick=f"{token_name} blocks: {b_prop[1]}")
                    await client.change_presence(
                        activity=Activity(
                            name=f"attestations: {a_exec[1]}",
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
