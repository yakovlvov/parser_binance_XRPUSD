import asyncio
from binance.client import Client
from environs import Env


env = Env()
env.read_env()
api_token = env('BINANCE_API')
secret_key = env('SECRET_KEY')


def get_max_price(client, symbol, interval):
    klines = client.futures_klines(symbol=symbol, interval=interval)
    max_hour_price = 0
    for kline in klines:
        close_price = float(kline[4])
        if close_price > max_hour_price:
            max_hour_price = close_price
    return max_hour_price

async def main():
    client = Client(api_token, secret_key)
    max_price = get_max_price(client, "XRPUSDT", Client.KLINE_INTERVAL_1HOUR)
    while True:
        price = float(client.futures_ticker(symbol="XRPUSDT")['lastPrice'])
        if price > max_price:
            max_price = price
            print(max_price)
        if (max_price - price) / max_price >= 0.01:
            print("Price dropped by 1% from the maximum price")
        await asyncio.sleep(10)

asyncio.run(main())


