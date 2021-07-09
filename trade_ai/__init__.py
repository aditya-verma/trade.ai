import os

from dotenv import load_dotenv


def load_dotenv_local():
    if os.environ.get('RATNASHREE_IS_DEBUG', True):
        load_dotenv(override=True)
    else:
        load_dotenv(dotenv_path='/etc/trade_ai/.env', override=True)
