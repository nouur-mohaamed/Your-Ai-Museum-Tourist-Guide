from dotenv import load_dotenv
import os
import requests
load_dotenv()
secret_value = os.getenv("secret")
URL="https://copied-hardcore-ensure.ngrok-free.dev/translate"
def generate_translation(text,target_lang,src_lang):
    if target_lang == "french":
        target_lang_symbol = "fra_Latn"
    elif target_lang == "spanish":
        target_lang_symbol = "spa_Latn"
    else:
        target_lang_symbol = "eng_Latn"
    if src_lang == "french":
        src_lang_symbol = "fra_Latn"
    elif src_lang == "spanish":
        src_lang_symbol = "spa_Latn"
    else:
        src_lang_symbol = "eng_Latn"

    prompt_header = {
        'authorization': str(secret_value)
    }
    prompt_payload = {
        'text': text,
        'target_language': target_lang_symbol,
        'src_language': src_lang_symbol
    }
    print("sending the prompt")
    result = requests.post(url=URL, headers=prompt_header, json=prompt_payload)
    try:
        result = result.json()
    except ValueError:
        raise RuntimeError(f"server returned non jason:{result.text}")
    if "response" not in result:
        raise RuntimeError(f"missing response key")
    return result['response']