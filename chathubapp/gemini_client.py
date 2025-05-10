from dotenv import load_dotenv
from pathlib import Path


import os
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # manage.py'nin olduğu dizin
load_dotenv(BASE_DIR / '.env')
# Debug çıktıları
print("🔄 Ortam Değişkenleri Yüklendi mi?", 'GOOGLE_API_KEY' in os.environ)
print("🔑 API Key İlk 5 Karakter:", os.environ.get("GOOGLE_API_KEY", "BULUNAMADI")[:5])

# API Anahtarını Kontrollü Al
api_key1 = os.environ.get("GOOGLE_API_KEY", "").strip()
if not api_key1:
    raise ValueError("❌ API anahtarı bulunamadı! .env dosyasını kontrol edin")

from google import genai
from google.genai import types
from django.conf import settings

api0=os.environ.get("GOOGLE_API_KEY").strip()
print("xxxx")
print(api0)
print("xxxx")


genai_client = genai.Client(api_key=api_key1)

def get_gemini_response(user_input):
    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=user_input),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    response_text = ""
    for chunk in genai_client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response_text += chunk.text
    return response_text
