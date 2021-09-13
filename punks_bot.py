import asyncio
import requests
from bs4 import BeautifulSoup

from discord import (
    Activity,
    ActivityType,
    Client,
    errors,
)
from datetime import datetime as dt

################################################################################
# Your bot's token goes here. This can be found on the Discord developers
# portal.
################################################################################
BOT_TOKEN = ''
################################################################################

print('\n---------- Flim\'s CryptoPunks Discord Bot ----------\n')

token_name = 'PUNK'

################################################################################
# Start client.
################################################################################
print(f'{dt.utcnow()} | Starting Discord client.')
client = Client()
################################################################################


################################################################################
# Client's on_ready event function. We do everything here.
################################################################################
@client.event
async def on_ready():
    errored_guilds = []
    print(f'{dt.utcnow()} | Discord client is running.\n')
    while True:
        try:
            response = requests.get(f'https://www.larvalabs.com/cryptopunks')
            print(f'{dt.utcnow()} | response status code: {response.status_code}.')
            soup = BeautifulSoup(response.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
            punk_stats = soup.findAll('div', attrs = {'class':'col-md-4 punk-stat'})
            
            # in case we want to get other stats, we iterate through all punk stats here
            # for index, stat in enumerate(punk_stats):
            #   print(punk_stats[index].text)
            
            floor = punk_stats[0].b
            split = floor.string.split(' ETH ')
            eth_floor = 'Ξ'+split[0]
            usd_floor = split[1].lstrip('(').rstrip(' USD)')
            print(f'{dt.utcnow()} | {token_name} floor: {eth_floor}.')
            print(f'{dt.utcnow()} | {token_name} floor: {usd_floor}.')
            for guild in client.guilds:
                try:
                    await guild.me.edit(
                        nick=f'{token_name} {eth_floor}'
                    )
                    await client.change_presence(
                        activity=Activity(
                            name=f'in USD: {usd_floor}',
                            type=ActivityType.watching,
                        ),
                    )
                except errors.Forbidden:
                    if guild not in errored_guilds:
                        print(f'{dt.utcnow()} | {guild}:{guild.id} hasn\'t set '
                              f'nickname permissions for the bot!')
                    errored_guilds.append(guild)
                except Exception as e:
                    print(f'{dt.utcnow()} | Unknown error: {e}.')
        except requests.exceptions.HTTPError as e:
            print(f'{dt.utcnow()} | HTTP error: {e}.')
        except ValueError:
            print(f'{dt.utcnow()} | ValueError due to {response.status_code}. Waiting: {response.headers["Retry-After"]}.')
            await asyncio.sleep(response.headers["Retry-After"])
        finally:
            await asyncio.sleep(30)
################################################################################

################################################################################
# Run the client.
################################################################################
client.run(BOT_TOKEN)
################################################################################
