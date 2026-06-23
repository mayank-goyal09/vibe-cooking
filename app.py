import streamlit as st
import os
from core.prompt_gen import FoodPromptEngine
from core.model_loader import FoodImageGenerator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- 1. Page Setup ---
st.set_page_config(page_title="AI Food Photo Studio", page_icon="📸", layout="wide")

# Custom CSS for a professional look (using our assets mindset!)
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #FF4B4B; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Sidebar (The Control Room) ---
st.sidebar.title("🛠️ Studio Settings")
st.sidebar.info("This app uses SDXL via Hugging Face API for professional food photography.")

style_choice = st.sidebar.selectbox(
    "Select Photography Style", 
    ["Rustic", "Fine Dining", "Modern", "Street Food", "Moody"]
)

# --- 3. Main Interface ---
st.title("🍔 Mayank's GenAI Food Studio")
st.subheader("Transforming Menu Names into Masterpieces")

col1, col2 = st.columns([1, 1])

with col1:
    dish_name = st.text_input("Enter Dish Name", placeholder="e.g., Creamy Butter Chicken with Garlic Naan")
    generate_btn = st.button("Generate High-Res Photo ✨")

with col2:
    st.write("### 🖼️ Resulting Masterpiece")
    # Placeholder for the image
    result_container = st.empty()
    result_container.info("Enter a dish name and click generate to see the magic!")

# --- 4. The Logic Flow ---
if generate_btn:
    if not dish_name:
        st.error("Wait! The chef needs a dish name to start cooking.")
    else:
        try:
            # Initialize our classes
            engine = FoodPromptEngine()
            generator = FoodImageGenerator() # No need to pass token, it's in .env!

            with st.spinner(f"👨‍🍳 Plating your {dish_name}..."):
                # 1. Generate the 'Senior' Prompt
                final_prompt = engine.build_prompt(dish_name, style=style_choice.lower())
                
                # 2. Call the API
                output_file = "output/latest_dish.png"
                os.makedirs("output", exist_ok=True)
                
                img_path = generator.generate(final_prompt, output_file)

                if img_path:
                    result_container.image(img_path, caption=f"Style: {style_choice}", use_container_width=True)
                    
                    # 3. Add Download Button
                    with open(img_path, "rb") as file:
                        st.download_button(
                            label="Download for Menu 📥",
                            data=file,
                            file_name=f"{dish_name.replace(' ', '_')}.png",
                            mime="image/png"
                        )
                    st.success("Bon Appétit! Your photo is ready.")
                
        except Exception as e:
            st.error(f"Kitchen Accident: {e}")

# --- 5. Footer ---
st.divider()
st.caption("Developed by Mayank | Powered by SDXL & Python")