from django.urls import path
from .views import UserAPIViewSet

app_name = "accounts"

urlpatterns = [
    path('user/', UserAPIViewSet.as_view(), name='user-create'),  # For POST (Create User)
    path('user/<str:uid>/', UserAPIViewSet.as_view(), name='user-detail'),  # For GET, PUT, DELETE
]
