import os
import uuid
import requests
from urllib.parse import quote
from django.conf import settings
from django.http import HttpResponse
from PIL import Image
import mimetypes

def generate_image(request):  # Now handles both generation + serving
    if request.method == 'GET':
        filename = request.GET.get('file')
        if filename:
            filepath = os.path.join(settings.MEDIA_ROOT, 'generated', filename)
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    img_data = f.read()
                # ✅ FIX: Force correct MIME type
                response = HttpResponse(img_data, content_type='image/jpeg')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
        return HttpResponse("File not found", status=404)
    
    # POST - generate new image
    prompt = request.POST.get('prompt')
    print(f"Generating image for prompt: {prompt}")
    
    encoded_prompt = quote(prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    
    response = requests.get(image_url)
    img_data = response.content
    
    folder = os.path.join(settings.MEDIA_ROOT, "generated")
    os.makedirs(folder, exist_ok=True)
    
    filename = f"img_{uuid.uuid4().hex[:8]}.jpg"
    image_path = os.path.join(folder, filename)
    
    with open(image_path, "wb") as f:
        f.write(img_data)
    
    print(f"Saved: {filename}")
    return f"generated/{filename}"
