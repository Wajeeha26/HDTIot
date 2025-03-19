import json
import logging

from django.http import JsonResponse
from django.views import View

from accounts.models.chat_model import UserChat
from accounts.models.user_model import User

logger = logging.getLogger("chatbot")


def generate_chatbot_response(prompt):
    return f"Bot: I received your message - '{prompt}'"


class ChatbotView(View):
    """Handles chatbot interactions"""

    def get(self, request, uid):
        """Retrieve chat history for a user"""
        try:
            user = User.objects.get(uid=uid)  # ✅ Changed `id` to `uid`
            chats = UserChat.objects.filter(user=user).values(
                "id", "prompt", "response", "created_at"
            )  # ✅ Changed `uid` to `user`
            return JsonResponse(list(chats), safe=False, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

    def post(self, request):
        """Save a new user chat and generate a bot response"""
        try:
            data = json.loads(request.body)
            uid = data["uid"]
            prompt = data["prompt"]

            user = User.objects.get(uid=uid)  # ✅ Changed `id` to `uid`
            response = generate_chatbot_response(prompt)  # Mock response

            user_chat = UserChat.objects.create(
                user=user, prompt=prompt, response=response
            )  # ✅ Changed `uid` to `user`

            return JsonResponse(
                {
                    "id": user_chat.id,
                    "uid": user_chat.user.uid,  # ✅ Changed `.id` to `.uid`
                    "prompt": user_chat.prompt,
                    "response": user_chat.response,
                    "created_at": user_chat.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                },
                status=201,
            )

        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
