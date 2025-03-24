import logging
from openapi_schema_validator import validate
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

from user.api_schema.signup import SIGNUP_API
from user.models import User
from utilities.response_utils import handle_api_exception

from rest_framework.response import Response

logger = logging.getLogger(__name__)

import logging
from openapi_schema_validator import validate
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from user.api_schema.signup import SIGNUP_API
from user.models import User
from utilities.response_utils import handle_api_exception

logger = logging.getLogger(__name__)

class CreateUserAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [JSONParser]  # Ensure JSON parsing

    """
    Sign up user in the system
    """

    def get_post_request_data(self, request):
        # ✅ Include 'uid' in the extracted data
        return (
            request.data.get("uid", ""),
            request.data.get("email", ""),
            request.data.get("first_name", ""),
            request.data.get("last_name", ""),
            request.data.get("user_type", 1),
            request.data.get("is_deleted", 0),
        )

    def post(self, request):
        (uid, email, first_name, last_name, user_type, is_deleted) = self.get_post_request_data(request)

        try:
            # ✅ Convert boolean to integer for 'is_deleted' if necessary
            request_data = request.data.copy()
            if isinstance(request_data.get("is_deleted"), bool):
                request_data["is_deleted"] = int(request_data["is_deleted"])

            validate(request_data, SIGNUP_API.get("POST").get("schema"))

            # ✅ Pass all required fields to create_user()
            _ = User.objects.create_user(
                uid=uid,
                email=email,
                first_name=first_name,
                last_name=last_name,
                user_type=user_type,
                is_deleted=is_deleted
            )

            return Response(
                {"status": "success", "message": "User created successfully"},
                status=status.HTTP_201_CREATED
            )

        except ValidationError as e:
            return handle_api_exception(
                e, status.HTTP_400_BAD_REQUEST, "Invalid request", request, logger
            )

        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return handle_api_exception(
                e,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Internal Server Error",
                request.data,
                logger,
            )
