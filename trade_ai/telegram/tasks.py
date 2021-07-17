from asgiref.sync import sync_to_async
from django.conf import settings
import requests

from trade_ai.celery import app


@app.task
def send_message(user_id: str, message: str) -> dict:
	"""
	Sends message from telegram bot to user ID

	Args:
		user_id: chat id of telegram group, channel or user.
		message: message that needs to be sent.

	Returns:
		A dictionary of json response from telegram api.
	"""
	url = 'https://api.telegram.org/bot' + str(settings.TELEGRAM_BOT_TOKEN) + \
		  '/sendMessage?chat_id=' + str(user_id) + \
		  '&text=' + str(message)
	return dict(requests.get(url).json())
