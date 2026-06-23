import random

class FoodPromptEngine:
    def __init__(self):
        # Professional photography vocabulary
        self.lighting = ["soft morning light", "dramatic rim lighting", "volumetric fog", "warm golden hour"]
        self.surfaces = ["dark slate", "weathered oak wood", "polished marble", "rustic linen"]
        self.camera_angles = ["macro close-up", "45-degree hero shot", "top-down flat lay"]
        self.extra_details = ["steam rising", "scattered herbs", "water droplets", "perfect plating"]

    def build_prompt(self, dish_name, style="rustic"):
        """Transforms a dish name into a professional photography prompt."""
        
        # Crafting the 'Professional' wrapper
        light = random.choice(self.lighting)
        surface = random.choice(self.surfaces)
        angle = random.choice(self.camera_angles)
        extra = random.choice(self.extra_details)
        
        # The Master Prompt
        prompt = (f"Professional food photography of {dish_name}, {angle}, "
                  f"placed on a {surface}, {light}, {extra}, "
                  f"8k resolution, shot on 85mm lens, f/1.8, highly detailed, "
                  f"commercial quality.")
        
        return prompt

# Quick Test
engine = FoodPromptEngine()
print(f"🚀 Generated Prompt: {engine.build_prompt('Paneer Tikka')}")