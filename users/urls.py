from django.urls import path
from users.views import RegisterView, LoginView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView #builtin so now coded
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh')
]


