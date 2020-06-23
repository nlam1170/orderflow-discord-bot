import asyncio
import discord
import rapidjson
import requests
from ExchangeClasses import OkexCycle, MexCycle

client = discord.Client()
channel_id = 723559287116267610
token = "NzIzNTU4MzY1MjYzMDM2NDI4.XuzYyA.BTc4m4fXVOlM4RSOm1r5wWWjNHQ"

mex = MexCycle()
okex = OkexCycle()

def get_ratio():
    usd = r"https://www.okex.com/api/swap/v3/instruments/BTC-USD-SWAP/index"
    tether = r"https://www.okex.com/api/swap/v3/instruments/BTC-USDT-SWAP/index"

    resp_usd = rapidjson.loads(requests.get(usd).text)
    resp_tehter = rapidjson.loads(requests.get(tether).text)

    return float (resp_tehter["index"]) / float(resp_usd["index"])

@client.event
async def on_ready():
    print("connected")

@client.event
async def on_message(message):
    channel = client.get_channel(channel_id)
    if message.author == client.user:
       return

    if message.content.startswith("$mexcycle"):
        mex_msg = F"__**Bitmex**__\n"\
        F"Funding:`{await mex.get_bitmex_funding()}`\n"\
        F"oi:`{await mex.get_bitmex_oi()}`"
        
        huboi_msg = F"\n__**Huboi**__\n"\
            F"Funding:`{await mex.get_huboi_funding()}`\n"\
            F"Funding Estimate:`{await mex.get_huboi_funding_estimate()}\n`"\
            F"oi:`{await mex.get_huboi_oi()}`"    
                
        await channel.send(mex_msg+huboi_msg)

    if message.content.startswith("$okcycle"):
        okex_usd_msg = F"__**Okex USD**__\n"\
            F"Funding:`{await okex.get_okex_usd_funding()}`\n"\
            F"Funding Estimate:`{await okex.get_okex_usd_funding_estimate()}`\n"\
            F"oi:`{await okex.get_okex_usd_oi()}\n`"

        okex_usdt_msg = F"__**Okex USDT**__\n"\
            F"Funding:`{await okex.get_okex_usdt_funding()}`\n"\
            F"Funding Estimate:`{await okex.get_okex_usdt_funding_estimate()}`\n"\
            F"oi:`{await okex.get_okex_usdt_oi()}\n`"

        binance_msg = F"__**Binance USD**__\n"\
            F"Funding:`{await okex.get_binance_funding()}`\n"\
            F"oi:`{await okex.get_binance_oi()}`\n"

        bybit_usd_msg = F"__**Bybit USD**__\n"\
            F"Funding:`{await okex.get_bybit_usd_funding()}`\n"\
            F"Funding Estimate:`{await okex.get_bybit_usd_funding_estimate()}`\n"\
            F"oi:`{await okex.get_bybit_usd_oi()}\n`"

        bybit_usdt_msg = F"__**Bybit USDT**__\n"\
            F"Funding:`{await okex.get_bybit_usdt_funding()}`\n"\
            F"Funding Estimate:`{await okex.get_bybit_usdt_funding_estimate()}`\n"\
            F"oi:`{await okex.get_bybit_usdt_oi()}\n`"

        
    
        await channel.send(okex_usd_msg+okex_usdt_msg+binance_msg+bybit_usd_msg+bybit_usdt_msg)

    if message.content.startswith("$ratio"):
        ratio = get_ratio()
        await channel.send("Tether/USD ratio:`"+str(ratio)+"`")

        




client.run(token)