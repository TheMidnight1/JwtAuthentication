from rest_framework_simplejwt.views import TokenRefreshView

from django.urls import path
from .views import user_registration, user_login,user_logout,get_user_from_access_token

urlpatterns = [
    path('register/', user_registration, name='user-registration'),
    path('login/', user_login, name='token-obtain-pair'),
     path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', get_user_from_access_token, name='get-user-from-access-token'),
    path('logout/', user_logout),
]
