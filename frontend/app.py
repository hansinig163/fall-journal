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
st.markdown("""
<div class="header">
  <img src="assets/header.jpg" style="width:100%; height:160px; object-fit:cover;" />
</div>
""", unsafe_allow_html=True)

st.title("🍁 September Fall Journal")
st.markdown("A cozy place to jot your thoughts — mood tags, prompts, and soft aesthetics.")

# layout
with st.sidebar:
    st.header("New Entry")
    date = st.date_input("Date", value=datetime.date.today())
    mood = st.selectbox("Mood", ["✨ Joyful", "😌 Calm", "😕 Meh", "😔 Sad", "🔥 Energized"])
    tags = st.text_input("Tags (comma separated)", placeholder="autumn,coffee,walks")
    entry_text = st.text_area("Write your entry...", height=160)
    # Only one cute Save button, no checkboxes for local/backend
    save_clicked = st.button("🍯 Save Entry", key="save_entry_btn")
    if save_clicked:
        entry = {
            "date": date.isoformat(),
            "mood": mood,
            "tags": [t.strip() for t in tags.split(",") if t.strip()],
            "text": entry_text
        }
        # Always save locally
        data_file = Path("journal_entries.json")
        if data_file.exists():
            df = pd.read_json(data_file)
            df = pd.concat([df, pd.json_normalize([entry])], ignore_index=True)
        else:
            df = pd.json_normalize([entry])
        df.to_json(data_file, orient="records", indent=2, date_format="iso")
        st.success("Saved to your cozy journal! 🍯")

# prompts & quick actions
st.markdown("## ✨ Quick Prompts")
col1, col2 = st.columns(2)
with col1:
    if st.button("🌱 Prompt: 3 small wins today", key="prompt_wins"):
        st.info("List 3 tiny wins you had today — even if it's just 'made tea' ☕")
with col2:
    if st.button("🌻 Prompt: Gratitude", key="prompt_gratitude"):
        st.info("Write 3 people/ things you're grateful for today.")

# viewing entries
st.markdown("## Your Entries")
data_file = Path("journal_entries.json")
if data_file.exists():
    df = pd.read_json(data_file)
    # show newest first
    df = df.sort_values("date", ascending=False).reset_index(drop=True)
    for _, row in df.iterrows():
        st.markdown('<div class="journal-card">', unsafe_allow_html=True)
        st.markdown(f"**{row.get('date','')}** · {row.get('mood','')}")
        if isinstance(row.get('tags', None), list):
            tags_line = " ".join([f"`{t}`" for t in row['tags']])
            st.markdown(f"<div class='small-muted'>{tags_line}</div>", unsafe_allow_html=True)
        st.markdown(row.get('text',''))
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("No journal entries yet — make your first one from the sidebar 🌾")

# small export button
if data_file.exists():
    st.download_button("Download JSON", data=data_file.read_text(), file_name="journal_entries.json", mime="application/json")

# footer
st.markdown("---")
st.markdown("Made with ❤️ • Fall vibes • Tips: Use the sidebar to save and optionally send to a backend.")
st.markdown('<div class="footer">🍂 Cozy Coding 2024</div>', unsafe_allow_html=True)
# End of app.py