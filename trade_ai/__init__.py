import os

from dotenv import load_dotenv, __all__
from trade_ai.celery import app as celery_app


def load_dotenv_local():
    if os.environ.get('RATNASHREE_IS_DEBUG', True):
        load_dotenv(override=True)
    else:
        load_dotenv(dotenv_path='/etc/trade_ai/.env', override=True)


__all__ == ['celery_app']
