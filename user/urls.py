from django.urls import path
from .views import RegisterView
from .views import CustomAuthToken


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='api_token_auth'),

]
