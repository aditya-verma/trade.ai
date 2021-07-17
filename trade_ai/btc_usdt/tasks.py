from asgiref.sync import sync_to_async
from binance import ThreadedWebsocketManager
from trade_ai.btc_usdt.models import BTC_USDT
from django.conf import settings
import asyncio

from trade_ai.celery import app


@sync_to_async()
def add_kline_data_to_database(kline):
    """
    Adds candlestick data for a given timeframe from exchange to local database

    Args:
        kline: candlestick data for a given timeframe.

    Returns:
        None
    """
    if kline["data"]["k"]["x"] is True:
        if settings.DEBUG:
            print(kline)
        BTC_USDT.objects.create(
            timestamp_open=kline["data"]["k"]["t"],
            timestamp_close=kline["data"]["k"]["T"],
            open=kline["data"]["k"]["o"],
            close=kline["data"]["k"]["c"],
            low=kline["data"]["k"]["l"],
            high=kline["data"]["k"]["h"],
            volume=kline["data"]["k"]["v"]
        )


def callback_func(kline):
    asyncio.create_task(add_kline_data_to_database(kline))


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
