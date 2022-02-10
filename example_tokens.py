################################################################################
# flim.eth
# twitter.com/0xflim
# 0xflim@pm.me
# if this is helpful to you, please consider donating:
# 0x8d6fc57487ade3738c2baf3437b63d35420db74d (or flim.eth)
#
# This is a gitignore file (tokens.py) which contains a simple dictionary:
#
# Values represent Discord API tokens
# Token info here: https://discord.com/developers/docs/topics/oauth2#bots
#
# Keys represent a list of attributes including for example coingecko market id:
# ex. --> https://www.coingecko.com/en/coins/<id>.
#
# You will need to add Discord bot API keys & rename this file to `tokens.py`
# 
# I store them both in lists here:
################################################################################

`tokens_dict = {
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
    ],
    # punks
    "anotherapikeyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy": [
        "punk",
        "larvalabs",
        "floor_price",
        "eth",
    ],
    # dopexapi
    "anotherapikeyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy": [
        "dpx-ssov",
        "dopexapi",
        "tvl",
        "usd",
    ],
    # dopexnft
    "anotherapikeyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy": [
        "bridgoor",
        "dopexnft",
        "floor_price",
        "eth",
    ],
    # etherscan gas
    "anotherapikeyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy": [
        "gas",
        "etherscan",
        "C67HPZF2EPRQ36IKWRDPMZEW5R1ZFYWQUW",
        "gas",
    ],
    # validator
    "anotherapikeyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy": [
        "195271",
        "beaconchain",
        "flimnode",
        "gas",
    ],
}`
