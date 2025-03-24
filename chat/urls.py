from django.urls import path
from chat.views.chat import ChatEndpoint, EpigeneticAgeEndpoint

app_name = "chat"

urlpatterns = [
    path('chat/', ChatEndpoint.as_view(), name='chat'),
    path('epigenetic-age/', EpigeneticAgeEndpoint.as_view(), name='epigenetic-age'),
]
