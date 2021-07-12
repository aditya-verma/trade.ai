from asgiref.sync import sync_to_async
from binance import ThreadedWebsocketManager
from trade_ai.btc_usdt.models import BTC_USDT
from django.conf import settings
import asyncio

from trade_ai.celery import app


@sync_to_async()
def handle_socket_message(msg):
    if msg["data"]["k"]["x"] is True:
        print(msg)
        BTC_USDT.objects.create(
            timestamp_open=msg["data"]["k"]["t"],
            timestamp_close=msg["data"]["k"]["T"],
            open=msg["data"]["k"]["o"],
            close=msg["data"]["k"]["c"],
            low=msg["data"]["k"]["l"],
            high=msg["data"]["k"]["h"],
            volume=msg["data"]["k"]["v"]
        )


def callback_func(msg):
    asyncio.create_task(handle_socket_message(msg))


@app.task()
def live_data():
    api_key = settings.BINANCE_API_KEY
    api_secret = settings.BINANCE_API_SECRET

    twm = ThreadedWebsocketManager(
        api_key=api_key,
        api_secret=api_secret
    )
    # start is required to initialise its internal loop
    twm.start()

    # twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)

    # multiple sockets can be started
    # twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)

    # or a multiplex socket can be started like this
    # see Binance docs for stream names
    streams = ['btcusdt@kline_1m', ]
    twm.start_multiplex_socket(
        callback=callback_func,
        streams=streams
    )

    twm.join()
