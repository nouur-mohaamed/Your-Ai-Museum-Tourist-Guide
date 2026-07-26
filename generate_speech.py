from dotenv import load_dotenv
import os
import requests
load_dotenv()
secret_value = os.getenv("secret")
URL="https://copied-hardcore-ensure.ngrok-free.dev/speech"
def generate_speech(text,language):
    if language == "japanese":
        lang_model_symbol = 'j'
    elif language == "french":
        lang_model_symbol = 'f'
    elif language == "spanish":
        lang_model_symbol = 'e'
    elif language == "hindi":
        lang_model_symbol = 'h'
    else:
        lang_model_symbol = 'a'
    prompt_header = {
        'authorization': str(secret_value)
    }
    prompt_payload = {
        'text':text,
        'language':lang_model_symbol
    }
    print("sending the prompt")
    result = requests.post(url=URL, headers=prompt_header, json=prompt_payload)
    result.raise_for_status()  # Raises an exception if the request failed
    return result.content
