from django.contrib import admin

from trade_ai.base.admin import TradeAIBaseAdmin
from trade_ai.btc_usdt.models import BTC_USDT


@admin.register(BTC_USDT)
class BTCUSDTAdmin(TradeAIBaseAdmin):

	list_display = ('id', 'open', 'close')

	readonly_fields = (
		'created_at', 'modified_at',
		'timestamp_open', 'timestamp_close',
		'low', 'high', 'open',
		'close', 'volume'
	)

	fieldsets = (
		(None, {
			'fields': (('timestamp_open', 'timestamp_close'),)
		}),
		('Address Details', {
			'fields': ('low', 'high', 'open', 'close'),
			'classes': ('wide',)
		}),
		('History', {
			'fields': (
				'created_at',
				'modified_at',
				'delete_flag',
			)
		}),
	)
