from trade_ai.accounts.viewsets import UserViewSet, MeViewSet
from trade_ai.base.routers import TradeAIBaseRouter


accounts_router_v1 = TradeAIBaseRouter()

accounts_router_v1.register(r'user', UserViewSet)
accounts_router_v1.register(r'me', MeViewSet)
