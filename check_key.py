from src.utils.config import OPENROUTER_API_KEY
import os

print(f"Current working directory: {os.getcwd()}")
print(f"OPENROUTER_API_KEY length: {len(OPENROUTER_API_KEY)}")
if len(OPENROUTER_API_KEY) > 5:
    print(f"OPENROUTER_API_KEY start: {OPENROUTER_API_KEY[:5]}...")
else:
    print("OPENROUTER_API_KEY is too short or empty")
