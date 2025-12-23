import os
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv('OPENAI_API_KEY', '')
gemini_key = os.getenv('GEMINI_API_KEY', '')
deepseek_key = os.getenv('DEEPSEEK_API_KEY', '')

print(f"OpenAI Key Present: {bool(openai_key)}")
print(f"OpenAI Key Length: {len(openai_key)}")
if len(openai_key) > 0:
    print(f"OpenAI Key Start: {openai_key[:5]}...")

print(f"Gemini Key Present: {bool(gemini_key)}")
print(f"Gemini Key Length: {len(gemini_key)}")

print(f"DeepSeek Key Present: {bool(deepseek_key)}")
print(f"DeepSeek Key Length: {len(deepseek_key)}")
