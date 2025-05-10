import os
import django
import google.generativeai as genai

# Django setup (script başında mutlaka yapın)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chathub_project.settings')
django.setup()

from django.conf import settings

def test_gemini_connection():
    try:
        # API Key kontrolü
        print(f"API Key from settings: {settings.GOOGLE_API_KEY[:5]}...")  # İlk 5 karakteri göster
        
        # Yapılandırma
        genai.configure(
            api_key=settings.GOOGLE_API_KEY,
            client_options={'api_endpoint': 'https://generativelanguage.googleapis.com/v1beta'}
        )
        
        # Model listesi
        print("\nAvailable Models:")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"- {model.name} (Toksin: {model.output_token_limit})")
                
        # Test sorgusu
        print("\nTest Response:")
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content("Python'da merhaba dünya nasıl yazılır?")
        print(response.text)
        
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    test_gemini_connection()