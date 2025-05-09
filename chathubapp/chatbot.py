import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def generate_gemini_response(user_input):
    response = model.generate_content(user_input)
    return response.text