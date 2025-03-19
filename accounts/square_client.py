from django.conf import settings
from square.client import Client

square_client = Client(
    access_token=settings.SQUARE_ACCESS_TOKEN, environment=settings.SQUARE_ENVIRONMENT
)


def get_square_client():
    return square_client
