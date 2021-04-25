# discord-coingecko-price-bot
Uses the CoinGecko API to actively display the price of a cryptocurrency via the nickname.

For python3.6+. You'll need `discord.py` and `requests`.

![bots](https://i.ibb.co/9ZBfN6n/test-img.png)

Open the `bot.py` file and add your desired `MARKET_ID` and `BOT_TOKEN`. The bot token can be obtained from the Discord developer portal after making a new app. The market ID is obtained by going to the token's page on CoinGecko, and grabbing the last bit of the URL i.e. https://www.coingecko.com/en/coins/rope-token -> `MARKET_ID = rope_token`.
