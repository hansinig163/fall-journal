# app.py — Streamlit Fall Journal
import streamlit as st
import pandas as pd
import datetime
import requests
import json 
from pathlib import Path

st.set_page_config(page_title="September Fall Journal", page_icon="🍂", layout="centered")

# load css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

assets_dir = Path(__file__).parent / "assets"
css_file = assets_dir / "style.css"
if css_file.exists():
    local_css(css_file)

# header
if st.session_state.get("custom_theme", {}).get("show_header_img", True):
    header_img_path = assets_dir / "fall.jpg"
    if header_img_path.exists():
        import base64
        img_bytes = header_img_path.read_bytes()
        img_b64 = base64.b64encode(img_bytes).decode()
        st.markdown(
            f"""
            <div style="display:flex; justify-content:center; align-items:center; margin-bottom: -12px;">
                <div style="position:relative; width:60%;">
                    <img src="data:image/jpg;base64,{img_b64}" 
                         style="width:100%; height:160px; object-fit:cover; border-radius:24px; box-shadow:0 8px 32px rgba(186,107,54,0.18); border:4px solid #E2B07A;" />
                    <div style="position:absolute; top:10px; left:18px; font-size:2.2em;">🍁✨</div>
                    <div style="position:absolute; top:10px; right:18px; font-size:2.2em;">🎃💛</div>
                    <div style="position:absolute; bottom:10px; left:18px; font-size:2em;">🧡🍂</div>
                    <div style="position:absolute; bottom:10px; right:18px; font-size:2em;">💖🌟</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown(
    """
    <div style='display:flex; align-items:center; justify-content:center; margin-top: -10px; margin-bottom: 0;'>
        <span style='font-size:2.2em; margin-right:8px;'>🍁</span>
        <span style='font-size:2.2em; margin-right:8px;'>🎃</span>
        <span style='font-size:2.2em; margin-right:8px;'>✨</span>
        <span style='font-size:2.2em; margin-right:8px;'>🧡</span>
        <span style='font-size:2.2em;'>💖</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("🍁 September Fall Journal  ✨🎃")
st.markdown(
    "<div style='font-size:1.2em; color:#B86B36; font-family:Georgia,serif;'>"
    "A cozy place to jot your thoughts — mood tags, prompts, and soft aesthetics. "
    "<span style='font-size:1.3em;'>🍂🧡💖</span>"
    "</div>",
    unsafe_allow_html=True
)

# --- Login Section ---
if "user_email" not in st.session_state:
    st.markdown(
        "<div style='text-align:center; font-size:1.2em; margin-top:2em;'>"
        "🔒 <b>Welcome to your Fall Journal!</b> <br> Please log in with your email to access your private journal. <span style='font-size:1.3em;'>🍁✨</span>"
        "</div>",
        unsafe_allow_html=True
    )
    email = st.text_input("📧 Enter your email (Gmail recommended)", key="login_email")
    if st.button("🔑 Login", key="login_btn") and email and "@" in email:
        st.session_state["user_email"] = email.strip().lower()
        # Initialize user-specific entries on login
        user_key = f"entries_{st.session_state['user_email']}"
        if user_key not in st.session_state:
            st.session_state[user_key] = []
        st.success(f"Logged in as {email} 🍁")
    st.stop()

# layout
with st.sidebar:
    st.header("📝 New Entry  🍂✨")
    st.markdown(f"<div style='font-size:1em; color:#B86B36;'>Logged in as: <b>{st.session_state['user_email']}</b></div>", unsafe_allow_html=True)
    date = st.date_input("📅 Date", value=datetime.date.today())
    mood = st.selectbox("🌈 Mood", [
        "✨ Joyful 🧡", "😌 Calm 🍃", "😕 Meh 🍂", "😔 Sad 💧", "🔥 Energized 🎃"
    ])
    tags = st.text_input("🏷️ Tags (comma separated) 🎃", placeholder="autumn,coffee,walks,🍁,✨")
    entry_text = st.text_area("💬 Write your entry... 💖", height=160)

    st.markdown("---")
    st.subheader("🎨 Customize Journal Appearance 🍁")
    st.caption("Personalize your cozy fall journal! <span style='font-size:1.2em;'>🍂🎃✨💖</span>", unsafe_allow_html=True)

    st.markdown("**🍁 Colors & Style**")
    primary_color = st.color_picker("Primary Color 🎨", value="#B86B36", key="primary_color")
    accent_color = st.color_picker("Accent Color 🍯", value="#E2B07A", key="accent_color")
    bg_color = st.color_picker("Background Color 🌻", value="#FFF8F1", key="bg_color")
    font_choice = st.selectbox(
        "Font Style 🖋️",
        ["Serif (Georgia)", "Sans Serif", "Monospace", "Cursive", "Comic Sans"],
        key="font_choice"
    )
    font_size = st.slider("Font Size 🔠", min_value=14, max_value=24, value=17, step=1, key="font_size")
    # Replace shape selector with a border style selector
    border_style = st.selectbox(
        "Card Border Style 🖼️",
        ["Solid", "Dashed", "Dotted", "Double", "None"],
        key="border_style"
    )
    card_shadow = st.checkbox("Card Shadow 🌑", value=True, key="card_shadow")

    st.markdown("**✨ Entry Display Options**")
    emoji = st.text_input("Favorite Emoji for Entries 🥰", value="🍂", key="fav_emoji")
    show_header_img = st.checkbox("Show Header Image 🖼️", value=True, key="show_header_img")
    entry_order = st.radio("Entry Order ⏳", ["Newest First", "Oldest First"], key="entry_order")
    show_tags = st.checkbox("Show Tags 🏷️", value=True, key="show_tags")
    show_mood = st.checkbox("Show Mood 🌈", value=True, key="show_mood")
    show_date = st.checkbox("Show Date 📅", value=True, key="show_date")

    save_clicked = st.button("🍯✨ Save Entry 🎃", key="save_entry_btn")
    user_key = f"entries_{st.session_state['user_email']}"
    if save_clicked:
        entry = {
            "date": date.isoformat(),
            "mood": mood,
            "tags": [t.strip() for t in tags.split(",") if t.strip()],
            "text": entry_text,
            "emoji": emoji
        }
        st.session_state[user_key].append(entry)
        st.success(f"Saved to your cozy journal! 🍯✨🎃\n\n📅 Saved entry for: {date.strftime('%B %d, %Y')} <span style='font-size:1.3em;'>💖</span>", unsafe_allow_html=True)
    st.session_state["custom_theme"] = {
        "primary_color": primary_color,
        "bg_color": bg_color,
        "accent_color": accent_color,
        "font_choice": font_choice,
        "font_size": font_size,
        "emoji": emoji,
        "show_header_img": show_header_img,
        "border_style": border_style,
        "card_shadow": card_shadow,
        "entry_order": entry_order,
        "show_tags": show_tags,
        "show_mood": show_mood,
        "show_date": show_date
    }

# prompts & quick actions
st.markdown("## ✨ Quick Prompts 🍁")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🌱 Prompt: 3 small wins today 💖", key="prompt_wins"):
        st.info("🌱 List 3 tiny wins you had today — even if it's just 'made tea' ☕\n\n✨ You are doing great! 🍁")
    if st.button("🍂 Prompt: Cosy Autumn Memory", key="prompt_memory"):
        st.info("🍂 Write about your favorite autumn memory. Who were you with? What made it special? 🧡")
with col2:
    if st.button("🌻 Prompt: Gratitude 🎃", key="prompt_gratitude"):
        st.info("🌻 Write 3 people/ things you're grateful for today. 💛\n\n💖 Spread the love! 🍂")
    if st.button("🎃 Prompt: Pumpkin Spice Moment", key="prompt_pumpkin"):
        st.info("🎃 Describe a moment that felt like 'pumpkin spice' to you today—warm, comforting, or exciting!")
with col3:
    if st.button("💖 Prompt: Self-Care Sparkle", key="prompt_selfcare"):
        st.info("💖 What did you do for yourself today? Even a small act counts! ✨")
    if st.button("✨ Prompt: Dream for Tomorrow", key="prompt_dream"):
        st.info("✨ What's one thing you're looking forward to or dreaming about for tomorrow? 🌙")

# Add a spacer to avoid extra blank button row above entries
st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

# Apply custom theme (advanced fall stickers)
custom_theme = st.session_state.get("custom_theme", {})
# helpers for theme
font_map = {
    "Serif (Georgia)": "Georgia, serif",
    "Sans Serif": "Arial, sans-serif",
    "Monospace": "Courier New, monospace",
    "Cursive": "Brush Script MT, cursive",
    "Comic Sans": "'Comic Sans MS', cursive, sans-serif"
}

border_style_css = {
    "Solid": "solid",
    "Dashed": "dashed",
    "Dotted": "dotted",
    "Double": "double",
    "None": "none"
}

border_radius = "18px"
box_shadow = "0 6px 18px rgba(0,0,0,0.12)" if custom_theme.get("card_shadow", True) else "none"

if custom_theme:
    # Subtle plaid pattern: white and very light orange (#FFF8F1)
    # Sidebar: animated falling leaves background using emoji
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: #FFF8F1 !important;
            background-image:
                repeating-linear-gradient(0deg, #fff 0, #fff 2px, transparent 2px, transparent 40px),
                repeating-linear-gradient(90deg, #fff 0, #fff 2px, transparent 2px, transparent 40px),
                repeating-linear-gradient(0deg, #FFF8F1 0, #FFF8F1 1px, transparent 1px, transparent 20px),
                repeating-linear-gradient(90deg, #FFF8F1 0, #FFF8F1 1px, transparent 1px, transparent 20px);
            background-size: 40px 40px, 40px 40px, 20px 20px, 20px 20px;
            background-position: 0 0, 0 0, 0 0, 0 0;
            font-family: {font_map.get(custom_theme.get("font_choice"), "Georgia, serif")};
            font-size: {custom_theme.get("font_size", 17)}px;
        }}
        /* Sidebar with falling leaves effect */
        section[data-testid="stSidebar"] > div:first-child {{
            background: linear-gradient(135deg, #fffbe9 0%, #ffe7c2 100%);
            border-radius: 18px;
            box-shadow: 0 4px 24px rgba(186,107,54,0.10);
            padding-top: 12px;
            padding-bottom: 12px;
            position: relative;
            overflow: hidden;
        }}
        /* Falling leaves animation */
        @keyframes fall-leaf {{
            0% {{ transform: translateY(-40px) rotate(-10deg); opacity: 0.7; }}
            70% {{ opacity: 1; }}
            100% {{ transform: translateY(340px) rotate(30deg); opacity: 0.2; }}
        }}
        section[data-testid="stSidebar"] > div:first-child .fall-leaf {{
            position: absolute;
            left: 10%;
            font-size: 2em;
            opacity: 0.7;
            animation: fall-leaf 6s linear infinite;
            pointer-events: none;
        }}
        section[data-testid="stSidebar"] > div:first-child .fall-leaf2 {{
            left: 60%;
            font-size: 1.7em;
            animation-delay: 1.5s;
        }}
        section[data-testid="stSidebar"] > div:first-child .fall-leaf3 {{
            left: 35%;
            font-size: 2.3em;
            animation-delay: 3s;
        }}
        section[data-testid="stSidebar"] > div:first-child .fall-leaf4 {{
            left: 80%;
            font-size: 1.5em;
            animation-delay: 2.2s;
        }}
        .journal-card {{
            border-left: 8px {border_style_css.get(custom_theme.get('border_style', 'Solid'), 'solid')} {custom_theme.get('primary_color', '#B86B36')};
            border-radius: {border_radius};
            box-shadow: {box_shadow};
            background: linear-gradient(100deg, #FFF8F1 80%, #F5E3D0 100%);
            margin-bottom: 18px;
            position: relative;
            padding-bottom: 18px;
        }}
        .journal-card::after {{
            content: "🍁✨🎃";
            position: absolute;
            bottom: 8px;
            right: 18px;
            font-size: 1.5em;
            opacity: 0.22;
            pointer-events: none;
        }}
        .small-muted {{
            color: {custom_theme.get('accent_color', '#E2B07A')};
            font-size: 1em;
            font-style: italic;
        }}
        .stExpanderHeader {{
            font-size: 1.1em !important;
            font-weight: bold !important;
            color: {custom_theme.get('primary_color', '#B86B36')} !important;
        }}
        .stExpander {{
            border: 2px solid {custom_theme.get('accent_color', '#E2B07A')} !important;
            border-radius: 18px !important;
            background: #FFF8F1 !important;
        }}
        </style>
        <div class="fall-leaf" style="top:0; animation-duration: 6s;">🍁</div>
        <div class="fall-leaf fall-leaf2" style="top:-30px; animation-duration: 7s;">🍂</div>
        <div class="fall-leaf fall-leaf3" style="top:-60px; animation-duration: 8s;">🍃</div>
        <div class="fall-leaf fall-leaf4" style="top:-20px; animation-duration: 5.5s;">🍁</div>
        """,
        unsafe_allow_html=True
    )

# viewing entries
st.markdown("## 📖 Your Entries 🍁✨")
entries = st.session_state.get(user_key, [])
if entries:
    order = reversed(entries) if custom_theme.get("entry_order", "Newest First") == "Newest First" else entries
    for idx, row in enumerate(order):
        emoji = row.get("emoji", custom_theme.get("emoji", "🍂"))
        entry_label = []
        if custom_theme.get("show_date", True):
            entry_label.append(f"<span style='color:{custom_theme.get('accent_color', '#E2B07A')}; font-weight:bold;'>📅 {row.get('date','')}</span>")
        if custom_theme.get("show_mood", True):
            entry_label.append(f"<span style='color:{custom_theme.get('accent_color', '#E2B07A')};'>{row.get('mood','')}</span>")
        if custom_theme.get("show_tags", True) and isinstance(row.get('tags', None), list):
            tags_line = " ".join([f"<span style='color:{custom_theme.get('accent_color', '#E2B07A')};'>🏷️ `{t}`</span>" for t in row['tags']])
            entry_label.append(tags_line)
        label = " · ".join(entry_label) if entry_label else f"Entry {idx+1}"
        with st.expander(f"{emoji} 🍁🎃✨ {label} 💖", expanded=False):
            st.markdown(
                f"<div style='font-size:1.1em; font-weight:bold; margin-bottom:6px;'>"
                f"{label} <span style='font-size:1.2em;'>🧡✨</span></div>",
                unsafe_allow_html=True
            )
            # Entry text is now bold for visibility
            st.markdown(
                f"<div style='margin-top:8px; font-size:1.08em; font-weight:bold;'>💬 {row.get('text','')} <span style='font-size:1.2em;'>🎃🍁💖</span></div>",
                unsafe_allow_html=True
            )
else:
    st.info("No journal entries yet — make your first one from the sidebar 🌾✨🎃💖")

# footer
st.markdown("---")
st.markdown(
    "<div style='font-size:1.1em; text-align:center;'>"
    "Made with ❤ • Fall vibes 🍁🎃✨💖 • Tips: Use the sidebar to save and customize your journal!"
    "</div>",
    unsafe_allow_html=True
)
st.markdown('<div class="footer">🍂 Cozy Coding 2025 ✨🎃💖</div>', unsafe_allow_html=True)