import asyncio
import requests
import ssl

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

from discord import Activity, ActivityType, Client, errors
from datetime import datetime as dt

################################################################################
# Your bot's token goes here. This can be found on the Discord developers
# portal.
################################################################################
BOT_TOKEN = ''
################################################################################

print('\n---------- Flim\'s Fidenza Discord Bot ----------\n')

ssl._create_default_https_context = ssl._create_unverified_context

token_name = 'Fidenza'
collection = 'art-blocks'

# token2 = 'Meridian'
# collection2 = 'art-blocks-playground'

hdr = {'User-Agent': 'Mozilla/5.0'}
url = (
    'https://opensea.io/assets/'
    + collection
    + '?search[sortAscending]=true&search[sortBy]=PRICE&search[stringTraits][0][name]='
    + token_name
    + '&search[stringTraits][0][values][0]=All%20'
    + token_name
    + 's'
)

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
            req = Request(url, headers=hdr)
            page = urlopen(req)
            soup = BeautifulSoup(page, 'html5lib')
            lowest = soup.findAll(
                'div',
                attrs={
                    'class': (
                        'Overflowreact__OverflowContainer-sc-10mm0lu-0 gjwKJf'
                        ' Price--amount'
                    )
                },
            )
            floor = lowest[0].text.strip()
            eth_floor = 'Ξ' + floor
            print(f'{dt.utcnow()} | {token_name} floor: {eth_floor}.')
            for guild in client.guilds:
                try:
                    await guild.me.edit(nick=f'{token_name} {eth_floor}')
                    await client.change_presence(
                        activity=Activity(
                            name=f'Opensea Floor', type=ActivityType.watching
                        )
                    )
                except errors.Forbidden:
                    if guild not in errored_guilds:
                        print(
                            f'{dt.utcnow()} | {guild}:{guild.id} hasn\'t set '
                            'nickname permissions for the bot!'
                        )
                    errored_guilds.append(guild)
                except Exception as e:
                    print(f'{dt.utcnow()} | Unknown error: {e}.')
        except requests.exceptions.HTTPError as e:
            print(f'{dt.utcnow()} | HTTP error: {e}.')
        except ValueError as e:
            print(f'{dt.utcnow()} | ValueError: {e}.')
        except TypeError as e:
            print(f'{dt.utcnow()} | TypeError: {e}.')
        finally:
            await asyncio.sleep(30)


################################################################################

################################################################################
# Run the client.
################################################################################
client.run(BOT_TOKEN)
################################################################################
