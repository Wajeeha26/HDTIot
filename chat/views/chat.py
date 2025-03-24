from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chat.models.chat import Chat, ChatHistory
from chat.utils import train_epigenetic_clock
from chat.ai_agent import get_response_from_ai_agent
from rest_framework.permissions import AllowAny

chat_history = {}

ALLOWED_MODEL_NAMES = [
    "llama3-70b-8192",
    "mixtral-8x7b-32768",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant"
]

class ChatEndpoint(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        model_name = request.data.get('model_name')
        messages = request.data.get('messages', [])
        allow_search = request.data.get('allow_search', False)
        system_prompt = request.data.get('system_prompt', 'Act as an AI chatbot who is smart and friendly')
        session_id = request.data.get('session_id')

        if model_name not in ALLOWED_MODEL_NAMES:
            return Response({"error": "Invalid model name"}, status=status.HTTP_400_BAD_REQUEST)

        if session_id not in chat_history:
            chat_history[session_id] = []
        
        chat_history[session_id].extend(messages)

        query = chat_history[session_id]
        response = get_response_from_ai_agent(model_name, query, allow_search, system_prompt)
        
        chat_history[session_id].append(response)

        return Response({"response": response, "session_id": session_id})


class EpigeneticAgeEndpoint(APIView):
    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = train_epigenetic_clock(file)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
