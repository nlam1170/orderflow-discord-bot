import aiohttp
import rapidjson
import asyncio

class MexCycle:
    def __init__(self, bitmex_funding=None, bitmex_oi=None, huboi_funding=None, huboi_oi=None):
        self.bitmex_funding = r"https://www.bitmex.com/api/v1/funding?symbol=XBTUSD&count=1&reverse=true"
        self.bitmex_oi = r"https://www.bitmex.com/api/v1/instrument?symbol=XBT%3Aperpetual&count=1&reverse=true"
        
        self.huboi_funding = r"https://api.btcgateway.pro/swap-api/v1/swap_funding_rate?&contract_code=BTC-USD"
        self.huboi_oi = r"https://api.btcgateway.pro/swap-api/v1/swap_open_interest?contract_code=BTC-USD"

    async def get_result(self, url):
        async with aiohttp.ClientSession(json_serialize=rapidjson.dumps) as session:
            async with session.get(url) as resp:
                data = await resp.json(loads=rapidjson.loads)
                return data
    
    async def get_bitmex_funding(self):
        data = await self.get_result(self.bitmex_funding)
        return data[0]["fundingRate"]

    async def get_bitmex_oi(self):
        data = await self.get_result(self.bitmex_oi)
        return data[0]["openInterest"]

    async def get_huboi_funding(self):
        async with aiohttp.ClientSession(json_serialize=rapidjson.dumps) as session:
            async with session.get(self.huboi_funding) as resp:
                data = await resp.read()
                data = rapidjson.loads(data)
                return data["data"]["funding_rate"]

    async def get_huboi_funding_estimate(self):
        async with aiohttp.ClientSession(json_serialize=rapidjson.dumps) as session:
            async with session.get(self.huboi_funding) as resp:
                data = await resp.read()
                data = rapidjson.loads(data)
                return data["data"]["estimated_rate"]

    async def get_huboi_oi(self):
        async with aiohttp.ClientSession(json_serialize=rapidjson.dumps) as session:
            async with session.get(self.huboi_oi) as resp:
                data = await resp.read()
                data = rapidjson.loads(data)
                return data["data"][0]["volume"]


class OkexCycle:
    def __init__(self,okex_usd_funding=None,okex_usdt_funding=None,okex_usd_oi=None,okex_usdt_oi=None,
                 binance_funding=None,binance_oi=None,
                    bybit_usd=None,bybit_usdt=None):
        self.okex_usd_funding = r"https://www.okex.com/api/swap/v3/instruments/BTC-USD-SWAP/funding_time"
        self.okex_usd_oi = r"https://www.okex.com/api/swap/v3/instruments/BTC-USD-SWAP/open_interest"
        
        self.okex_usdt_funding = r"https://www.okex.com/api/swap/v3/instruments/BTC-USDT-SWAP/funding_time"
        self.okex_usdt_oi = r"https://www.okex.com/api/swap/v3/instruments/BTC-USDT-SWAP/open_interest"

        self.binance_funding = r"https://fapi.binance.com/fapi/v1/fundingRate?limit=1&symbol=BTCUSDT"
        self.binance_oi = r"https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT"

        self.bybit_usd = r"https://api.bybit.com/v2/public/tickers?symbol=BTCUSD"
        self.bybit_usdt = r"https://api.bybit.com/v2/public/tickers?symbol=BTCUSDT"

    async def get_result(self, url):
        async with aiohttp.ClientSession(json_serialize=rapidjson.dumps) as session:
            async with session.get(url) as resp:
                data = await resp.json(loads=rapidjson.loads)
                return data

    async def get_okex_usd_funding(self):
        data = await self.get_result(self.okex_usd_funding)
        return data["funding_rate"]

    async def get_okex_usd_funding_estimate(self):
        data = await self.get_result(self.okex_usd_funding)
        return data["estimated_rate"]

    async def get_okex_usdt_funding(self):
        data = await self.get_result(self.okex_usdt_funding)
        return data["funding_rate"]

    async def get_okex_usdt_funding_estimate(self):
        data = await self.get_result(self.okex_usdt_funding)
        return data["estimated_rate"]

    async def get_okex_usd_oi(self):
        data = await self.get_result(self.okex_usd_oi)
        return data["amount"]

    async def get_okex_usdt_oi(self):
        data = await self.get_result(self.okex_usdt_oi)
        return data["amount"]

    async def get_binance_funding(self):
        data = await self.get_result(self.binance_funding)
        return data[0]["fundingRate"]

    async def get_binance_oi(self):
        data = await self.get_result(self.binance_oi)
        return data["openInterest"]

    async def get_bybit_usd_funding(self):
        data = await self.get_result(self.bybit_usd)
        return data["result"][0]["funding_rate"]

    async def get_bybit_usd_funding_estimate(self):
        data = await self.get_result(self.bybit_usd)
        return data["result"][0]["predicted_funding_rate"]

    async def get_bybit_usdt_funding(self):
        data = await self.get_result(self.bybit_usdt)
        return data["result"][0]["funding_rate"]

    async def get_bybit_usdt_funding_estimate(self):
        data = await self.get_result(self.bybit_usdt)
        return data["result"][0]["predicted_funding_rate"]

    async def get_bybit_usd_oi(self):
        data = await self.get_result(self.bybit_usd)
        return data["result"][0]["open_interest"]

    async def get_bybit_usdt_oi(self):
        data = await self.get_result(self.bybit_usdt)
        return data["result"][0]["open_interest"]
