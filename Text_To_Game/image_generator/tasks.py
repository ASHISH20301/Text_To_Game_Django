from celery import shared_task
import requests
from .models import GeneratedImage
import base64
from io import BytesIO
from PIL import Image
import os
from django.conf import settings

STABILITY_API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
STABILITY_API_KEY = "sk-roPHU9xmr3Vtid5tuydFg7fBdeS14KbaQOC1VtRWp6yTxO1S"


@shared_task
def generate_image(prompt):
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7.0,
        "clip_guidance_preset": "FAST_BLUE"
    }
    response = requests.post(STABILITY_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        response_json = response.json()
        artifacts = response_json.get('artifacts', [])

        if artifacts:
            artifact = artifacts[0]
            base64_string = artifact.get('base64', '')
            image_data = base64.b64decode(base64_string)

            image = Image.open(BytesIO(image_data))
            file_name = f"{prompt.replace(' ', '_')}.png"
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            image.save(file_path)

            image_url = os.path.join(settings.MEDIA_URL, file_name)

            GeneratedImage.objects.create(prompt=prompt, image_url=image_url)

            return {'prompt': prompt, 'base64': base64_string, 'image_url': image_url}
        else:
            return {"error": "No artifacts found in response"}
    else:
        return {"error": response.text}
