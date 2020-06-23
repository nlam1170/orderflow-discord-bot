import asyncio
import rapidjson
import requests

async def get_basis():
    cw = rapidjson.loads(requests.get("https://api.hbdm.com/index/market/history/basis?symbol=BTC_CW&period=1min&size=1&basis_price_type=open").text)
    nw = rapidjson.loads(requests.get("https://api.hbdm.com/index/market/history/basis?symbol=BTC_NW&period=1min&size=1&basis_price_type=open").text)
    cq = rapidjson.loads(requests.get("https://api.hbdm.com/index/market/history/basis?symbol=BTC_CQ&period=1min&size=1&basis_price_type=open").text)
    
    cwb = (float(cw['data'][0]['basis_rate'])*100)
    nwb = (float(nw['data'][0]['basis_rate'])*100)
    cqb = (float(cq['data'][0]['basis_rate'])*100)
    
    return [cwb,nwb,cqb]
