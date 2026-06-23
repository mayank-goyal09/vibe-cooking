import random

class FoodPromptEngine:
    def __init__(self):
        # Style-specific mapping for authentic food photography
        self.style_presets = {
            "rustic": {
                "lighting": ["warm afternoon sunlight", "soft diffused window light", "golden hour glow"],
                "surfaces": ["dark weathered oak table", "reclaimed barn wood", "rustic textured linen"],
                "angles": ["45-degree angle hero shot", "macro close-up shot"],
                "extra": ["scattered fresh herbs", "bread crumbs around the plate", "cast iron accents in background"]
            },
            "fine dining": {
                "lighting": ["dramatic studio spotlighting", "soft key light with dark shadow fill", "elegant candlelit reflections"],
                "surfaces": ["polished white marble countertop", "sleek black slate plate", "crisp luxury white tablecloth"],
                "angles": ["low-angle hero shot", "meticulous top-down flat lay"],
                "extra": ["microgreens garnish", "delicate sauce drizzle", "minimalist plating style", "expensive silver cutlery"]
            },
            "modern": {
                "lighting": ["bright clean studio lighting", "volumetric side window light"],
                "surfaces": ["minimalist matte concrete", "brushed copper sheet", "contemporary ceramic tile"],
                "angles": ["sharp 45-degree angle", "front-facing eye-level shot"],
                "extra": ["geometric shadows", "vibrant colorful plating contrast", "sleek modern glassware"]
            },
            "street food": {
                "lighting": ["vibrant neon glow", "harsh sun overhead", "warm streetlamp light"],
                "surfaces": ["crumpled brown parchment paper", "wooden street vendor cart", "industrial metal dining tray"],
                "angles": ["macro shot of texture", "top-down tray view"],
                "extra": ["steam rising", "generous sauce drips", "plastic/paper container", "close-up of hand holding the dish"]
            },
            "moody": {
                "lighting": ["low-key moody chiaroscuro lighting", "dramatic rim lighting with high contrast"],
                "surfaces": ["dark charcoal stone surface", "black charred wood", "dark velvet cloth"],
                "angles": ["extreme macro close-up", "high-contrast side-angle"],
                "extra": ["smoke drifting", "single drop of olive oil reflecting light", "dark ingredients scattered around"]
            }
        }

    def build_prompt(self, dish_name, style="rustic", custom_angle=None, custom_light=None):
        """Transforms a dish name into a professional photography prompt based on style and optional overrides."""
        style_key = style.lower().strip()
        preset = self.style_presets.get(style_key, self.style_presets["rustic"])
        
        # Pick standard components or use overrides
        angle = custom_angle if custom_angle else random.choice(preset["angles"])
        light = custom_light if custom_light else random.choice(preset["lighting"])
        surface = random.choice(preset["surfaces"])
        extra = random.choice(preset["extra"])
        
        prompt = (
            f"Award-winning professional food photography of {dish_name}, {angle}, "
            f"placed on {surface}, under {light}, {extra}. "
            f"Shot on 85mm lens, f/1.8 aperture, highly detailed texture, "
            f"commercial quality, ultra-realistic, 8k resolution."
        )
        return prompt

if __name__ == "__main__":
    engine = FoodPromptEngine()
    print(f"🚀 Generated Prompt: {engine.build_prompt('Paneer Tikka', style='fine dining')}")