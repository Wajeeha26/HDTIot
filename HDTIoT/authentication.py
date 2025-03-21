import logging

from django.core.exceptions import ObjectDoesNotExist
from firebase_admin import auth
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from HDTIoT.settings import EXCLUDE_AUTH_ENDPOINTS
from user.models import User

logger = logging.getLogger(__name__)


def get_auth_token(request):
    """
    Returns Auth token from request
    :param request: HTTP Request
    :returns auth_token: Authorization token sent in request headers
    """
    middleware = "[FireBase Auth] "
    extras = {"endpoint": f"{middleware}", "user": ""}
    try:
        auth_header = request.headers.get("Authorization")
        logger.info(f"Authorization header: {auth_header}", extra=extras)
        if auth_header:
            auth_tokens = auth_header.split()
            if len(auth_tokens) == 2 and auth_tokens[0].lower() == "bearer":
                return auth_tokens[1]
        return None
    except BaseExceptionGroup:
        return None


class FirebaseAuthentication(BaseAuthentication):
    middleware = "[FireBase Auth]"

    def authenticate(self, request):
        extras = {"endpoint": f"{self.middleware}", "user": ""}
        logger.info(f"Request path: {request.path}", extra=extras)
        token = get_auth_token(request)
        if not token:
            logger.info("No token found", extra=extras)
            raise AuthenticationFailed("Authentication credentials were not provided.")

        try:
            firebase_user = auth.verify_id_token(token)
            if not firebase_user["email_verified"]:
                logger.info("User Email is not verified", extra=extras)
                raise AuthenticationFailed("User Email is not verified")

            request.fb_uuid = firebase_user.get("uid", "")
            user_email = firebase_user.get("email")
            logger.info(f"Got user[{user_email}] from firebase", extra=extras)
            if not user_email:
                raise auth.InvalidIdTokenError

            user = User.objects.get(email=user_email)
            if not user:
                logger.info("User not Found", extra=extras)
                raise AuthenticationFailed("User not found in current region")

            # Set user on the request
            logger.info(f"User Found: {user.id}", extra=extras)

            # if not check_user_access(user, request):
            #     raise AuthenticationFailed('User not authorized')

            return_tuple = (user, None)
            return return_tuple

        except ObjectDoesNotExist:
            logger.error("User not Found", extra=extras)
            raise AuthenticationFailed("User not found in current region")

        except auth.ExpiredIdTokenError:
            logger.error("Token expired", extra=extras)
            raise AuthenticationFailed("Expired token")

        except auth.InvalidIdTokenError:
            logger.error("Invalid token", extra=extras)
            raise AuthenticationFailed("Invalid token")


class BaseAuth(BaseAuthentication):
    def authenticate(self, request):
        authentication_classes = [FirebaseAuthentication()]

        if request.path.rstrip("/").split("/")[-1] in EXCLUDE_AUTH_ENDPOINTS:
            logger.info(
                f"Skipping auth check for: {request.path}",
                extra={"endpoint": "[General Auth]"},
            )
            return

        for auth_class in authentication_classes:
            try:
                user_auth_tuple = auth_class.authenticate(request)
                if user_auth_tuple is not None:
                    return user_auth_tuple
            except AuthenticationFailed:
                continue

        raise AuthenticationFailed("User not Authenticated")
