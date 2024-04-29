from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from openai import OpenAI
from django.conf import settings
from .bots import translate_bot
# Create your views here.


class TranslateAPIView(APIView):
    def post(self, request):
        user_message = request.data.get("message")
        chatgpt_reponse = translate_bot(user_message)
        return Response({"message": chatgpt_reponse})
