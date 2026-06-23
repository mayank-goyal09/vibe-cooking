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
        self.url = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
        self.headers = {"Authorization": f"Bearer {self.hf_token}"}
        
        if not self.hf_token:
            raise ValueError("❌ Error: HF_TOKEN not found in .env file!")

    def generate(self, prompt, output_path="output/dish.png"):
        print("👨‍🍳 Chef is cooking (using SDXL on Hugging Face)...")
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "negative_prompt": "blurry, distorted, low quality, text, watermark, messy plate",
                "guidance_scale": 7.5
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
            return self.generate(prompt, output_path)
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return None