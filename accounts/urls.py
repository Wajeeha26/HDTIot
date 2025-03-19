from django.urls import path

from accounts.views.chat_view import ChatbotView
from accounts.views.payment_views import VerifySquarePaymentView
from accounts.views.user_view import UserAPIViewSet

app_name = "accounts"

urlpatterns = [
    path("user/", UserAPIViewSet.as_view(), name="user-create"),
    path("user/<str:uid>/", UserAPIViewSet.as_view(), name="user-detail"),
    path("chatbot/<str:uid>/", ChatbotView.as_view(), name="chatbot-history"),
    path("chatbot/", ChatbotView.as_view(), name="chatbot-chat"),
    path("verify-payment/", VerifySquarePaymentView.as_view(), name="verify-payment"),
]
