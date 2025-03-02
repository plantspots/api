from django.urls import path
from api.views import CloseRequestData, GetRequestData, Login, CreateAccount, RequestData, HomeData, OpenAIData, UpdateRequestData

urlpatterns = [
    path("login", Login.as_view(), name="login-view"),
    path("create-account", CreateAccount.as_view(), name="create-account-view"),
    path("requests", RequestData.as_view(), name="request-data-view"),
    path("get-request", GetRequestData.as_view(), name="get-request-data-view"),
    path("update-request", UpdateRequestData.as_view(), name="update-request-data-view"),
    path("close-request", CloseRequestData.as_view(), name="close-request-data-view"),
    path("home", HomeData.as_view(), name="home-data-view"),
    path("openai", OpenAIData.as_view(), name="open-ai-view"),
]