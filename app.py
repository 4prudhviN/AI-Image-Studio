"""
AI Image Studio
===============
A polished Streamlit web app that generates images using the Pollinations AI API,
with Groq-powered prompt enhancement, prompt history, favourites, aspect ratio
presets, generation statistics, and a dark gradient UI.

MirAI School of Technology - Virtual Summer Internship 2026 AI Builder Track
"""

import io
import random
import urllib.parse
from datetime import datetime

import requests
import streamlit as st
from PIL import Image

# ---------------------------------------------------------------------------
# Page config  (MUST be first Streamlit call)
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Global CSS — dark gradient theme
# ---------------------------------------------------------------------------

st.markdown(
    """
    <style>
    /* ─────────────────────────────────────────
       BASE — dark gradient background
    ───────────────────────────────────────── */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }

    /* ─────────────────────────────────────────
       GLOBAL TEXT — force everything light
    ───────────────────────────────────────── */
    html, body,
    .stApp, .stApp *,
    .stMarkdown, .stMarkdown p,
    div[data-testid="stText"],
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] li,
    div[data-testid="stMarkdownContainer"] span,
    label, .stLabel,
    p, span, div { color: #e8e8f0; }

    /* ─────────────────────────────────────────
       WIDGET LABELS  (the text above inputs)
    ───────────────────────────────────────── */
    .stTextInput  label,
    .stSelectbox  label,
    .stSlider     label,
    .stCheckbox   label,
    .stRadio      label,
    .stTextArea   label,
    .stNumberInput label,
    div[data-testid="stWidgetLabel"],
    div[data-testid="stWidgetLabel"] p,
    div[data-testid="stWidgetLabel"] span {
        color: #c4b5fd !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.02em;
    }

    /* ─────────────────────────────────────────
       INPUTS — text boxes & select boxes
    ───────────────────────────────────────── */
    .stTextInput input,
    .stTextArea  textarea,
    .stNumberInput input {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(167, 139, 250, 0.45) !important;
        border-radius: 10px !important;
        color: #f0f0ff !important;
        font-size: 0.95rem !important;
        padding: 10px 14px !important;
    }
    .stTextInput input::placeholder,
    .stTextArea  textarea::placeholder {
        color: #7c7ca0 !important;
    }
    .stTextInput input:focus,
    .stTextArea  textarea:focus {
        border-color: #f953c6 !important;
        box-shadow: 0 0 0 2px rgba(249, 83, 198, 0.25) !important;
    }

    /* ─────────────────────────────────────────
       SELECTBOX
    ───────────────────────────────────────── */
    div[data-baseweb="select"] > div {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(167, 139, 250, 0.45) !important;
        border-radius: 10px !important;
        color: #f0f0ff !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {
        color: #f0f0ff !important;
    }
    /* Dropdown menu */
    ul[data-baseweb="menu"],
    li[role="option"] {
        background: #1e1b4b !important;
        color: #e8e8f0 !important;
    }
    li[role="option"]:hover {
        background: rgba(249, 83, 198, 0.2) !important;
    }

    /* ─────────────────────────────────────────
       SLIDERS
    ───────────────────────────────────────── */
    div[data-testid="stSlider"] div[data-baseweb="slider"] div {
        background: rgba(167, 139, 250, 0.3) !important;
    }
    div[data-testid="stSlider"] div[role="slider"] {
        background: #f953c6 !important;
        border: 2px solid #fff !important;
    }
    /* Slider value label */
    div[data-testid="stSlider"] p,
    div[data-testid="stSlider"] span {
        color: #c4b5fd !important;
        font-weight: 600;
    }

    /* ─────────────────────────────────────────
       CHECKBOXES
    ───────────────────────────────────────── */
    .stCheckbox label span {
        color: #e8e8f0 !important;
        font-size: 0.92rem !important;
    }
    .stCheckbox svg { color: #f953c6 !important; }

    /* ─────────────────────────────────────────
       CAPTION / SMALL TEXT
    ───────────────────────────────────────── */
    .stCaption, div[data-testid="stCaptionContainer"] p,
    small { color: #9090b8 !important; }

    /* ─────────────────────────────────────────
       INFO / SUCCESS / WARNING banners
    ───────────────────────────────────────── */
    div[data-testid="stAlert"] p,
    div[data-testid="stAlert"] span { color: #1a1a2e !important; }

    /* ─────────────────────────────────────────
       TABS
    ───────────────────────────────────────── */
    div[data-testid="stTabs"] button {
        color: #a78bfa !important;
        font-weight: 600;
        font-size: 0.92rem;
        border-bottom: 2px solid transparent;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #f953c6 !important;
        border-bottom: 2px solid #f953c6 !important;
    }

    /* ─────────────────────────────────────────
       EXPANDER
    ───────────────────────────────────────── */
    details summary p,
    details summary span,
    div[data-testid="stExpander"] summary p {
        color: #c4b5fd !important;
        font-weight: 600;
    }
    div[data-testid="stExpander"] {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(167,139,250,0.25) !important;
        border-radius: 10px !important;
    }

    /* ─────────────────────────────────────────
       SIDEBAR
    ───────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0b26 0%, #1a1740 100%) !important;
        border-right: 1px solid rgba(249, 83, 198, 0.3) !important;
    }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #e8e8f0 !important;
    }
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #f9a8d4 !important;
        font-size: 1rem;
        letter-spacing: 0.04em;
    }

    /* ─────────────────────────────────────────
       BUTTONS
    ───────────────────────────────────────── */
    div.stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #f953c6, #b91d73) !important;
        border: none !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(249, 83, 198, 0.4) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(249, 83, 198, 0.6) !important;
    }
    div.stButton > button[kind="secondary"] {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(167,139,250,0.5) !important;
        color: #c4b5fd !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background: rgba(167,139,250,0.15) !important;
        transform: translateY(-2px) !important;
    }

    /* ─────────────────────────────────────────
       DOWNLOAD BUTTON
    ───────────────────────────────────────── */
    div.stDownloadButton > button {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(167,139,250,0.5) !important;
        color: #c4b5fd !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
    div.stDownloadButton > button:hover {
        background: rgba(167,139,250,0.15) !important;
    }

    /* ─────────────────────────────────────────
       DIVIDER
    ───────────────────────────────────────── */
    hr { border-color: rgba(167, 139, 250, 0.2) !important; }

    /* ─────────────────────────────────────────
       GRADIENT TITLE
    ───────────────────────────────────────── */
    .gradient-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #f953c6, #b91d73, #a78bfa, #f953c6);
        background-size: 300% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shine 4s linear infinite;
        margin-bottom: 0;
        line-height: 1.2;
    }
    @keyframes shine { to { background-position: 300% center; } }

    .subtitle {
        color: #a78bfa !important;
        font-size: 1.05rem;
        margin-top: 0.3rem;
        margin-bottom: 1.2rem;
    }

    /* ─────────────────────────────────────────
       SECTION HEADINGS
    ───────────────────────────────────────── */
    h2, h3 {
        color: #e8e8f0 !important;
        font-weight: 700;
    }

    /* ─────────────────────────────────────────
       STAT CARDS
    ───────────────────────────────────────── */
    .stat-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(167,139,250,0.2);
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        margin-bottom: 10px;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 800;
        color: #f953c6 !important;
        line-height: 1;
    }
    .stat-label {
        font-size: 0.72rem;
        color: #a78bfa !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 4px;
    }

    /* ─────────────────────────────────────────
       PROMPT PILLS
    ───────────────────────────────────────── */
    .pill-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 6px 0 14px 0;
    }
    .pill {
        background: rgba(249, 83, 198, 0.12);
        border: 1px solid rgba(249, 83, 198, 0.4);
        border-radius: 20px;
        padding: 5px 14px;
        font-size: 0.8rem;
        color: #f9a8d4 !important;
    }

    /* ─────────────────────────────────────────
       HISTORY & FAVOURITE CARDS
    ───────────────────────────────────────── */
    .history-card {
        background: rgba(255,255,255,0.04);
        border-left: 3px solid #f953c6;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        font-size: 0.85rem;
        color: #d1d5db !important;
        line-height: 1.5;
    }
    .history-card b { color: #f9a8d4 !important; }

    .fav-card {
        background: rgba(255,255,255,0.04);
        border-left: 3px solid #fbbf24;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        font-size: 0.85rem;
        color: #d1d5db !important;
        line-height: 1.5;
    }

    /* ─────────────────────────────────────────
       IMAGE CAPTION
    ───────────────────────────────────────── */
    div[data-testid="stImage"] p {
        color: #a78bfa !important;
        font-size: 0.82rem;
        text-align: center;
    }

    /* ─────────────────────────────────────────
       SCROLLBAR
    ───────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0f0c29; }
    ::-webkit-scrollbar-thumb {
        background: rgba(249, 83, 198, 0.4);
        border-radius: 3px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ART_STYLES = [
    "Realistic", "Anime", "Oil Painting", "Watercolor",
    "Cyberpunk", "Fantasy", "Pixel Art", "Sketch", "3D Render", "Minimalist",
]

# Aspect ratio presets: label → (width, height)
ASPECT_RATIOS = {
    "1:1 Square":   (512, 512),
    "16:9 Landscape": (912, 512),
    "9:16 Portrait":  (512, 912),
    "4:3 Standard": (768, 576),
    "Custom":       None,
}

MAGIC_ENHANCE_KEYWORDS = (
    "masterpiece, 8k resolution, highly detailed, cinematic lighting, "
    "trending on artstation, unreal engine 5 render"
)

EXAMPLE_PROMPTS = [
    "Neon samurai in a rainy cyberpunk city",
    "Enchanted forest with glowing mushrooms",
    "Astronaut surfing a wave on Mars",
    "Dragon made of cherry blossoms",
    "Underwater steampunk library",
    "Wolf howling at a galaxy moon",
    "Cozy wizard cottage in autumn",
    "Robot tending a futuristic garden",
]

SURPRISE_PROMPTS = [
    "A majestic dragon soaring over a misty mountain range at sunrise",
    "An astronaut exploring an alien jungle with bioluminescent plants",
    "A steampunk city floating in the clouds with airships and gear towers",
    "A lone samurai standing under cherry blossoms in the rain",
    "An underwater kingdom with coral castles and merfolk royalty",
    "A futuristic Tokyo street at night, neon reflections on wet pavement",
    "A magical forest library where books fly between ancient trees",
    "A wolf made entirely of galaxies and stardust howling at the moon",
    "An ancient Egyptian pyramid surrounded by a modern cyberpunk city",
    "A cozy cottage on the edge of a volcanic crater with lavender fields",
]

POLLINATIONS_BASE_URL = "https://image.pollinations.ai/prompt/"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------

defaults = {
    "generated_image": None,
    "current_art_style": "Realistic",
    "current_prompt": "",
    "enhanced_prompt": "",
    "total_generated": 0,
    "prompt_history": [],      # list of dicts: {prompt, style, time}
    "favourites": [],          # list of dicts: {prompt, style}
    "selected_example": "",
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ---------------------------------------------------------------------------
# Groq prompt enhancement
# ---------------------------------------------------------------------------

def enhance_prompt_with_groq(prompt: str, art_style: str) -> str:
    """Use Groq LLM to rewrite the prompt for richer image generation."""
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        return prompt

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert AI image prompt engineer. "
                    "Rewrite the user's prompt into a rich, vivid, detailed image generation prompt. "
                    "Keep it under 200 words. Output ONLY the enhanced prompt — no labels, no explanations."
                ),
            },
            {
                "role": "user",
                "content": f"Rewrite this prompt for a {art_style} style image:\n\n{prompt}",
            },
        ],
        "temperature": 0.7,
        "max_tokens": 300,
    }

    try:
        resp = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=15)
        if not resp.ok:
            st.warning(f"⚠️ Groq {resp.status_code}: {resp.json().get('error', {}).get('message', resp.text)}")
            return prompt
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as exc:
        st.warning(f"⚠️ Groq skipped ({exc}).")
        return prompt

# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def build_prompt(prompt: str, art_style: str, magic_enhance: bool, use_groq: bool) -> str:
    """Assemble the final prompt with optional Groq enhancement and magic keywords."""
    if use_groq:
        prompt = enhance_prompt_with_groq(prompt, art_style)
    full = f"{prompt}, {art_style} style"
    if magic_enhance:
        full += f", {MAGIC_ENHANCE_KEYWORDS}"
    return full


def build_image_url(prompt: str, width: int, height: int) -> str:
    """Return the Pollinations AI URL for the given prompt and dimensions."""
    return (
        f"{POLLINATIONS_BASE_URL}{urllib.parse.quote(prompt)}"
        f"?width={width}&height={height}&nologo=true"
    )


def fetch_image(url: str):
    """Fetch and return a PIL Image from the URL, or None on failure."""
    try:
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        return Image.open(io.BytesIO(resp.content))
    except requests.exceptions.RequestException as exc:
        st.error(f"❌ Image generation failed: {exc}")
        return None


def image_to_png_bytes(image) -> bytes:
    """Convert PIL Image to PNG bytes."""
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()


def generate_and_display(
    prompt: str, art_style: str, width: int, height: int,
    magic_enhance: bool, use_groq: bool,
) -> None:
    """Run the full generation pipeline and update session state."""
    with st.spinner("✨ Enhancing prompt with Groq AI…" if use_groq else "🎨 Building prompt…"):
        full_prompt = build_prompt(prompt, art_style, magic_enhance, use_groq)

    st.session_state["enhanced_prompt"] = full_prompt

    url = build_image_url(full_prompt, width, height)

    with st.spinner("🖼️ Generating image with Pollinations AI…"):
        image = fetch_image(url)

    if image is not None:
        st.session_state["generated_image"] = image
        st.session_state["current_art_style"] = art_style
        st.session_state["current_prompt"] = prompt
        st.session_state["total_generated"] += 1

        # Add to history (keep last 10)
        entry = {
            "prompt": prompt,
            "style": art_style,
            "time": datetime.now().strftime("%H:%M"),
        }
        history = st.session_state["prompt_history"]
        history.insert(0, entry)
        st.session_state["prompt_history"] = history[:10]

        st.success("✅ Image generated successfully!")

# ---------------------------------------------------------------------------
# ── SIDEBAR ──
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")

    # — Aspect ratio preset —
    st.markdown("**📐 Aspect Ratio**")
    ratio_choice = st.selectbox(
        "Preset",
        options=list(ASPECT_RATIOS.keys()),
        index=0,
        label_visibility="collapsed",
    )

    preset_dims = ASPECT_RATIOS[ratio_choice]
    if preset_dims:
        width, height = preset_dims
        st.caption(f"→ {width} × {height} px")
    else:
        width = st.slider("Width (px)", 256, 1024, 512, 64)
        height = st.slider("Height (px)", 256, 1024, 512, 64)

    st.markdown("---")

    # — Enhancements —
    st.markdown("**🪄 Enhancements**")
    use_groq = st.checkbox("🤖 Groq Prompt AI", value=True,
                           help="Let Groq rewrite your prompt for better results.")
    magic_enhance = st.checkbox("✨ Magic Enhance", value=False,
                                help="Append quality-boosting keywords.")

    if magic_enhance:
        st.caption("_Adds: masterpiece, 8k, cinematic lighting…_")

    st.markdown("---")

    # — Generation statistics —
    st.markdown("**📊 Session Stats**")
    total = st.session_state["total_generated"]
    fav_count = len(st.session_state["favourites"])
    hist_count = len(st.session_state["prompt_history"])

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-number">{total}</div>
            <div class="stat-label">Images Generated</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{fav_count}</div>
            <div class="stat-label">Favourites</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{hist_count}</div>
            <div class="stat-label">History Entries</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.caption("Powered by [Pollinations AI](https://pollinations.ai/) & [Groq](https://groq.com/)")

# ---------------------------------------------------------------------------
# ── MAIN AREA ──
# ---------------------------------------------------------------------------

# Gradient title
st.markdown(
    '<p class="gradient-title">🎨 AI Image Studio</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="subtitle">Generate stunning AI artwork — free, instant, no sign-up required.</p>',
    unsafe_allow_html=True,
)
st.markdown("---")

# ---------------------------------------------------------------------------
# Example prompt suggestions
# ---------------------------------------------------------------------------

st.markdown("**💡 Quick Prompts — click to use:**")
pill_html = '<div class="pill-container">'
for p in EXAMPLE_PROMPTS:
    pill_html += f'<span class="pill">✦ {p}</span>'
pill_html += "</div>"
st.markdown(pill_html, unsafe_allow_html=True)

# Selectbox approach so clicking a suggestion fills the prompt
example_choice = st.selectbox(
    "Or pick a suggestion:",
    options=["— type your own below —"] + EXAMPLE_PROMPTS,
    index=0,
    label_visibility="collapsed",
)

# ---------------------------------------------------------------------------
# Prompt input + art style
# ---------------------------------------------------------------------------

col_prompt, col_style = st.columns([3, 1])

with col_prompt:
    # Pre-fill from suggestion if chosen
    prefill = "" if example_choice.startswith("—") else example_choice
    user_prompt = st.text_input(
        "📝 Describe your image",
        value=prefill,
        placeholder="e.g. A futuristic city at sunset with flying cars",
        help="Groq AI will enrich your prompt automatically.",
    )

with col_style:
    art_style = st.selectbox("🎭 Art Style", options=ART_STYLES, index=0)

# ---------------------------------------------------------------------------
# Action buttons
# ---------------------------------------------------------------------------

b1, b2, b3 = st.columns(3)

with b1:
    generate_clicked = st.button("🎨 Generate Image", type="primary", use_container_width=True)
with b2:
    surprise_clicked = st.button("🎲 Surprise Me!", use_container_width=True)
with b3:
    fav_clicked = st.button("❤️ Save to Favourites", use_container_width=True)

# Handle Generate
if generate_clicked:
    if not user_prompt.strip():
        st.warning("⚠️ Please enter a prompt first.")
    else:
        generate_and_display(user_prompt.strip(), art_style, width, height, magic_enhance, use_groq)

# Handle Surprise Me
if surprise_clicked:
    rand_prompt = random.choice(SURPRISE_PROMPTS)
    st.info(f"🎲 Using: _{rand_prompt}_")
    generate_and_display(rand_prompt, art_style, width, height, magic_enhance, use_groq)

# Handle Favourite
if fav_clicked:
    p = user_prompt.strip() or st.session_state.get("current_prompt", "")
    if p:
        entry = {"prompt": p, "style": art_style}
        if entry not in st.session_state["favourites"]:
            st.session_state["favourites"].append(entry)
            st.success("❤️ Saved to favourites!")
        else:
            st.info("Already in favourites.")
    else:
        st.warning("Enter a prompt to save.")

# ---------------------------------------------------------------------------
# Generated image display
# ---------------------------------------------------------------------------

if st.session_state["generated_image"] is not None:
    st.markdown("---")

    img_col, info_col = st.columns([2, 1])

    with img_col:
        st.subheader("🖼️ Generated Image")
        st.image(
            st.session_state["generated_image"],
            caption=f"Style: {st.session_state['current_art_style']}",
        )

        safe_style = st.session_state["current_art_style"].replace(" ", "_")
        png_bytes = image_to_png_bytes(st.session_state["generated_image"])
        st.download_button(
            label="⬇️ Download PNG",
            data=png_bytes,
            file_name=f"{safe_style}_image.png",
            mime="image/png",
        )

    with info_col:
        st.subheader("📋 Image Details")
        st.markdown(f"**Style:** {st.session_state['current_art_style']}")
        st.markdown(f"**Size:** {width} × {height} px")
        st.markdown(f"**Ratio:** {ratio_choice}")

        if st.session_state["enhanced_prompt"]:
            with st.expander("🔍 Enhanced prompt", expanded=False):
                st.write(st.session_state["enhanced_prompt"])

# ---------------------------------------------------------------------------
# Prompt history & favourites tabs
# ---------------------------------------------------------------------------

st.markdown("---")
tab_hist, tab_fav = st.tabs(["📜 Prompt History", "❤️ Favourites"])

with tab_hist:
    history = st.session_state["prompt_history"]
    if not history:
        st.caption("No history yet — generate an image to start tracking.")
    else:
        for i, entry in enumerate(history):
            st.markdown(
                f'<div class="history-card">'
                f'<b>{entry["time"]}</b> &nbsp;|&nbsp; 🎭 {entry["style"]}<br>'
                f'{entry["prompt"]}'
                f'</div>',
                unsafe_allow_html=True,
            )
        if st.button("🗑️ Clear History"):
            st.session_state["prompt_history"] = []
            st.rerun()

with tab_fav:
    favs = st.session_state["favourites"]
    if not favs:
        st.caption("No favourites yet — click ❤️ Save to Favourites after typing a prompt.")
    else:
        for i, fav in enumerate(favs):
            col_text, col_del = st.columns([5, 1])
            with col_text:
                st.markdown(
                    f'<div class="fav-card">'
                    f'🎭 {fav["style"]}<br>{fav["prompt"]}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            with col_del:
                if st.button("✕", key=f"del_fav_{i}"):
                    st.session_state["favourites"].pop(i)
                    st.rerun()

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#6b7280; font-size:0.82rem;'>"
    "🎓 MirAI School of Technology · Virtual Summer Internship 2026 · AI Builder Track"
    "</div>",
    unsafe_allow_html=True,
)
