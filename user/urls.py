from django.urls import path

from user.views.signup import CreateUserAPIView
from user.views.user import UserAPIViewSet

app_name = "user"

urlpatterns = [
    path("signup/", CreateUserAPIView.as_view(), name="signup"),
    path("user/", UserAPIViewSet.as_view(), name="user"),
    path(
        "organizations/", OrganizationAPIView.as_view(), name="organization-list-create"
    ),
    path(
        "organizations/<int:pk>/",
        OrganizationAPIView.as_view(),
        name="organization-detail",
    ),
]
