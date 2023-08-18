from django.urls import path
from .consumers import *

wb_urlpatterns = [
    path("ws/<str:grpname>",MyCustomConsumer.as_asgi()),
    path("wt/<str:grpname>",CustomAsyncConsumer.as_asgi()),
]