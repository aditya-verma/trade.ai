from datetime import datetime, timedelta

from django.contrib.auth.models import PermissionsMixin
from django.db import models

from trade_ai.base.models import TradeAIBaseModel

class BTC_USDT(TradeAIBaseModel):
    """Django model class to represent btc_usdt table.
    """

    timestamp = models.DateTimeField()
    open = models.FloatField(max_length=16, unique=True)
    close = models.FloatField(max_length=16, unique=True)
    low = models.FloatField(max_length=16, unique=True)
    high = models.FloatField(max_length=16, unique=True)
    volume = models.FloatField(max_length=16, unique=True)

    REQUIRED_FIELDS = ('timestamp', 'open', 'close', 'high', 'low', 'volume')

    def __str__(self):
        return f'{self.close}'
