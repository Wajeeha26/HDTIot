from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User

class UserAPIViewSet(APIView):
    
    def get(self, request, uid=None):
        if uid is None:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(uid=uid)
            return Response({"uid": user.uid, "email": user.email, "role": user.role})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):

        
        try:
            data = request.data
            user = User.objects.create_user(uid=data['uid'], email=data['email'], role=data['role'])
            return Response({"message": "User created", "uid": user.uid}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, uid=None):
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

