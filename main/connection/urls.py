from .views import AccountView, webhook, AccountDetailView
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', AccountView.as_view(), name='account'),
    path('web',webhook, name='webhook'),
    path('account_detail',AccountDetailView.as_view(),name='account-detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

