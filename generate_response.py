import requests
import os
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from typing import Any
from dotenv import load_dotenv

# get the authentication password
load_dotenv()
secret_value = os.getenv("secret")
URL="https://copied-hardcore-ensure.ngrok-free.dev/generate"
def ask_question(prompt):
    prompt_header={
        'authorization':str(secret_value)
    }
    if prompt[0:5]=="story":
        prompt_payload={
            'prompt':prompt[6:],
        'max_length': 2048
        }
    else:
        prompt_payload = {
            'prompt': prompt[3:],
            'max_length': int(prompt[0:3])
        }
    # print(prompt[0:3])
    # print(prompt[3:])
    print("sending the prompt")
    result= requests.post(url=URL,headers=prompt_header,json=prompt_payload)
    try:
        result=result.json()
    except ValueError:
        raise RuntimeError(f"server returned non jason:{result.text}")
    if "response" not in result:
        raise RuntimeError(f"missing response key")
    return result['response']

class GenerativeLLM(LLM):
    def _call(self, prompt: str, stop: list[str] | None = None, run_manager: CallbackManagerForLLMRun | None = None, **kwargs: Any) :
        return ask_question(prompt)
    @property
    def _llm_type(self) -> str:
        return "custom_huggingface"