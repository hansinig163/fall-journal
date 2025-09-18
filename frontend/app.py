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

st.title("🍁 September Fall Journal  ✨")
st.markdown(
    "<div style='font-size:1.2em; color:#B86L36; font-family:Georgia,serif;'>"
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
    # Move sidebar contents up
    st.markdown(
        """
        <div style='margin-top:-32px;'>
        """,
        unsafe_allow_html=True
    )
    # Centered, bigger "New Entry" header
    st.markdown(
        """
        <div style='text-align:center; font-size:2em; font-weight:bold; color:#B86B36; margin-bottom:8px; margin-top:2px;'>
            📝 New Entry  🍂✨
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='font-size:1em; color:#B86B36; text-align:center;'>Logged in as: <b>{st.session_state['user_email']}</b></div>",
        unsafe_allow_html=True
    )

    # "Pick a Date for Your Memory" as small text, not in a box, with pixel art/gif and leaf emojis
    st.markdown(
        """
        <div style='
            font-size:0.95em;
            color:#E2B07A;
            font-family:Georgia,serif;
            margin-bottom:2px;
            margin-top:10px;
            display:flex;
            align-items:center;
            justify-content:center;
            gap:8px;
        '>
            🍁 <img src="https://em-content.zobj.net/thumbs/120/twitter/351/maple-leaf_1f341.png" width="28" style="vertical-align:middle; margin-bottom:2px;" />
            <b>Pick a Date for Your Memory</b>
            <img src="https://media.giphy.com/media/3o7TKtnuHOHHUjR38Y/giphy.gif" width="32" style="vertical-align:middle; margin-bottom:2px; border-radius:6px;" />
            🍂
        </div>
        <div style='text-align:center; margin-bottom:2px;'>
            <img src="https://www.pixelartcss.com/images/leaf-pixel-art.gif" width="60" style="margin:2px 0 4px 0; border-radius:8px;" />
        </div>
        """,
        unsafe_allow_html=True
    )
    date = st.date_input(
        "Pick a Date",
        value=datetime.date.today(),
        key="date_input",
        label_visibility="collapsed"
    )

    mood = st.selectbox("🌈 Mood", [
        "✨ Joyful 🧡", "😌 Calm 🍃", "😕 Meh 🍂", "😔 Sad 💧", "🔥 Energized 🎃"
    ])
    tags = st.text_input("🏷️ Tags (comma separated) 🎃", placeholder="autumn,coffee,walks,🍁,✨")
    entry_text = st.text_area("💬 Write your entry... 💖", height=160)
    
    # Small, cute Save Entry button inside the entry box area
    st.markdown(
        """
        <div style='text-align:center; margin-top:-10px; margin-bottom:8px;'>
            <style>
            .cute-save-btn {
                background: linear-gradient(90deg, #ffe7c2 60%, #fffbe9 100%);
                border: 1.5px solid #E2B07A;
                border-radius: 12px;
                color: #B86B36;
                font-size: 1em;
                font-weight: bold;
                padding: 0.3em 1em;
                margin-top: 2px;
                margin-bottom: 2px;
                box-shadow: 0 1px 6px rgba(186,107,54,0.10);
                cursor: pointer;
                transition: 0.2s;
            }
            </style>
        </div>
        """,
        unsafe_allow_html=True
    )
    font_choice, accent_color = st.columns(2)
    with font_choice:
        font_val = st.selectbox(
            "Font Style 🖋️",
            ["Serif (Georgia)", "Sans Serif", "Monospace", "Cursive", "Comic Sans"],
            index=["Serif (Georgia)", "Sans Serif", "Monospace", "Cursive", "Comic Sans"].index(
                st.session_state.get("custom_theme", {}).get("font_choice", "Serif (Georgia)")
            ) if st.session_state.get("custom_theme", {}).get("font_choice") else 0,
            key="font_choice"
        )
    with accent_color:
        accent_val = st.color_picker(
            "Accent Color 🍯",
            value=st.session_state.get("custom_theme", {}).get("accent_color", "#E2B07A"),
            key="accent_color"
        )
    st.markdown("---")

    user_key = f"entries_{st.session_state['user_email']}"
    if user_key not in st.session_state:
        st.session_state[user_key] = []
    save_clicked = st.button(
        label="🍯 Save Entry 💖",
        key="save_entry_btn",
        help="Save your cozy memory!",
        use_container_width=False,
        type="secondary",
        # Add custom class for pixel style
        args=(),
        kwargs={},
        on_click=None,
        disabled=False
    )
    # Patch the button to have the pixel-art class (Streamlit workaround)
    st.markdown(
        """
        <script>
        const btns = window.parent.document.querySelectorAll('button[kind="secondary"]');
        btns.forEach(btn => {
            if (!btn.classList.contains('cute-save-btn')) {
                btn.classList.add('cute-save-btn');
            }
        });
        </script>
        """,
        unsafe_allow_html=True
    )
    if save_clicked:
        entry = {
            "date": date.strftime("%Y-%m-%d"),
            "mood": mood,
            "tags": [t.strip() for t in tags.split(",") if t.strip()],
            "text": entry_text,
            "emoji": st.session_state.get("custom_theme", {}).get("emoji", "🍂")
        }
        st.session_state[user_key].append(entry)
        st.success(f"Saved to your cozy journal! 🍯✨💖🧡\n\n📅 Saved entry for: {date.strftime('%B %d, %Y')} 💖🍁✨")
    # Fix: set accent_val and font_val before using them in custom_theme
    st.session_state["custom_theme"] = {
        "emoji": st.session_state.get("custom_theme", {}).get("emoji", "🍂"),
        "accent_color": accent_val,
        "font_choice": font_val
    }
    st.markdown("</div>", unsafe_allow_html=True)

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
    st.markdown(
        f"""
        <style>
        .stApp {{
            /* Plaid background only, no background-color override */
            background-image:
                repeating-linear-gradient(0deg, #fff 0, #fff 4px, transparent 4px, transparent 40px),
                repeating-linear-gradient(90deg, #fff 0, #fff 4px, transparent 4px, transparent 40px),
                repeating-linear-gradient(0deg, #FFE5B4 0, #FFE5B4 2px, transparent 2px, transparent 20px),
                repeating-linear-gradient(90deg, #FFE5B4 0, #FFE5B4 2px, transparent 2px, transparent 20px);
            background-size: 40px 40px, 40px 40px, 20px 20px, 20px 20px;
            background-position: 0 0, 0 0, 0 0, 0 0;
            font-family: {font_map.get(custom_theme.get("font_choice"), "Georgia, serif")};
            font-size: {custom_theme.get("font_size", 17) if "font_size" in custom_theme else 17}px;
        }}
        section[data-testid="stSidebar"] > div:first-child {{
            background: linear-gradient(135deg, #fffbe9 0%, #ffe7c2 100%);
            border-radius: 18px;
            box-shadow: 0 4px 24px rgba(186,107,54,0.10);
            padding-top: 12px;
            padding-bottom: 12px;
            position: relative;
            overflow: visible !important;
            display: flex;
            flex-direction: column;
            height: 100vh !important;
        }}
        .stSidebarContent {{
            flex: 1 1 auto !important;
            height: 100% !important;
            max-height: 100vh !important;
            overflow-y: auto !important;
            padding-bottom: 60px;
            scrollbar-width: auto;
            scrollbar-color: #E2B07A #F5E3D0;
            background: transparent;
        }}
        .stSidebarContent::-webkit-scrollbar {{
            width: 12px;
            background: #F5E3D0;
            border-radius: 8px;
            display: block;
        }}
        .stSidebarContent::-webkit-scrollbar-thumb {{
            background: #E2B07A;
            border-radius: 8px;
            min-height: 40px;
        }}
        .stSidebarContent::-webkit-scrollbar-thumb:hover {{
            background: #B86B36;
        }}
        /* Ensure sidebar is always scrollable */
        section[data-testid="stSidebar"] > div:first-child,
        section[data-testid="stSidebar"] .block-container {{
            overflow-y: auto !important;
            max-height: 100vh !important;
        }}
        /* Fallback for older Streamlit: */
        section[data-testid="stSidebar"] .block-container {{
            height: 100% !important;
            max-height: 100vh !important;
            overflow-y: auto !important;
        }}
        section[data-testid="stSidebar"] .block-container::-webkit-scrollbar {{
            width: 12px;
            background: #F5E3D0;
            border-radius: 8px;
            display: block;
        }}
        section[data-testid="stSidebar"] .block-container::-webkit-scrollbar-thumb {{
            background: #E2B07A;
            border-radius: 8px;
            min-height: 40px;
        }}
        section[data-testid="stSidebar"] .block-container::-webkit-scrollbar-thumb:hover {{
            background: #B86B36;
        }}
        /* Falling leaves animation */
        @keyframes fall-leaf {{
            0% {{ transform: translateY(-60px) rotate(-10deg); opacity: 0.8; }}
            70% {{ opacity: 1; }}
            100% {{ transform: translateY(420px) rotate(30deg); opacity: 0.2; }}
        }}
        .fall-leaf {{
            position: absolute;
            z-index: 10;
            pointer-events: none;
            animation: fall-leaf 7s linear infinite;
        }}
        .fall-leaf1 {{ left: 10%; font-size: 2em; animation-delay: 0s; }}
        .fall-leaf2 {{ left: 60%; font-size: 1.7em; animation-delay: 1.5s; }}
        .fall-leaf3 {{ left: 35%; font-size: 2.3em; animation-delay: 3s; }}
        .fall-leaf4 {{ left: 80%; font-size: 1.5em; animation-delay: 2.2s; }}
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
        .stSidebarContent label, .stSidebarContent .css-1cpxqw2, .stSidebarContent .css-1v0mbdj {{
            color: {custom_theme.get("accent_color", "#E2B07A")} !important;
            font-family: {font_map.get(custom_theme.get("font_choice"), "Georgia, serif")} !important;
        }}
        </style>
        <div class="fall-leaf fall-leaf1" style="top:0; animation-duration: 7s;">🍁</div>
        <div class="fall-leaf fall-leaf2" style="top:-30px; animation-duration: 8s;">🍂</div>
        <div class="fall-leaf fall-leaf3" style="top:-60px; animation-duration: 9s;">🍃</div>
        <div class="fall-leaf fall-leaf4" style="top:-20px; animation-duration: 6.5s;">🍁</div>
        """,
        unsafe_allow_html=True
    )

# viewing entries
st.markdown("## 📖 Your Entries 🍁✨")
entries = st.session_state.get(user_key, [])
if entries:
    order = list(reversed(entries)) if custom_theme.get("entry_order", "Newest First") == "Newest First" else list(entries)
    font_css = font_map.get(custom_theme.get("font_choice"), "Georgia, serif")
    accent = custom_theme.get('accent_color', '#E2B07A')
    for idx, row in enumerate(order):
        emoji = row.get("emoji", custom_theme.get("emoji", "🍂"))
        date_str = row.get('date', '')
        tags_list = row.get('tags', [])
        mood_str = row.get('mood', '')
        expander_label = f"{emoji}  📅 {date_str}"
        with st.expander(expander_label, expanded=False):
            # Show mood as a subheading if present
            if mood_str:
                st.markdown(
                    f"<div style='margin-bottom:4px; margin-top:2px; font-size:1.08em; color:{accent}; font-family:{font_css}; font-weight:600;'>"
                    f"{mood_str}</div>",
                    unsafe_allow_html=True
                )
            # Show tags as a subheading if present
            if tags_list:
                tags_str = " ".join([
                    f"<span style='background:#ffe7c2; color:#B86B36; border-radius:8px; padding:2px 10px; margin-right:6px; font-size:1em; font-family:{font_css}; font-weight:600; display:inline-block;'>🏷️ {t}</span>"
                    for t in tags_list
                ])
                st.markdown(
                    f"<div style='margin-bottom:8px; margin-top:2px;'>{tags_str}</div>",
                    unsafe_allow_html=True
                )
            st.markdown(
                f"<div style='margin-top:8px; font-size:1.08em; font-weight:bold; font-family:{font_css};'>💬 {row.get('text','')}</div>",
                unsafe_allow_html=True
            )
            # Delete button
            col_del = st.columns([0.7, 0.3])
            with col_del[1]:
                if st.button("🗑️ Delete", key=f"delete_entry_{idx}"):
                    real_idx = len(entries) - 1 - idx if custom_theme.get("entry_order", "Newest First") == "Newest First" else idx
                    st.session_state[user_key].pop(real_idx)
                    st.rerun()
                    break
else:
    st.info("No journal entries yet — make your first one from the sidebar 🌾✨🎃💖")

# For pixel-art style delete button inside entry expander
# (This will style all Streamlit buttons with the 🗑️ label in the expander)
st.markdown(
    """
    <style>
    .stButton>button:has(span:contains('🗑️')) {
        background: url('https://www.pixelartcss.com/images/pixel-button-bg.png'), linear-gradient(90deg, #ffe7c2 60%, #fffbe9 100%);
        background-size: cover, 100% 100%;
        border: 2.5px solid #B86B36;
        border-radius: 8px;
        color: #B86B36;
        font-size: 1.08em;
        font-family: 'Press Start 2P', 'Comic Sans MS', cursive, sans-serif;
        font-weight: bold;
        padding: 0.4em 1.1em;
        margin-top: 2px;
        margin-bottom: 2px;
        box-shadow: 0 2px 8px rgba(186,107,54,0.18), 0 0 0 4px #ffe7c2 inset;
        cursor: pointer;
        transition: 0.2s;
        outline: none !important;
        text-shadow: 1px 1px #fffbe9, 2px 2px #E2B07A;
        letter-spacing: 1px;
    }
    .stButton>button:has(span:contains('🗑️')):hover {
        background: url('https://www.pixelartcss.com/images/pixel-button-bg.png'), linear-gradient(90deg, #ffe7c2 60%, #ffe7c2 100%);
        filter: brightness(1.08);
        border-color: #ffb347;
    }
    </style>
    """,
    unsafe_allow_html=True
)