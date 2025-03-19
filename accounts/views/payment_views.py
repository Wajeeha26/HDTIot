from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models.service_model import Service, UserService
from accounts.models.user_model import User
from accounts.square_client import get_square_client


class VerifySquarePaymentView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        service_id = request.data.get("service_id")
        receipt_id = request.data.get("receipt_id")

        if not user_id or not service_id or not receipt_id:
            return Response(
                {"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Step 1: Get Square client
            client = get_square_client()

            # Step 2: Verify the payment using the receipt ID
            result = client.payments.get_payment(receipt_id)
            if result.is_error():
                return Response(
                    {"error": "Invalid payment receipt"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            payment = result.body.get("payment")
            if not payment or payment.get("status") != "COMPLETED":
                return Response(
                    {"error": "Payment not completed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Step 3: Get the user and service
            user = User.objects.get(uid=user_id)
            service = Service.objects.get(id=service_id)

            # Step 4: Check if service is already registered
            if UserService.objects.filter(user=user, service=service).exists():
                return Response(
                    {"message": "Service already registered for user"},
                    status=status.HTTP_200_OK,
                )

            # Step 5: Register the service for the user
            UserService.objects.create(user=user, service=service)

            return Response(
                {"message": "Payment verified and service registered successfully"},
                status=status.HTTP_201_CREATED,
            )

        except ObjectDoesNotExist:
            return Response(
                {"error": "User or Service not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
