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
        st.image(str(header_img_path), use_column_width=True, output_format="auto")

st.title("🍁 September Fall Journal")
st.markdown("A cozy place to jot your thoughts — mood tags, prompts, and soft aesthetics.")

# layout
with st.sidebar:
    st.header("New Entry")
    date = st.date_input("Date", value=datetime.date.today())
    mood = st.selectbox("Mood", ["✨ Joyful", "😌 Calm", "😕 Meh", "😔 Sad", "🔥 Energized"])
    tags = st.text_input("Tags (comma separated)", placeholder="autumn,coffee,walks")
    entry_text = st.text_area("Write your entry...", height=160)
    
    st.markdown("---")
    st.subheader("🎨 Customize Journal")
    # Theme color picker
    primary_color = st.color_picker("Primary Color", value="#B86L36", key="primary_color")
    bg_color = st.color_picker("Background Color", value="#FFF8F1", key="bg_color")
    font_choice = st.selectbox("Font Style", ["Serif (Georgia)", "Sans Serif", "Monospace"], key="font_choice")
    emoji = st.text_input("Favorite Emoji for Entries", value="🍂", key="fav_emoji")
    show_header_img = st.checkbox("Show Header Image", value=True, key="show_header_img")
    
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
        st.success("Saved to your cozy journal! 🍯")
    # Store customization in session state
    st.session_state["custom_theme"] = {
        "primary_color": primary_color,
        "bg_color": bg_color,
        "font_choice": font_choice,
        "emoji": emoji,
        "show_header_img": show_header_img
    }

# prompts & quick actions
st.markdown("## ✨ Quick Prompts")
col1, col2 = st.columns(2)
with col1:
    if st.button("🌱 Prompt: 3 small wins today", key="prompt_wins"):
        st.info("List 3 tiny wins you had today — even if it's just 'made tea' ☕")
with col2:
    if st.button("🌻 Prompt: Gratitude", key="prompt_gratitude"):
        st.info("Write 3 people/ things you're grateful for today.")

# Add a spacer to avoid extra blank button row above entries
st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

# Apply custom theme (basic, for demo)
custom_theme = st.session_state.get("custom_theme", {})
if custom_theme:
    st.markdown(
        f"""
        <style>
        body {{
            background: {custom_theme.get('bg_color', '#FFF8F1')} !important;
        }}
        .stApp {{
            font-family: {"Georgia, serif" if custom_theme.get("font_choice")=="Serif (Georgia)" else "sans-serif" if custom_theme.get("font_choice")=="Sans Serif" else "monospace"};
        }}
        .journal-card {{
            border-left: 6px solid {custom_theme.get('primary_color', '#B86B36')};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# viewing entries
st.markdown("## Your Entries")
entries = st.session_state.get("entries", [])
if entries:
    for row in reversed(entries):
        emoji = row.get("emoji", custom_theme.get("emoji", "🍂"))
        st.markdown(f'<div class="journal-card">{emoji}', unsafe_allow_html=True)
        st.markdown(f"**{row.get('date','')}** · {row.get('mood','')}")
        if isinstance(row.get('tags', None), list):
            tags_line = " ".join([f"`{t}`" for t in row['tags']])
            st.markdown(f"<div class='small-muted'>{tags_line}</div>", unsafe_allow_html=True)
        st.markdown(row.get('text',''))
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("No journal entries yet — make your first one from the sidebar 🌾")

# footer
st.markdown("---")
st.markdown("Made with ❤️ • Fall vibes • Tips: Use the sidebar to save and optionally send to a backend.")
st.markdown('<div class="footer">🍂 Cozy Coding 2025</div>', unsafe_allow_html=True)
# End of app.py