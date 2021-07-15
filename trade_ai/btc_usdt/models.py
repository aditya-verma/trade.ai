from datetime import datetime, timedelta

from django.contrib.auth.models import PermissionsMixin
from django.db import models

from trade_ai.base.models import TradeAIBaseModel


class BTC_USDT(TradeAIBaseModel):
    """Django model class to represent btc_usdt table.
    """

    timestamp_open = models.CharField(max_length=16)
    timestamp_close = models.CharField(max_length=16)
    open = models.FloatField()
    close = models.FloatField()
    low = models.FloatField()
    high = models.FloatField()
    volume = models.FloatField()

    REQUIRED_FIELDS = (
        'timestamp', 'open',
        'close', 'high',
        'low', 'volume'
    )

    def __str__(self):
        if self.open < self.close:
            return 'Green'
        else:
            return 'Red'
