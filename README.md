# discord_multibot
I have refactored by bots into a single "multibot" which takes as input a dictionary of 
Discord Tokens (keys) and bot attributes (market_it, api, data point, currency). This data sits in a .gitignored file called `tokens.py` which lives in the same folder as my multibot script. You will see a file called `example_tokens.py` which you can add discord tokens and rename to `tokens.py` 

This is the structure of that file:
```
tokens_dict = {
    # coingecko
    "apikeyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy": [
        "dopex",
        "coingecko",
        "current_price",
        "usd",
    ],
	# opensea
    "anotherapikeyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy": [
        "boredapeyachtclub",
        "opensea",
        "floor_price",
        "eth",
    ],}
```

## dependencies
[beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
```
pip install beautifulsoup4
```

[discord.py](https://pypi.org/project/discord.py/)
```
pip install discord.py
```

Other referenced libaries:
``` 
asyncio.py
requests.py
tokens.py (this is the file mentioned above)
time.py
ssl.py
json.py
Request.py
urlopen.py
datetime.py
requests.py
math.py
```
The multibot needs nickname-changing permissions.

For example to utilize Coingecko, open the `tokens.py` file and add your `discord_token` along with your `market_id` (dopex), your `api` (coingecko), `data_point` (current_price), and `currency` (usd). Please note, my script currently only handles `usd` or `btc` as currency inputs, as well as `current_price` or `market_cap` as data point inputs. 

The bot token can be obtained from the Discord developer portal after making a new app. 

The market ID is obtained by going to the token's page on CoinGecko, locating `API id`. Please note the API id is sometimes the same as the URL i.e. https://www.coingecko.com/en/coins/dopex -> `MARKET_ID = dopex`. But not always, as is the case with BTRFLY: https://www.coingecko.com/en/coins/redacted-cartel -- API id = butterflydao

## how it works

The multibot will do a quick API call for each token in the tokens.py dictionary. If the market isn't found, or a 403 error is returned, the multibot will notify via console and exit. If all sanity checks pass, the multibot will then start up all the bots in discord, and then update price procedurally stepping through each discort bot, one every 3 seconds. The multibot will also print its fetched data points to the console.

## footnotes

originally forked from
https://github.com/verata-veritatis/discord-coingecko-price-bot

rebuilt & refactored with <3 by:
flim.eth

questions? reach out
https://twitter.com/0xflim
0xflim@pm.me

if this is helpful to you, please consider donating:
0x8d6fc57487ade3738c2baf3437b63d35420db74d (or flim.eth)

god bless