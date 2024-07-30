import base64
from io import BytesIO
from django.http import JsonResponse
from PIL import Image
from .tasks import generate_image
from django.conf import settings
import os


def generate_images_view(request):
    prompts = [
        "A red flying dog",
        "A piano ninja",
        "A footballer kid"
    ]

    results = [generate_image.delay(prompt) for prompt in prompts]
    results = [result.get(timeout=100) for result in results]

    image_results = []

    for result in results:

        if 'base64' in result:
            base64_string = result['base64']
            image_data = base64.b64decode(base64_string)

            image = Image.open(BytesIO(image_data))

            file_name = f"{result['prompt'].replace(' ', '_')}.png"
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)

            image.save(file_path)

            prompt = result['prompt']
            image_url = os.path.join(settings.MEDIA_URL, file_name)
            image_results.append({'prompt': prompt, 'image_url': image_url})
            print("getting it")

    return JsonResponse({"status": "success", "results": image_results})