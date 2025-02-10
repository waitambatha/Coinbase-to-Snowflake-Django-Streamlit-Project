from django.urls import path
from .views import Level1Currencies, Level2Currencies, Level3Currencies, LoginAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name="api-login"),
    path('level1/currencies/', Level1Currencies.as_view(), name="level1-currencies"),
    path('level2/currencies/', Level2Currencies.as_view(), name="level2-currencies"),
    path('level3/currencies/', Level3Currencies.as_view(), name="level3-currencies"),
]
