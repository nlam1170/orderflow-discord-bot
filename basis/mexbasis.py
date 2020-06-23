import aiohttp
import rapidjson
import asyncio

async def get_contracts_marks():
    contracts= []
    marks = []
    url = r"https://www.bitmex.com/api/v1/instrument/activeAndIndices"
    async with aiohttp.ClientSession(json_serialize=rapidjson.dumps) as session:
        async with session.get(url) as resp:
            resp = await resp.json(loads=rapidjson.loads)
    
    for i in resp:
        if i["symbol"] != "XBTUSD" and i["rootSymbol"] == "XBT" and i["settlCurrency"] == "XBt":
            contracts.append(i["symbol"])
            marks.append(i["markPrice"])
    
    return contracts, marks

async def get_contracts_basis():
    contracts, marks = await get_contracts_marks()
    index_url = r"https://www.bitmex.com/api/v1/instrument?symbol=.BXBT&count=1&reverse=true"
    basis = []

    async with aiohttp.ClientSession(json_serialize=rapidjson.dumps) as session:
        async with session.get(index_url) as resp:
            resp = await resp.json(loads=rapidjson.loads)
            index = resp[0]["markPrice"]

    for i in range(len(contracts)):
        diff = (float(marks[i]) - float(index)) / float(index) * 100
        basis.append(diff)

    return contracts,basis

