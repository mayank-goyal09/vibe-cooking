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
if "current_style" not in st.session_state:
    st.session_state.current_style = "Rustic"
if "current_ratio" not in st.session_state:
    st.session_state.current_ratio = "Square (1:1)"
if "current_angle" not in st.session_state:
    st.session_state.current_angle = "Auto-Detect"
if "current_light" not in st.session_state:
    st.session_state.current_light = "Auto-Detect"

# --- 2. Page Configuration & Setup ---
st.set_page_config(
    page_title="GenAI Food Studio",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Premium Obsidian & Saffron Theme, complete with background floating emojis
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&display=swap');

    /* Hide Streamlit Sidebar completely */
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    section[data-testid="stSidebar"] {
        display: none !important;
    }

    /* Global styling */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #070504 !important; /* Premium deep obsidian dark */
        color: #eae7e2 !important; /* Ivory text */
        overflow-x: hidden;
    }
    
    [data-testid="stHeader"] {
        background-color: rgba(7, 5, 4, 0.8) !important;
        backdrop-filter: blur(12px);
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1250px !important;
    }

    /* Elegant Font Headers */
    h1, h2, h3, h4 {
        font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important;
    }

    /* Background Floating Emojis (55% opacity for custom vivid blending on dark background) */
    .floating-emoji {
        position: fixed;
        font-size: 3.5rem;
        opacity: 0.55 !important;
        z-index: -1;
        pointer-events: none;
        user-select: none;
    }

    /* Asynchronous Keyframe Animations */
    .float-slow {
        animation: float-slow-anim 14s ease-in-out infinite;
    }
    .float-medium {
        animation: float-medium-anim 10s ease-in-out infinite;
    }
    .float-fast {
        animation: float-fast-anim 7s ease-in-out infinite;
    }

    @keyframes float-slow-anim {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-35px) rotate(15deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }
    @keyframes float-medium-anim {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-25px) rotate(-20deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }
    @keyframes float-fast-anim {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-15px) rotate(10deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }

    /* Input & Text Fields Styling */
    div[data-baseweb="input"] {
        background-color: #120f0d !important;
        border: 1px solid rgba(212, 175, 55, 0.25) !important;
        border-radius: 14px !important;
        color: #ffffff !important;
        transition: all 0.3s ease;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #e59c2b !important;
        box-shadow: 0 0 10px rgba(229, 156, 43, 0.35) !important;
    }
    
    /* Selectbox/Dropdown Styling */
    div[data-baseweb="select"] {
        background-color: #120f0d !important;
        border-radius: 14px !important;
        border: 1px solid rgba(212, 175, 55, 0.25) !important;
    }
    
    /* Premium Culinary Gradient Button */
    .stButton>button {
        background: linear-gradient(135deg, #a31d1d 0%, #d48a1c 100%) !important; /* Culinary Crimson to Amber Gold */
        color: #ffffff !important;
        border: 1px solid rgba(212, 175, 55, 0.35) !important;
        border-radius: 14px !important;
        height: 3.4em !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.8px !important;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        box-shadow: 0 6px 20px rgba(163, 29, 29, 0.45) !important;
        text-transform: uppercase;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 28px rgba(229, 156, 43, 0.55) !important;
        background: linear-gradient(135deg, #b82323 0%, #e59c2b 100%) !important;
        border-color: #e59c2b !important;
    }
    .stButton>button:active {
        transform: translateY(1px) !important;
    }

    /* Re-cook history buttons */
    .reuse-btn>button {
        background: rgba(18, 15, 13, 0.8) !important;
        color: #d4af37 !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        border-radius: 10px !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        padding: 6px 12px !important;
        box-shadow: none !important;
        text-transform: none !important;
        height: auto !important;
        width: auto !important;
    }
    .reuse-btn>button:hover {
        background: rgba(212, 175, 55, 0.15) !important;
        color: #ffffff !important;
        border-color: #e59c2b !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(212, 175, 55, 0.2) !important;
    }
    
    /* Glassmorphic card layouts */
    .glass-card {
        background: rgba(18, 14, 11, 0.75);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(212, 175, 55, 0.18);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 24px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.6);
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(212, 175, 55, 0.35);
        box-shadow: 0 15px 40px rgba(212, 175, 55, 0.1);
    }

    /* Gallery Card Styling */
    .gallery-card {
        background: rgba(18, 14, 11, 0.6);
        border: 1px solid rgba(212, 175, 55, 0.15);
        border-radius: 16px;
        padding: 12px;
        text-align: center;
        transition: all 0.3s ease;
        margin-bottom: 12px;
    }
    .gallery-card:hover {
        transform: translateY(-5px);
        border-color: rgba(212, 175, 55, 0.35);
        box-shadow: 0 10px 20px rgba(212, 175, 55, 0.08);
    }
    
    /* Metadata Badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        font-size: 0.72rem;
        font-weight: 800;
        border-radius: 50px;
        background: rgba(212, 175, 55, 0.1);
        color: #d4af37;
        border: 1px solid rgba(212, 175, 55, 0.2);
        margin-right: 6px;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    
    .prompt-text {
        font-size: 0.88rem;
        color: #dcdad4;
        background: rgba(0, 0, 0, 0.45);
        padding: 16px;
        border-radius: 10px;
        border-left: 4px solid #d4af37;
        margin-top: 10px;
        font-style: italic;
        line-height: 1.5;
    }

    /* Customize Streamlit Expander styling */
    .streamlit-expanderHeader {
        background-color: #120f0d !important;
        border: 1px solid rgba(212, 175, 55, 0.18) !important;
        border-radius: 12px !important;
        color: #eae7e2 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }
    
    /* Center text alignments */
    .centered-header {
        text-align: center;
        margin-bottom: 5px;
    }
    .centered-sub {
        text-align: center;
        color: #b5b1a9;
        font-size: 1.15rem;
        margin-top: 0px;
        margin-bottom: 35px;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Background Floating Food Emojis Injection ---
st.markdown("""
    <div class="floating-emoji float-slow" style="top: 10%; left: 3%;">🍕</div>
    <div class="floating-emoji float-medium" style="top: 38%; left: 5%;">🍣</div>
    <div class="floating-emoji float-fast" style="top: 75%; left: 3%;">🍝</div>
    <div class="floating-emoji float-slow" style="top: 12%; right: 4%;">🍰</div>
    <div class="floating-emoji float-medium" style="top: 48%; right: 6%;">🍤</div>
    <div class="floating-emoji float-fast" style="top: 82%; right: 3%;">🥐</div>
    <div class="floating-emoji float-slow" style="top: 4%; left: 45%;">🥑</div>
    <div class="floating-emoji float-medium" style="top: 90%; left: 35%;">🥩</div>
    """, unsafe_allow_html=True)

# --- 4. Main Page Header ---
st.markdown("<h1 class='centered-header' style='background: linear-gradient(135deg, #a31d1d 0%, #e59c2b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.5rem;'>DigitalChef AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='centered-sub'>Fine Art AI Food Photography Studio</p>", unsafe_allow_html=True)

# --- 5. Application Workspace Split Layout ---
col1, col2 = st.columns([1.1, 1])

# Input Options (from session state default values)
styles = ["Rustic", "Fine Dining", "Modern", "Street Food", "Moody"]
ratios = ["Square (1:1)", "Landscape (16:9)", "Portrait (9:16)"]
angles = ["Auto-Detect", "macro close-up shot", "45-degree angle hero shot", "top-down flat lay", "low-angle hero shot"]
lights = ["Auto-Detect", "warm golden hour glow", "soft diffused window light", "dramatic studio spotlighting", "vibrant neon glow"]

with col1:
    st.markdown("""
        <div class="glass-card" style="margin-bottom: 20px;">
            <h3 style="margin-top:0px; color:#d4af37; font-size:1.4rem; margin-bottom: 10px;">🍽️ Studio Console</h3>
            <p style="color:#b5b1a9; font-size:0.88rem; margin-bottom:0px;">Configure photography properties to achieve the perfect plating aesthetic.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Grid for main controls
    ctrl_col1, ctrl_col2 = st.columns(2)
    with ctrl_col1:
        style_idx = styles.index(st.session_state.current_style) if st.session_state.current_style in styles else 0
        style_choice = st.selectbox("Photography Style", styles, index=style_idx)
        st.session_state.current_style = style_choice
        
    with ctrl_col2:
        ratio_idx = ratios.index(st.session_state.current_ratio) if st.session_state.current_ratio in ratios else 0
        ratio_choice = st.selectbox("Aspect Ratio", ratios, index=ratio_idx)
        st.session_state.current_ratio = ratio_choice
        
    # Advanced Expander for Camera and Lighting
    angle_idx = angles.index(st.session_state.current_angle) if st.session_state.current_angle in angles else 0
    light_idx = lights.index(st.session_state.current_light) if st.session_state.current_light in lights else 0
    
    with st.expander("🛠️ Advanced Camera & Lighting Configurations"):
        adv_col1, adv_col2 = st.columns(2)
        with adv_col1:
            custom_angle = st.selectbox("Camera Angle", angles, index=angle_idx)
            st.session_state.current_angle = custom_angle
        with adv_col2:
            custom_light = st.selectbox("Lighting Setup", lights, index=light_idx)
            st.session_state.current_light = custom_light

    st.markdown("<br>", unsafe_allow_html=True)

    # Chef Input Box
    st.markdown("""
        <div class="glass-card">
            <h3 style="margin-top:0px; color:#d4af37; font-size:1.4rem; margin-bottom: 8px;">👨‍🍳 Culinary Specification</h3>
            <p style="color:#b5b1a9; font-size:0.88rem; margin-bottom:15px;">Input your dish name and description below.</p>
        </div>
    """, unsafe_allow_html=True)
    
    dish_name = st.text_input(
        "Enter Dish Name", 
        value=st.session_state.dish_input,
        placeholder="e.g., Creamy Butter Chicken with Garlic Naan",
        label_visibility="collapsed"
    )
    st.session_state.dish_input = dish_name
    
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("Generate Masterpiece ✨", use_container_width=True)

with col2:
    st.markdown("<h3 style='margin-top:0px; color:#d4af37; margin-bottom: 24px; font-size:1.4rem;'>📸 Studio Canvas</h3>", unsafe_allow_html=True)
    result_container = st.empty()
    
    # Set premium placeholder card
    result_container.markdown("""
        <div class="glass-card" style="text-align: center; padding: 75px 30px;">
            <span style="font-size: 3.5rem; display: block; margin-bottom: 15px;">🎨</span>
            <h3 style="color: #d4af37; margin-top: 5px; margin-bottom: 10px;">Canvas Ready to Plate</h3>
            <p style="color: #b5b1a9; font-size: 0.92rem; max-width: 320px; margin: 0 auto;">Specify a dish on the left console and hit generate to render the masterpiece.</p>
        </div>
    """, unsafe_allow_html=True)

# --- 6. Application Logic Execution ---
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

            with st.spinner(f"👨‍🍳 Chef is crafting prompt and plating your {dish_name}..."):
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
                
                # 4. Generate the image using FLUX.1
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
                        "angle": custom_angle,
                        "light": custom_light,
                        "path": saved_path,
                        "prompt": final_prompt,
                        "width": width,
                        "height": height
                    })
                    
                    # Update canvas display
                    with result_container.container():
                        st.markdown(f'<div class="glass-card" style="padding: 15px;">', unsafe_allow_html=True)
                        st.image(saved_path, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Metadata card
                        st.markdown(f"""
                            <div class="glass-card" style="margin-top: 15px;">
                                <span class="badge">{style_choice}</span>
                                <span class="badge">{ratio_choice}</span>
                                <span class="badge">{width}x{height}</span>
                                <p style="margin-bottom:0px; font-weight:700; color:#d4af37; margin-top:12px; font-size:1.05rem;">Generated Composition Prompt:</p>
                                <div class="prompt-text">"{final_prompt}"</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Download Button
                        with open(saved_path, "rb") as file:
                            st.download_button(
                                label="Download High-Res Masterpiece 📥",
                                data=file,
                                file_name=f"{dish_name.lower().replace(' ', '_')}_{timestamp}.png",
                                mime="image/png",
                                use_container_width=True
                            )
                        st.success("Your masterpiece is served. Bon Appétit!")
                        st.balloons()
                
        except Exception as e:
            st.error(f"Kitchen Accident: {e}")

# --- 7. History Gallery at Bottom of Main Page ---
if st.session_state.history:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #d4af37; font-size:2rem; margin-bottom:5px;'>🍽️ Recent Culinary Masterpieces</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #b5b1a9; font-size: 0.95rem; margin-bottom: 30px;'>Select any previous creation to restore its configuration and re-cook it.</p>", unsafe_allow_html=True)
    
    # Display up to 4 recent dishes in a responsive row layout
    recent_items = list(reversed(st.session_state.history))[:4]
    cols = st.columns(len(recent_items))
    
    for idx, item in enumerate(recent_items):
        with cols[idx]:
            st.markdown(f"""
                <div class="gallery-card">
                    <p style="font-weight: 700; color: #ffffff; margin-bottom: 6px; font-size: 0.95rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{item['dish_name']}</p>
                    <span class="badge" style="font-size: 0.6rem; padding: 2px 8px; margin: 0 auto 10px auto; display: inline-block;">{item['style']}</span>
                </div>
            """, unsafe_allow_html=True)
            st.image(item["path"], use_container_width=True)
            
            btn_col1, btn_col2, btn_col3 = st.columns([1, 6, 1])
            with btn_col2:
                st.markdown("<div class='reuse-btn'>", unsafe_allow_html=True)
                # Ensure unique key for each button to avoid streamlit duplication errors
                if st.button("Re-cook Settings 🔄", key=f"recook_{idx}_{item['path'][-14:-4]}"):
                    st.session_state.dish_input = item["dish_name"]
                    st.session_state.current_style = item["style"]
                    st.session_state.current_ratio = item["aspect_ratio"]
                    st.session_state.current_angle = item.get("angle", "Auto-Detect")
                    st.session_state.current_light = item.get("light", "Auto-Detect")
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

# --- 8. Footer ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---", unsafe_allow_html=True)
st.caption("DigitalChef AI Studio | Designed for premium food rendering | Powered by FLUX.1")