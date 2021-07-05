"""trade_ai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from trade_ai.base.routers import RatnashreeBaseRouter
from trade_ai.accounts.routers import accounts_router_v1
from trade_ai.addresses.routers import addresses_router_v1
from trade_ai.products.routers import products_router_v1

trade_ai_base_router_v1 = RatnashreeBaseRouter()

trade_ai_base_router_v1.extend(accounts_router_v1)
trade_ai_base_router_v1.extend(addresses_router_v1)
trade_ai_base_router_v1.extend(products_router_v1)


urlpatterns = [
    path('trade_ai_admin/', admin.site.urls),
    path('api/v1/', include(trade_ai_base_router_v1.urls)),
]
