# contas/urls.py

from django.urls import path
from .views import *
from .views import CookieTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('send-mail/', send_mail_view, name='send_mail'),

    # JWT com cookies
    path('token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
