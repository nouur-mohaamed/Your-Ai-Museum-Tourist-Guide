from PIL import Image
import io
import base64
import requests
from dotenv import load_dotenv
import os
import numpy as np
load_dotenv()
URL_2="https://copied-hardcore-ensure.ngrok-free.dev/embedd"
secret_value = os.getenv("SECRET")
def get_image_embedding(image_url):
    print("prepare the image to turn to embedding")
    image = Image.open(image_url).convert("RGB") # convert into Image object
    buffer = io.BytesIO() # create the temp file "buffer" that will store the image bytes in RAM
    image.save(buffer, format="JPEG") #writes the JPEG bytes into memory.
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8") #transform from bytes to string that can be sent to server
    print("finished preparations")
    prompt_header = {
        'authorization': str(secret_value)
    }
    prompt_payload = {
        'image': image_base64
    }
    print("sending image to get it's embedding")
    print("hello")
    resulted_embedding = requests.post(url=URL_2, headers=prompt_header, json=prompt_payload)
    print(resulted_embedding)
    try:
        resulted_embedding= resulted_embedding.json() #transform to python dictionary
    except ValueError :
        raise RuntimeError(f'image embedding process error:server returned non jason/{resulted_embedding.text}')
    if 'response' not in resulted_embedding:
        raise RuntimeError(f'image embedding process error:response key is missing')
    print("image embedding received successfully")
    embedding=resulted_embedding['response']
    embedding = np.array(embedding, dtype=np.float32) #transform to numpy array
    print("embeddings: ", embedding)
    return embedding