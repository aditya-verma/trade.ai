"""
WSGI config for trade_ai project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from trade_ai import load_dotenv_local
from trade_ai.btc_usdt import tasks

# Start celery task
tasks.live_data.apply_async((), retry=False)


# Load .env on startup of WSGI server
load_dotenv_local()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
application = get_wsgi_application()
