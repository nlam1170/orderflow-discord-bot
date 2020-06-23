import asyncio
import aiohttp
import ssl
import rapidjson
import requests

okex_usd = r"https://www.okex.com/api/swap/v3/instruments/BTC-USD-SWAP/index"
okex_usdt = r"https://www.okex.com/api/swap/v3/instruments/BTC-USDT-SWAP/index"

async def get_contracts():
    instruments = r"https://www.okex.com/api/futures/v3/instruments"
    contracts = []

    async with aiohttp.ClientSession(json_serialize=rapidjson.dumps) as session:
        async with session.get(instruments) as resp:
            resp = await resp.json(loads=rapidjson.loads)

    for i in resp:
        if i['underlying_index'] == 'BTC':
            contracts.append(i['instrument_id'])

    return contracts

async def get_mark_price(contracts):
    mark = []
    for contract in contracts:
        url = url = "https://www.okex.com/api/futures/v3/instruments/%s/mark_price" % contract

        async with aiohttp.ClientSession(json_serialize=rapidjson.dumps) as session:
            async with session.get(url) as resp:
                resp = await resp.json(loads=rapidjson.loads)
                mark.append(resp['mark_price'])
    
    return mark

async def get_contracts_basis():
    contracts = await get_contracts()
    marks = await get_mark_price(contracts)
    basis = []

    async with aiohttp.ClientSession(json_serialize=rapidjson.dumps) as session:
        async with session.get(okex_usd) as resp:
            resp = await resp.json(loads=rapidjson.loads)
            usd = resp["index"]

    async with aiohttp.ClientSession(json_serialize=rapidjson.dumps) as session:
        async with session.get(okex_usdt) as resp:
            resp = await resp.json(loads=rapidjson.loads)
            usdt = resp["index"]

    for i in range(len(contracts)):
        if contracts[i][3] == "-":
            diff = (float(marks[i]) - float(usd)) / float(usd) * 100
            basis.append(diff)
        if contracts[i][3] == "T":
            diff = (float(marks[i]) - float(usdt)) / float(usdt) * 100
            basis.append(diff)

    return contracts, basis

