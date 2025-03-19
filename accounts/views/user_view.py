from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models.user_model import User


class UserAPIViewSet(APIView):

    def get(self, request, uid=None):
        if uid is None:
            return Response(
                {"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(uid=uid)
            return Response(
                {
                    "uid": user.uid,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "user_type": user.user_type,
                    "is_deleted": user.is_deleted,
                }
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):
        try:
            data = request.data
            user = User.objects.create_user(
                uid=data["uid"],
                email=data["email"],
                first_name=data["first_name"],
                last_name=data.get("last_name", ""),
                user_type=data.get("user_type", 1),
                is_deleted=data.get("is_deleted", 0),
                password=data.get("password", None),
            )
            return Response(
                {"message": "User created", "uid": user.uid},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, uid=None):
        if uid is None:
            return Response(
                {"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(uid=uid)
            user.email = request.data.get("email", user.email)
            user.first_name = request.data.get("first_name", user.first_name)
            user.last_name = request.data.get("last_name", user.last_name)
            user.user_type = request.data.get("user_type", user.user_type)
            user.is_deleted = request.data.get("is_deleted", user.is_deleted)
            user.save()
            return Response({"message": "User updated"})
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uid=None):
        if uid is None:
            return Response(
                {"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(uid=uid)
            user.delete()
            return Response({"message": "User deleted"})
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
