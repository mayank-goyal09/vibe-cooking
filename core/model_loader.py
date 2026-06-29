import os
import io
import time
import requests
from PIL import Image
from dotenv import load_dotenv

# Load the variables from .env
load_dotenv()

class FoodImageGenerator:
    def __init__(self):
        # Automatically pull the token from the .env file
        self.hf_token = os.getenv("HF_TOKEN")
        # We use the official Hugging Face Router endpoint.
        # Paid/Partner models (like FLUX.1-schnell) consume partner credits.
        # Free serverless models (like stabilityai/stable-diffusion-xl-base-1.0) do not deplete partner credits.
        self.model_id = "black-forest-labs/FLUX.1-schnell" 
        self.url = f"https://router.huggingface.co/hf-inference/models/{self.model_id}"
        self.headers = {"Authorization": f"Bearer {self.hf_token}"}
        
        if not self.hf_token:
            raise ValueError("❌ Error: HF_TOKEN not found in .env file!")

    def generate(self, prompt, output_path="output/dish.png", width=1024, height=1024):
        print(f"👨‍🍳 Chef is cooking (using {self.model_id} on Hugging Face, {width}x{height})...")
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "negative_prompt": "blurry, distorted, low quality, text, watermark, messy plate, low resolution, deformed, bad lighting",
                "guidance_scale": 7.5,
                "width": int(width),
                "height": int(height)
            }
        }

        response = requests.post(self.url, headers=self.headers, json=payload)

        if response.status_code == 200:
            image = Image.open(io.BytesIO(response.content))
            image.save(output_path)
            print(f"✅ Image saved to {output_path}")
            return output_path
        
        elif response.status_code == 503:
            print("⏳ Model is warming up. Waiting 20 seconds...")
            time.sleep(20)
            return self.generate(prompt, output_path, width=width, height=height)
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            raise Exception(f"API Error {response.status_code}: {response.text}")