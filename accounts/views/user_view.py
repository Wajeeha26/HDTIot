import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.api_schema.user_apiview import USER_API
from accounts.models.user_model import User
from openapi_schema_validator import validate

from utilities.log_utils import log_request
from utilities.response_utils import handle_api_exception, api_success_response

logger = logging.getLogger(__name__)


class UserAPIViewSet(APIView):
    
    def get(self, request):
        """
        API to get user details
        :param request: HTTP Request
        :returns: User details
        """
        # Get logs Extras
        extras = log_request(request, logger=logger, api_name=USER_API.get("GET").get("api_name"))

        try:

            # Validate request
            validate(request.body, USER_API.get("GET").get("schema"))


            uid = request.query_params.get('uid')

            user = User.objects.get(uid=uid)
            logger.info(f"Fetching details for user: {uid}", extra=extras)

            user_data = {
                "uid": user.uid,
                "email": user.email,
                "role": user.role
            }
            return api_success_response(status_code=status.HTTP_200_OK, message="Success",
                                        data=user_data, extras=extras)

        except ValidationError as e:
            return handle_api_exception(exception=e, status_code=status.HTTP_400_BAD_REQUEST,
                                        message="Validation Error", extras=extras, logger_obj=logger)

        except Exception as e:
            return handle_api_exception(exception=e, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        message="Internal Server Error", extras=extras, logger_obj=logger)

    
    def put(self, request):
        uid = request.data.get('uid')
        if uid is None:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(uid=uid)
            user.email = request.data.get('email', user.email)
            user.role = request.data.get('role', user.role)
            user.save()
            return Response({"message": "User updated"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, uid=None):
        if uid is None:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(uid=uid)
            user.delete()
            return Response({"message": "User deleted"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

