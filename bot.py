import asyncio
import requests

from discord import (
    Activity,
    ActivityType,
    Client,
    errors,
)
from datetime import datetime as dt

################################################################################
# Market ID goes here. This can be found by going to the token's page on
# CoinGecko ex. --> https://www.coingecko.com/en/coins/<id>.
################################################################################
MARKET_ID = 'ADD YOUR ID HERE'
################################################################################

################################################################################
# Your bot's token goes here. This can be found on the Discord developers
# portal.
################################################################################
BOT_TOKEN = 'ADD YOUR TOKEN HERE'
################################################################################

print('\n---------- V² DISCORD x COINGECKO BOT ----------\n')

################################################################################
# Sanity check for market ID.
################################################################################
print(f'{dt.utcnow()} | Checking CoinGecko for market ID.')
r = requests.get(f'https://api.coingecko.com/api/v3/coins/{MARKET_ID}')
if r.status_code > 400:
    print(f'{dt.utcnow()} | Could not find market. Exiting...\n')
    exit()
else:
    token_name = r.json()['symbol'].upper()
    print(f'{dt.utcnow()} | Found {token_name}.')
################################################################################

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
    await client.change_presence(
        activity=Activity(
            name=f'{token_name}/USD on CoinGecko',
            type=ActivityType.watching,
        ),
    )
    print(f'{dt.utcnow()} | Discord client is running.\n')
    while True:
        try:
            price = requests.get(
                f'https://api.coingecko.com/api/v3/coins/{MARKET_ID}'
            ).json()['market_data']['current_price']['usd']
            for guild in client.guilds:
                try:
                    await guild.me.edit(
                        nick=f'{token_name} ${round(float(price), 2)}'
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
        finally:
            await asyncio.sleep(30)
################################################################################

################################################################################
# Run the client.
################################################################################
client.run(BOT_TOKEN)
################################################################################
