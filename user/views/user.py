import logging

from django.core.exceptions import ObjectDoesNotExist
from openapi_schema_validator import validate
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from user.api_schema.user_apiview import USER_API
from user.models.user import User
from utilities.log_utils import log_request
from utilities.response_utils import api_success_response, handle_api_exception

logger = logging.getLogger(__name__)


class UserAPIViewSet(APIView):

    def get(self, request):
        """
        API to get user details
        :param request: HTTP Request
        :returns: User details
        """
        # Get logs Extras
        extras = log_request(
            request, logger=logger, api_name=USER_API.get("GET").get("api_name")
        )

        try:
            # Validate request
            validate(request.body, USER_API.get("GET").get("schema"))

            logger.info(f"Fetching details for user: {request.user.id}", extra=extras)

            user_data = {"uid": request.user.id, "email": request.user.email}
            return api_success_response(
                status_code=status.HTTP_200_OK,
                message="Success",
                data=user_data,
                extras=extras,
            )

        except ValidationError as e:
            return handle_api_exception(
                exception=e,
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Validation Error",
                extras=extras,
                logger_obj=logger,
            )

        except Exception as e:
            return handle_api_exception(
                exception=e,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal Server Error",
                extras=extras,
                logger_obj=logger,
            )

    def put(self, request):
        """
        API to update user details
        :param request: HTTP Request
        :returns: User details
        """
        # Get logs Extras
        extras = log_request(
            request, logger=logger, api_name=USER_API.get("PUT").get("api_name")
        )

        try:
            # Validate request
            validate(request.body, USER_API.get("PUT").get("schema"))

            # Update user details
            request.user.update_email(request.data.get("email", request.user.email))
            request.user.update_name(
                request.data.get("first_name", request.user.first_name),
                request.data.get("last_name", request.user.last_name),
            )
            # Save user
            request.user.save()

            user_data = {
                "uid": request.user.id,
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
            }

            return api_success_response(
                status_code=status.HTTP_200_OK,
                message="Success",
                data=user_data,
                extras=extras,
            )

        except ValidationError as e:
            return handle_api_exception(
                exception=e,
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Validation Error",
                extras=extras,
                logger_obj=logger,
            )

        except Exception as e:
            return handle_api_exception(
                exception=e,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal Server Error",
                extras=extras,
                logger_obj=logger,
            )

    def delete(self, request, uid=None):
        # Get logs Extras
        extras = log_request(
            request, logger=logger, api_name=USER_API.get("DELETE").get("api_name")
        )

        try:
            # Validate request
            validate(request.body, USER_API.get("DELETE").get("schema"))

            # Set user status as deleted
            request.user.delete()
            request.user.save()

            return api_success_response(
                status_code=status.HTTP_200_OK,
                message="User Deleted",
                data={},
                extras=extras,
            )

        except ValidationError as e:
            return handle_api_exception(
                exception=e,
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Validation Error",
                extras=extras,
                logger_obj=logger,
            )

        except Exception as e:
            return handle_api_exception(
                exception=e,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal Server Error",
                extras=extras,
                logger_obj=logger,
            )
