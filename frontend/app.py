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
        st.image(str(header_img_path), use_column_width=True, output_format="auto", clamp=False)
        st.markdown(
            """
            <style>
            .element-container img {
                border-radius: 12px !important;
                object-fit: cover !important;
                height: 160px !important;
                width: 100% !important;
                display: block;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

st.title("🍁 September Fall Journal")
st.markdown("A cozy place to jot your thoughts — mood tags, prompts, and soft aesthetics. 🍂✨")

# layout
with st.sidebar:
    st.header("📝 New Entry")
    date = st.date_input("📅 Date", value=datetime.date.today())
    mood = st.selectbox("🌈 Mood", ["✨ Joyful", "😌 Calm", "😕 Meh", "😔 Sad", "🔥 Energized"])
    tags = st.text_input("🏷️ Tags (comma separated)", placeholder="autumn,coffee,walks")
    entry_text = st.text_area("💬 Write your entry...", height=160)
    
    st.markdown("---")
    st.subheader("🎨 Customize Journal")
    # Theme color picker
    primary_color = st.color_picker("Primary Color 🎨", value="#B86B36", key="primary_color")
    bg_color = st.color_picker("Background Color 🌻", value="#FFF8F1", key="bg_color")
    accent_color = st.color_picker("Accent Color 🍯", value="#E2B07A", key="accent_color")
    font_choice = st.selectbox(
        "Font Style 🖋️",
        ["Serif (Georgia)", "Sans Serif", "Monospace", "Cursive", "Comic Sans"],
        key="font_choice"
    )
    font_size = st.slider("Font Size 🔠", min_value=14, max_value=24, value=17, step=1, key="font_size")
    emoji = st.text_input("Favorite Emoji for Entries 🥰", value="🍂", key="fav_emoji")
    show_header_img = st.checkbox("Show Header Image 🖼️", value=True, key="show_header_img")
    card_shape = st.selectbox("Card Shape 🃏", ["Rounded", "Sharp", "Circle"], key="card_shape")
    card_shadow = st.checkbox("Card Shadow 🌑", value=True, key="card_shadow")
    entry_order = st.radio("Entry Order ⏳", ["Newest First", "Oldest First"], key="entry_order")
    show_tags = st.checkbox("Show Tags 🏷️", value=True, key="show_tags")
    show_mood = st.checkbox("Show Mood 🌈", value=True, key="show_mood")
    show_date = st.checkbox("Show Date 📅", value=True, key="show_date")
    
    # Save button
    save_clicked = st.button("🍯 Save Entry", key="save_entry_btn")
    if save_clicked:
        entry = {
            "date": date.isoformat(),
            "mood": mood,
            "tags": [t.strip() for t in tags.split(",") if t.strip()],
            "text": entry_text,
            "emoji": emoji
        }
        if "entries" not in st.session_state:
            st.session_state["entries"] = []
        st.session_state["entries"].append(entry)
        st.success("Saved to your cozy journal! 🍯✨")
    # Store customization in session state
    st.session_state["custom_theme"] = {
        "primary_color": primary_color,
        "bg_color": bg_color,
        "accent_color": accent_color,
        "font_choice": font_choice,
        "font_size": font_size,
        "emoji": emoji,
        "show_header_img": show_header_img,
        "card_shape": card_shape,
        "card_shadow": card_shadow,
        "entry_order": entry_order,
        "show_tags": show_tags,
        "show_mood": show_mood,
        "show_date": show_date
    }

# prompts & quick actions
st.markdown("## ✨ Quick Prompts")
col1, col2 = st.columns(2)
with col1:
    if st.button("🌱 Prompt: 3 small wins today", key="prompt_wins"):
        st.info("🌱 List 3 tiny wins you had today — even if it's just 'made tea' ☕")
with col2:
    if st.button("🌻 Prompt: Gratitude", key="prompt_gratitude"):
        st.info("🌻 Write 3 people/ things you're grateful for today.")

# Add a spacer to avoid extra blank button row above entries
st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

# Apply custom theme (basic, for demo)
custom_theme = st.session_state.get("custom_theme", {})
if custom_theme:
    font_map = {
        "Serif (Georgia)": "Georgia, serif",
        "Sans Serif": "sans-serif",
        "Monospace": "monospace",
        "Cursive": "cursive",
        "Comic Sans": "'Comic Sans MS', cursive, sans-serif"
    }
    border_radius = {
        "Rounded": "16px",
        "Sharp": "0px",
        "Circle": "32px"
    }
    box_shadow = "0 6px 18px rgba(186,107,54,0.08)" if custom_theme.get("card_shadow", True) else "none"
    st.markdown(
        f"""
        <style>
        body {{
            background: {custom_theme.get('bg_color', '#FFF8F1')} !important;
        }}
        .stApp {{
            font-family: {font_map.get(custom_theme.get("font_choice"), "Georgia, serif")};
            font-size: {custom_theme.get("font_size", 17)}px;
        }}
        .journal-card {{
            border-left: 6px solid {custom_theme.get('primary_color', '#B86B36')};
            border-radius: {border_radius.get(custom_theme.get("card_shape", "Rounded"), "16px")};
            box-shadow: {box_shadow};
        }}
        .small-muted {{
            color: {custom_theme.get('accent_color', '#E2B07A')};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# viewing entries
st.markdown("## 📖 Your Entries")
entries = st.session_state.get("entries", [])
if entries:
    order = reversed(entries) if custom_theme.get("entry_order", "Newest First") == "Newest First" else entries
    for row in order:
        emoji = row.get("emoji", custom_theme.get("emoji", "🍂"))
        st.markdown(f'<div class="journal-card">{emoji} ', unsafe_allow_html=True)
        line = []
        if custom_theme.get("show_date", True):
            line.append(f"📅 **{row.get('date','')}**")
        if custom_theme.get("show_mood", True):
            line.append(f"{row.get('mood','')}")
        st.markdown(" · ".join(line))
        if custom_theme.get("show_tags", True) and isinstance(row.get('tags', None), list):
            tags_line = " ".join([f"🏷️ `{t}`" for t in row['tags']])
            st.markdown(f"<div class='small-muted'>{tags_line}</div>", unsafe_allow_html=True)
        st.markdown(f"💬 {row.get('text','')}")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("No journal entries yet — make your first one from the sidebar 🌾✨")

# footer
st.markdown("---")
st.markdown("Made with ❤️ • Fall vibes 🍁 • Tips: Use the sidebar to save and customize your journal!")
st.markdown('<div class="footer">🍂 Cozy Coding 2025 ✨</div>', unsafe_allow_html=True)
# End of app.py