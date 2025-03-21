import logging

from openapi_schema_validator import validate
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from user.api_schema.signup import SIGNUP_API
from user.models import User
from utilities.response_utils import handle_api_exception

logger = logging.getLogger(__name__)


class CreateUserAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    """
    Sign up user in the system
    """

    def get_post_request_data(self, request):
        return (
            request.POST.get("email", ""),
            request.POST.get("first_name", ""),
            request.POST.get("last_name", ""),
        )

    def post(self, request):
        (email, first_name, last_name) = self.get_post_request_data(request)

        try:
            validate(request.body, SIGNUP_API.get("POST").get("schema"))

            # Create user
            _ = User.objects.create_user(
                email=email, first_name=first_name, last_name=last_name
            )

        except ValidationError as e:
            return handle_api_exception(
                e, status.HTTP_400_BAD_REQUEST, "Invalid request", request, logger
            )

        except Exception as e:
            return handle_api_exception(
                e,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Internal Server Error",
                request,
                logger,
            )
