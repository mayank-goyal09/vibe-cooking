import streamlit as st
import os
import time
from core.prompt_gen import FoodPromptEngine
from core.model_loader import FoodImageGenerator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- 1. Session State Initialization ---
if "history" not in st.session_state:
    st.session_state.history = []
if "dish_input" not in st.session_state:
    st.session_state.dish_input = ""

# --- 2. Page Configuration & Setup ---
st.set_page_config(
    page_title="GenAI Food Studio",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Dark Theme and Sleek UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Global styling */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #080c14 !important;
        color: #e5e7eb !important;
    }
    
    [data-testid="stHeader"] {
        background-color: rgba(8, 12, 20, 0.8) !important;
        backdrop-filter: blur(12px);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0b111e !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Input Styling */
    div[data-baseweb="input"] {
        background-color: #121926 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        transition: all 0.3s ease;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #ff5e62 !important;
        box-shadow: 0 0 0 2px rgba(255, 94, 98, 0.2) !important;
    }
    
    /* Selectbox/Dropdown Styling */
    div[data-baseweb="select"] {
        background-color: #121926 !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    /* Premium Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #ff5e62 0%, #ff9966 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        height: 3.2em !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(255, 94, 98, 0.3) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 94, 98, 0.5) !important;
        background: linear-gradient(135deg, #ff6b70 0%, #ffa87d 100%) !important;
    }
    .stButton>button:active {
        transform: translateY(1px) !important;
    }
    
    /* Info/Success/Error styling */
    div[data-testid="stNotification"] {
        background-color: #121926 !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        color: #e5e7eb !important;
    }
    
    /* Custom containers */
    .glass-card {
        background: rgba(18, 25, 38, 0.6);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
    }
    .badge {
        display: inline-block;
        padding: 4px 12px;
        font-size: 0.75rem;
        font-weight: 700;
        border-radius: 50px;
        background: rgba(255, 94, 98, 0.12);
        color: #ff9966;
        border: 1px solid rgba(255, 94, 98, 0.2);
        margin-right: 8px;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .prompt-text {
        font-size: 0.85rem;
        color: #9ca3af;
        background: rgba(0, 0, 0, 0.2);
        padding: 12px;
        border-radius: 8px;
        border-left: 3px solid #ff5e62;
        margin-top: 8px;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Sidebar (The Studio Control Room) ---
st.sidebar.markdown("<h2 style='text-align: center; margin-bottom: 0px;'>📸</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<h2 style='text-align: center; margin-top: 0px; background: linear-gradient(135deg, #ff5e62 0%, #ff9966 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Studio Controls</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #9ca3af; font-size: 0.9rem;'>Fine-tune your photography settings</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

style_choice = st.sidebar.selectbox(
    "🍽️ Photography Style", 
    ["Rustic", "Fine Dining", "Modern", "Street Food", "Moody"]
)

ratio_choice = st.sidebar.selectbox(
    "📐 Aspect Ratio", 
    ["Square (1:1)", "Landscape (16:9)", "Portrait (9:16)"]
)

# Advanced Configuration Expander
with st.sidebar.expander("🛠️ Advanced Settings"):
    custom_angle = st.selectbox(
        "Camera Angle",
        ["Auto-Detect", "macro close-up shot", "45-degree angle hero shot", "top-down flat lay", "low-angle hero shot"]
    )
    custom_light = st.selectbox(
        "Lighting Setup",
        ["Auto-Detect", "warm golden hour glow", "soft diffused window light", "dramatic studio spotlighting", "vibrant neon glow"]
    )

# History Gallery in Sidebar
if st.session_state.history:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Recent Dishes 🍽️")
    for idx, item in enumerate(reversed(st.session_state.history)):
        st.sidebar.image(item["path"], caption=f"{item['dish_name']} ({item['style']})", use_container_width=True)
        if st.sidebar.button("Reuse Settings 🔄", key=f"reuse_{len(st.session_state.history)-1-idx}"):
            st.session_state.dish_input = item["dish_name"]
            st.rerun()

# --- 4. Main Interface ---
st.markdown("<h1 style='background: linear-gradient(135deg, #ff5e62 0%, #ff9966 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 2.8rem; margin-bottom: 0px;'>DigitalChef AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #9ca3af; font-size: 1.1rem; margin-top: 5px; margin-bottom: 30px;'>Professional GenAI Food Photography Studio</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1.1, 1])

with col1:
    st.markdown("""
        <div class="glass-card">
            <h3 style="margin-top:0px; color:#ffffff;">👨‍🍳 What's cooking today?</h3>
            <p style="color:#9ca3af; font-size:0.9rem; margin-bottom:15px;">Input your dish name and watch the studio assemble the perfect studio shot.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Text input binding to session state
    dish_name = st.text_input(
        "Enter Dish Name", 
        value=st.session_state.dish_input,
        placeholder="e.g., Creamy Butter Chicken with Garlic Naan",
        label_visibility="collapsed"
    )
    
    # Store input value back into session state so it persists
    st.session_state.dish_input = dish_name
    
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("Generate Masterpiece ✨", use_container_width=True)

with col2:
    st.markdown("<h3 style='margin-top:0px; color:#ffffff;'>🖼️ Studio Canvas</h3>", unsafe_allow_html=True)
    result_container = st.empty()
    result_container.info("Enter a dish name and click Generate to see the magic!")

# --- 5. Application Logic ---
if generate_btn:
    if not dish_name.strip():
        st.error("Wait! The chef needs a dish name to start cooking.")
    else:
        try:
            # 1. Resolve Aspect Ratio Dimensions
            dimensions = {
                "Square (1:1)": (1024, 1024),
                "Landscape (16:9)": (1152, 648),
                "Portrait (9:16)": (648, 1152)
            }
            width, height = dimensions[ratio_choice]
            
            # Resolve custom overrides
            angle_param = None if custom_angle == "Auto-Detect" else custom_angle
            light_param = None if custom_light == "Auto-Detect" else custom_light
            
            engine = FoodPromptEngine()
            generator = FoodImageGenerator()

            with st.spinner(f"👨‍🍳 Plating your {dish_name}..."):
                # 2. Build the detailed style-preset prompt
                final_prompt = engine.build_prompt(
                    dish_name, 
                    style=style_choice, 
                    custom_angle=angle_param, 
                    custom_light=light_param
                )
                
                # 3. Create output path with timestamp to prevent caching issues
                os.makedirs("output", exist_ok=True)
                timestamp = int(time.time())
                img_path = f"output/dish_{timestamp}.png"
                
                # 4. Generate the image
                saved_path = generator.generate(
                    final_prompt, 
                    output_path=img_path, 
                    width=width, 
                    height=height
                )

                if saved_path:
                    # Save to session history
                    st.session_state.history.append({
                        "dish_name": dish_name,
                        "style": style_choice,
                        "aspect_ratio": ratio_choice,
                        "path": saved_path,
                        "prompt": final_prompt,
                        "width": width,
                        "height": height
                    })
                    
                    # Update canvas display
                    with result_container.container():
                        st.image(saved_path, use_container_width=True)
                        
                        # Metadata card
                        st.markdown(f"""
                            <div class="glass-card">
                                <span class="badge">{style_choice}</span>
                                <span class="badge">{ratio_choice}</span>
                                <span class="badge">{width}x{height}</span>
                                <p style="margin-bottom:0px; font-weight:700; color:#ffffff; margin-top:10px;">Generated Prompt:</p>
                                <div class="prompt-text">"{final_prompt}"</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Download Button
                        with open(saved_path, "rb") as file:
                            st.download_button(
                                label="Download High-Res Image 📥",
                                data=file,
                                file_name=f"{dish_name.lower().replace(' ', '_')}_{timestamp}.png",
                                mime="image/png",
                                use_container_width=True
                            )
                        st.success("Bon Appétit! Your photo is ready.")
                        st.balloons()
                
        except Exception as e:
            st.error(f"Kitchen Accident: {e}")

# --- 6. Footer ---
st.markdown("---", unsafe_allow_html=True)
st.caption("DigitalChef AI Studio | Designed for premium food rendering | Powered by FLUX.1")