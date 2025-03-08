from django.urls import path
from accounts.views.user_view import UserAPIViewSet
from accounts.views.chat_view import ChatbotView 

app_name = "accounts"

urlpatterns = [
    path('user/', UserAPIViewSet.as_view(), name='user-create'), 
    path('user/<str:uid>/', UserAPIViewSet.as_view(), name='user-detail'),  
    path('chatbot/<str:uid>/', ChatbotView.as_view(), name='chatbot-history'),
    path('chatbot/', ChatbotView.as_view(), name='chatbot-chat'),
]
