from datetime import datetime
import requests
import base64
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
STABILITY_API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

out_dir = 'api_out'
out_dir_t2i = os.path.join(out_dir, 'txt2img')
os.makedirs(out_dir_t2i, exist_ok=True)

def timestamp():
    return datetime.fromtimestamp(time.time()).strftime("%Y%m%d-%H%M%S")

def decode_and_save_base64(base64_str, save_path):
    with open(save_path, "wb") as file:
        file.write(base64.b64decode(base64_str))

def generate_images(image_prompts: list):
    images = []

    for prompt_text in image_prompts:
        headers = {
            "Authorization": f"Bearer {STABILITY_API_KEY}",
            "Accept": "application/json",
        }
        
        payload = {
            "text_prompts": [
                {
                    "text": prompt_text,
                    "weight": 1
                }
            ],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "steps": 30,
            "samples": 1,
        }

        try:
            response = requests.post(
                STABILITY_API_URL,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            response_data = response.json()
            
            if "artifacts" in response_data and len(response_data["artifacts"]) > 0:
                base64_image = response_data["artifacts"][0]["base64"]
                filename = f"txt2img-{timestamp()}.png"
                save_path = os.path.join(out_dir_t2i, filename)
                decode_and_save_base64(base64_image, save_path)

                # return base64 for frontend display (optional)
                images.append(f"data:image/png;base64,{base64_image}")
            else:
                print("No image artifacts in response")
                images.append("image not available")
        except requests.exceptions.RequestException as e:
            print("Image generation failed:", e)
            images.append("image not available")

    return images