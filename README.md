# discord-coingecko-price-bot
Uses the CoinGecko API to actively display the price of a cryptocurrency via the nickname.

For python3.6+. You'll need `discord.py` and `requests`. The bot needs nickname-changing permissions.

![bots](https://i.ibb.co/9ZBfN6n/test-img.png)

Open the `bot.py` file and add your desired `MARKET_ID` and `BOT_TOKEN`. The bot token can be obtained from the Discord developer portal after making a new app. The market ID is obtained by going to the token's page on CoinGecko, and grabbing the last bit of the URL i.e. https://www.coingecko.com/en/coins/rope-token -> `MARKET_ID = rope_token`.

# bayc-opensea-floor-price-bot

No `MARKET_ID` necessary for this bot. Discord bot token still required. I didn't figure out how to query collections and get to BAYC but was able to do it using an address which I know owns a BAYC. There's probably a smarter way to do it without specifying 'asset_owner' but I'm n00b shadowy super coder. I'm learning. 

BAYC bot shows the floor price, and for "watching" displays the 7-day average price. All other requirements for this bot match the Coingecko Price bot. 

# crypto-punks-floor-price-bot

Dependencies: `requests` & `BeautifulSoup`. This bot uses BeautifulSoup to pull the CryptoPunks floor price from larvalabs.com/cryptopunks in ETH and USD. 

god bless
