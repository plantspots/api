from django.urls import path
from api.views import Login, CreateAccount, RequestData, HomeData

urlpatterns = [
    path("login", Login.as_view(), name="login-view"),
    path("create-account", CreateAccount.as_view(), name="create-account-view"),
    path("requests", RequestData.as_view(), name="request-data-view"),
    path("home", HomeData.as_view(), name="home-data-view"),
]