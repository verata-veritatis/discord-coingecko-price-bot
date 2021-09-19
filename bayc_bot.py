import asyncio
import requests

from discord import Activity, ActivityType, Client, errors
from datetime import datetime as dt

################################################################################
# Your bot's token goes here. This can be found on the Discord developers
# portal.
################################################################################
BOT_TOKEN = ''
################################################################################

print('\n---------- Flim\'s BAYC Discord Bot ----------\n')

url = "https://api.opensea.io/api/v1/collections"
querystring = {
    "offset": "0",
    "asset_owner": "0x5b21175a82F112C88e306A546166037d238DE684",
}

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
            response = requests.request("GET", url, params=querystring)
            for index, primary_asset_contract in enumerate(response):
                if (
                    response.json()[index]['primary_asset_contracts'][0]['address']
                    == "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"
                ):
                    break
            floor_price = response.json()[index]['stats']['floor_price']
            address = response.json()[index]['primary_asset_contracts'][0]['address']
            name = response.json()[index]['name']
            token_name = response.json()[index]['primary_asset_contracts'][0]['symbol']
            pctchng = response.json()[index]['stats']['seven_day_average_price']

            # print(f'{dt.utcnow()} | index: {index}.')
            print(f'{dt.utcnow()} | response status code: {response.status_code}.')
            print(f'{dt.utcnow()} | {token_name} floor price: Ξ{floor_price}.')
            print(f'{dt.utcnow()} | {token_name} 7d avg. price: Ξ{round(pctchng,2)}.')
            for guild in client.guilds:
                try:
                    await guild.me.edit(nick=f'{token_name} Ξ{round(floor_price,2):,}')
                    await client.change_presence(
                        activity=Activity(
                            name=f'7d avg.: Ξ{round(pctchng,2)}',
                            type=ActivityType.watching,
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
        except simplejson.errors.JSONDecodeError as j:
            print(f'{dt.utcnow()} | JSONDecodeError: {j}.')
        except requests.exceptions.HTTPError as e:
            print(f'{dt.utcnow()} | HTTP error: {e}.')
        except ValueError:
            print(
                f'{dt.utcnow()} | ValueError due to '
                f'{response.status_code}. Waiting:'
                f' {response.headers["Retry-After"]}.'
            )
        except KeyError:
            print(
                f'{dt.utcnow()} | KeyError due to '
                f'{response.status_code}. Waiting:'
                f' {response.headers["Retry-After"]}.'
            )
            await asyncio.sleep(int(response.headers["Retry-After"]))
        except:
            print(f'{dt.utcnow()} | Something else happened. Pass.')
            pass
        finally:
            await asyncio.sleep(30)


################################################################################

################################################################################
# Run the client.
################################################################################
client.run(BOT_TOKEN)
################################################################################
