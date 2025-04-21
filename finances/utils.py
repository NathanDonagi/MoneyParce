import google.generativeai as genai
from django.conf import settings



def configure_gemini():
    genai.configure(api_key=settings.GEMINI_API_KEY)

def get_chat_model():
    configure_gemini()
    return genai.GenerativeModel('gemini-pro')