# app.py — Streamlit Fall Journal
import streamlit as st
import pandas as pd
import datetime
import requests
import json
from pathlib import Path
import os
import hashlib

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

USERS_FILE = Path(__file__).parent / "users.json"

def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    users[username] = hash_password(password)
    save_users(users)
    return True, "Registration successful!"

def login_user(username, password):
    users = load_users()
    if username in users and users[username] == hash_password(password):
        return True
    return False

def logout_user():
    st.session_state.pop("user", None)

# --- Pastel Fall-Themed Login UI with Lo-fi Music ---
def login_ui():
    st.markdown(
        """
        <style>
        body, .stApp {
            background: linear-gradient(120deg, #fffbe9 0%, #ffe7c2 100%);
        }
        .pastel-login-bg {
            min-height: 100vh;
            width: 100vw;
            position: fixed;
            top: 0; left: 0;
            z-index: 0;
            background: linear-gradient(120deg, #fffbe9 0%, #ffe7c2 100%);
            overflow: hidden;
        }
        .pastel-login-card {
            background: rgba(255, 250, 235, 0.98);
            border-radius: 28px;
            box-shadow: 0 8px 32px rgba(186,107,54,0.10), 0 0 0 8px #ffe7c2 inset;
            padding: 2.5em 2em 2em 2em;
            max-width: 370px;
            margin: 60px auto 0 auto;
            border: 2.5px solid #f7e3c2;
            position: relative;
        }
        .pastel-login-card h2 {
            font-family: 'Comic Sans MS', 'Georgia', cursive, sans-serif;
            color: #b97a56;
            font-size: 1.6em;
            text-align: center;
            margin-bottom: 0.7em;
        }
        .pastel-login-card label, .pastel-login-card input {
            font-family: 'Comic Sans MS', 'Georgia', cursive, sans-serif;
        }
        .pastel-login-card input {
            width: 100%;
            padding: 0.7em 1.2em;
            margin-bottom: 1.1em;
            border-radius: 12px;
            border: 2px solid #f7e3c2;
            background: #fffbe9;
            font-size: 1.1em;
            color: #b97a56;
            outline: none;
            transition: border 0.2s;
        }
        .pastel-login-card input:focus {
            border: 2px solid #e2b07a;
            background: #fff7e0;
        }
        .pastel-login-btn {
            width: 100%;
            background: linear-gradient(90deg, #ffd9a0 60%, #ffe7c2 100%);
            color: #b97a56;
            font-size: 1.15em;
            font-family: 'Comic Sans MS', 'Georgia', cursive, sans-serif;
            font-weight: bold;
            border: none;
            border-radius: 16px;
            padding: 0.7em 0;
            margin-top: 0.2em;
            margin-bottom: 0.2em;
            box-shadow: 0 2px 8px rgba(186,107,54,0.10), 0 0 0 4px #ffe7c2 inset;
            cursor: pointer;
            transition: 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        .pastel-login-btn:hover {
            background: linear-gradient(90deg, #ffe7c2 60%, #ffd9a0 100%);
            filter: brightness(1.06);
        }
        .pastel-login-card .emoji-header {
            font-size: 2.2em;
            text-align: center;
            margin-bottom: 0.2em;
        }
        /* Falling pastel leaves animation */
        .fall-leaf-pastel {
            position: fixed;
            z-index: 1;
            pointer-events: none;
            animation: fall-leaf-pastel 8s linear infinite;
            opacity: 0.7;
        }
        @keyframes fall-leaf-pastel {
            0% { transform: translateY(-60px) rotate(-10deg); opacity: 0.7; }
            70% { opacity: 1; }
            100% { transform: translateY(100vh) rotate(30deg); opacity: 0.2; }
        }
        .fall-leaf-pastel1 { left: 12%; font-size: 2.1em; animation-delay: 0s; }
        .fall-leaf-pastel2 { left: 55%; font-size: 1.7em; animation-delay: 2s; }
        .fall-leaf-pastel3 { left: 35%; font-size: 2.5em; animation-delay: 3.5s; }
        .fall-leaf-pastel4 { left: 80%; font-size: 1.5em; animation-delay: 1.2s; }
        .fall-leaf-pastel5 { left: 25%; font-size: 1.8em; animation-delay: 4.2s; }
        </style>
        <div class="pastel-login-bg"></div>
        <div class="fall-leaf-pastel fall-leaf-pastel1">🍂</div>
        <div class="fall-leaf-pastel fall-leaf-pastel2">🍁</div>
        <div class="fall-leaf-pastel fall-leaf-pastel3">🌰</div>
        <div class="fall-leaf-pastel fall-leaf-pastel4">🍃</div>
        <div class="fall-leaf-pastel fall-leaf-pastel5">🍂</div>
        """,
        unsafe_allow_html=True
    )
    # Lo-fi/fall music (autoplay, loop, hidden controls)
    st.markdown(
        """
        <audio id="lofi-music" src="https://cdn.pixabay.com/audio/2022/10/16/audio_12b6b6e2e6.mp3" autoplay loop>
        </audio>
        <script>
        // Ensure music continues after login (if possible)
        window.addEventListener('DOMContentLoaded', function() {
            var audio = document.getElementById('lofi-music');
            if (audio) { audio.volume = 0.25; }
        });
        </script>
        """,
        unsafe_allow_html=True
    )
    tab_login, tab_register = st.tabs(["☕ Login", "🍁 Register"])
    with tab_login:
        st.markdown(
            """
            <div class="pastel-login-card">
                <div class="emoji-header">☕🍂🍁🌰</div>
                <h2>Welcome Back!</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
        username = st.text_input("👤 Username", key="login_username", placeholder="👤 username")
        password = st.text_input("🔑 Password", type="password", key="login_password", placeholder="🔑 password")
        login_btn = st.button("☕  Login", key="login_btn", help="Login to your cozy journal!", use_container_width=True)
        if login_btn:
            if login_user(username, password):
                st.session_state["user"] = username
                st.success("Login successful! 🍁")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password.")
    with tab_register:
        st.markdown(
            """
            <div class="pastel-login-card">
                <div class="emoji-header">🍁🍂🌰☕</div>
                <h2>Register for Cozy Journal</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
        new_username = st.text_input("👤 New Username", key="register_username", placeholder="👤 new username")
        new_password = st.text_input("🔑 New Password", type="password", key="register_password", placeholder="🔑 new password")
        register_btn = st.button("☕  Register", key="register_btn", help="Create your cozy account!", use_container_width=True)
        if register_btn:
            ok, msg = register_user(new_username, new_password)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

def require_login():
    if "user" not in st.session_state:
        login_ui()
        st.stop()
    # Create user folder if not exists
    user_folder = Path(__file__).parent.parent / "journal_entries" / st.session_state["user"]
    user_folder.mkdir(parents=True, exist_ok=True)

def show_logout():
    if "user" in st.session_state:
        if st.button("🚪 Logout", key="logout_btn"):
            logout_user()
            st.experimental_rerun()

# --- Replace old login logic ---
require_login()
user_key = f"entries_{st.session_state['user']}"
if user_key not in st.session_state:
    st.session_state[user_key] = []

# Load user's journal entries from their folder
def load_journal_entries(username):
    entries_dir = Path(__file__).parent.parent / "journal_entries" / username
    if not entries_dir.exists():
        return []
    entries = []
    for file in sorted(entries_dir.glob("*.txt"), reverse=True):
        try:
            with open(file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                title = ""
                content = ""
                if lines and lines[0].startswith("Title:"):
                    title = lines[0].replace("Title:", "").strip()
                    content = "".join(lines[2:]).strip() if len(lines) > 2 else ""
                else:
                    title = file.stem
                    content = "".join(lines).strip()
                date_part = file.name.split("-entry.txt")[0]
                entries.append({
                    "filename": str(file),
                    "date": date_part,
                    "title": title,
                    "content": content
                })
        except Exception:
            continue
    return entries

st.session_state[user_key] = load_journal_entries(st.session_state["user"])

# --- PIXEL ART UI THEME ---

st.markdown(
    """
    <style>
    /* Pixel-art wooden shelf sidebar */
    section[data-testid="stSidebar"] > div:first-child {
        background: url('https://i.imgur.com/6Q8QvQj.png') repeat, linear-gradient(135deg, #e7c49a 0%, #b97a56 100%);
        background-size: 80px 80px, 100% 100%;
        border: 4px solid #a05a2c;
        border-radius: 18px;
        box-shadow: 0 4px 24px rgba(186,107,54,0.18), 0 0 0 8px #e7c49a inset;
        padding-top: 12px;
        padding-bottom: 12px;
        position: relative;
        overflow: visible !important;
        display: flex;
        flex-direction: column;
        height: 100vh !important;
    }
    .stSidebarContent {
        flex: 1 1 auto !important;
        height: 100% !important;
        max-height: 100vh !important;
        overflow-y: auto !important;
        padding-bottom: 60px;
        scrollbar-width: auto;
        scrollbar-color: #B86L36 #e7c49a;
        background: transparent;
    }
    .stSidebarContent::-webkit-scrollbar {
        width: 12px;
        background: #e7c49a;
        border-radius: 8px;
        display: block;
    }
    .stSidebarContent::-webkit-scrollbar-thumb {
        background: #B86L36;
        border-radius: 8px;
        min-height: 40px;
    }
    .stSidebarContent::-webkit-scrollbar-thumb:hover {
        background: #a05a2c;
    }

    /* Pixel notebook page main area */
    .stApp {
        background: url('https://i.imgur.com/2QbQZbK.png') repeat, linear-gradient(0deg, #fffbe9 0%, #ffe7c2 100%);
        background-size: 120px 120px, 100% 100%;
        font-family: 'Press Start 2P', 'Comic Sans MS', cursive, sans-serif;
        font-size: 17px;
    }
    .pixel-notebook {
        background: url('https://i.imgur.com/2QbQZbK.png') repeat, #fffbe9;
        border: 4px solid #e2b07a;
        border-radius: 18px;
        box-shadow: 0 6px 18px rgba(186,107,54,0.12), 0 0 0 8px #ffe7c2 inset;
        padding: 32px 24px 24px 24px;
        margin-bottom: 32px;
        margin-top: 12px;
        min-height: 320px;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        position: relative;
    }
    /* Pixel-art buttons */
    .pixel-btn {
        background: url('https://i.imgur.com/6Q8QvQj.png') repeat, linear-gradient(90deg, #ffe7c2 60%, #fffbe9 100%);
        background-size: 40px 40px, 100% 100%;
        border: 3px solid #a05a2c;
        border-radius: 8px;
        color: #B86L36;
        font-size: 1.08em;
        font-family: 'Press Start 2P', 'Comic Sans MS', cursive, sans-serif;
        font-weight: bold;
        padding: 0.5em 1.2em;
        margin-top: 2px;
        margin-bottom: 2px;
        box-shadow: 0 2px 8px rgba(186,107,54,0.18), 0 0 0 4px #ffe7c2 inset;
        cursor: pointer;
        transition: 0.2s;
        outline: none !important;
        text-shadow: 1px 1px #fffbe9, 2px 2px #E2B07A;
        letter-spacing: 1px;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    .pixel-btn:hover {
        background: url('https://i.imgur.com/6Q8QvQj.png') repeat, linear-gradient(90deg, #ffe7c2 60%, #ffe7c2 100%);
        filter: brightness(1.08);
        border-color: #ffb347;
    }
    .pixel-icon {
        width: 22px;
        height: 22px;
        vertical-align: middle;
        margin-right: 2px;
        image-rendering: pixelated;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
        <div style='text-align:center; font-size:2em; font-weight:bold; color:#B86L36; margin-bottom:8px; margin-top:2px;'>
            📝 New Entry  🍂✨
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='font-size:1em; color:#B86L36; text-align:center;'>Logged in as: <b>{st.session_state['user']}</b></div>",
        unsafe_allow_html=True
    )
    show_logout()

    # Add pixel art, coffee gif, and cozy pumpkin latte pixel art above the calendar
    st.markdown(
        """
        <div style='
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 6px;
        '>
            <img src="https://www.pixelartcss.com/images/leaf-pixel-art.gif" width="60" style="margin:2px 0 4px 0; border-radius:8px;" />
            <img src="https://media.giphy.com/media/3o6Zt6ML6BklcajjsA/giphy.gif" width="60" style="margin:2px 0 4px 0; border-radius:8px;" />
            <img src="https://i.imgur.com/7yT7vQy.png" width="60" style="margin:2px 0 4px 0; border-radius:8px;" title="Cozy Pumpkin Latte Pixel Art" />
        </div>
        <div style='
            font-size:1.1em;
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
        """,
        unsafe_allow_html=True
    )

    # Cute calendar with emoji hints (Streamlit doesn't support custom calendar widgets, so add emoji hints above)
    st.markdown(
        """
        <div style='text-align:center; font-size:1.2em; margin-bottom:2px;'>
            <span>🌞🌻🌾🍁🍂🍃🍄☕🎃🧣🧋🍪🍫🍵</span>
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
    entry_title = st.text_input("📝 Entry Title", placeholder="A cozy autumn day")
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
                color: #B86L36;
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

    user_key = f"entries_{st.session_state['user']}"
    if user_key not in st.session_state:
        st.session_state[user_key] = []
    # Add "New Entry" button to clear the editor
    if st.button("🆕 New Entry", key="new_entry_btn"):
        st.session_state["loaded_entry"] = None
        st.session_state["entry_title_loaded"] = ""
        st.session_state["entry_text_loaded"] = ""
        st.experimental_rerun()

    # Entry editor fields
    loaded_entry = st.session_state.get("loaded_entry")
    if loaded_entry:
        entry_title = st.text_input("📝 Entry Title", value=loaded_entry["title"], key="entry_title_loaded")
        entry_text = st.text_area("💬 Write your entry... 💖", value=loaded_entry["content"], height=160, key="entry_text_loaded")
    else:
        entry_title = st.text_input("📝 Entry Title", value="", key="entry_title_loaded")
        entry_text = st.text_area("💬 Write your entry... 💖", value="", height=160, key="entry_text_loaded")

    def save_entry_to_file(username, title, content, date):
        entries_dir = Path(__file__).parent.parent / "journal_entries" / username
        entries_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{date.strftime('%Y-%m-%d')}-entry.txt"
        filepath = entries_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Title: {title}\n")
            f.write("Content:\n")
            f.write(content.strip() + "\n")

    save_clicked = st.button(
        label='''<img class="pixel-icon" src="https://i.imgur.com/8Qf3XyB.png" /> Save Entry''',
        key="save_entry_btn",
        help="Save your cozy memory!",
        use_container_width=False,
    )
    # Patch the button to have the pixel-btn class (Streamlit workaround)
    st.markdown(
        """
        <script>
        const btns = window.parent.document.querySelectorAll('button');
        btns.forEach(btn => {
            if (btn.innerText.includes("Save Entry") && !btn.classList.contains('pixel-btn')) {
                btn.classList.add('pixel-btn');
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
            "title": entry_title,
            "text": entry_text,
            "emoji": st.session_state.get("custom_theme", {}).get("emoji", "🍂")
        }
        st.session_state[user_key].append(entry)
        # Save as a new file in user's folder
        save_entry_to_file(st.session_state["user"], entry_title, entry_text, date)
        st.session_state["loaded_entry"] = None
        st.session_state["entry_title_loaded"] = ""
        st.session_state["entry_text_loaded"] = ""
        st.success(f"Saved to your cozy journal! 🍯✨💖🧡\n\n📅 Saved entry for: {date.strftime('%B %d, %Y')} 💖🍁✨")
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- Calendar Events Storage ---
calendar_events_path = Path(__file__).parent / "calendar_events.json"
if calendar_events_path.exists():
    with open(calendar_events_path, "r", encoding="utf-8") as f:
        calendar_events = json.load(f)
else:
    calendar_events = {}

def save_calendar_events():
    with open(calendar_events_path, "w", encoding="utf-8") as f:
        json.dump(calendar_events, f, indent=2)

# --- Calendar UI with Events ---
st.markdown("## 📅 Calendar: Add Events to Specific Days")

today = datetime.date.today()
selected_month = st.selectbox(
    "Select month",
    options=[(today.year, m) for m in range(1, 13)],
    format_func=lambda ym: f"{datetime.date(ym[0], ym[1], 1):%B %Y}",
    index=today.month - 1
)
year, month = selected_month

# Generate calendar grid
import calendar as pycal
cal = pycal.Calendar()
month_days = list(cal.itermonthdates(year, month))
weeks = [month_days[i:i+7] for i in range(0, len(month_days), 7)]

# Render calendar
st.markdown("<style>.calendar-cell{padding:6px 0;text-align:center;min-width:38px;min-height:38px;display:inline-block;vertical-align:middle;border-radius:8px;cursor:pointer;}.calendar-today{background:#ffe7c2;}.calendar-event{background:#ffb347;color:#fff;}</style>", unsafe_allow_html=True)
selected_day = st.session_state.get("calendar_selected_day", None)

def calendar_cell(day, is_today, has_event):
    style = "calendar-cell"
    if is_today:
        style += " calendar-today"
    if has_event:
        style += " calendar-event"
    return f"<span class='{style}'>{day.day}{' 🍂' if has_event else ''}</span>"

st.markdown("<div style='display:inline-block;width:100%;overflow-x:auto;'>", unsafe_allow_html=True)
st.markdown(
    "<div style='font-weight:bold;display:flex;justify-content:space-between;max-width:340px;'>"
    + "".join(f"<span style='width:38px;text-align:center;'>{d}</span>" for d in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])
    + "</div>",
    unsafe_allow_html=True
)
for week in weeks:
    cols = st.columns(7)
    for i, day in enumerate(week):
        is_this_month = (day.month == month)
        is_today = (day == today)
        has_event = str(day) in calendar_events and calendar_events[str(day)]
        label = calendar_cell(day, is_today, has_event) if is_this_month else ""
        if is_this_month:
            if cols[i].button(label, key=f"cal_{day}"):
                st.session_state["calendar_selected_day"] = str(day)
        else:
            cols[i].markdown(" ")
st.markdown("</div>", unsafe_allow_html=True)

# --- Day Event Window ---
sel_day = st.session_state.get("calendar_selected_day", str(today))
if sel_day:
    st.markdown(f"### 📆 {sel_day}")
    events = calendar_events.get(sel_day, [])
    new_event = st.text_input("Add event for this day", key="calendar_event_input")
    if st.button("Add Event", key="calendar_add_event"):
        if new_event.strip():
            events.append(new_event.strip())
            calendar_events[sel_day] = events
            save_calendar_events()
            st.experimental_rerun()
    if events:
        st.markdown("#### Events:")
        for idx, ev in enumerate(events):
            col1, col2 = st.columns([0.85, 0.15])
            col1.markdown(f"- {ev}")
            if col2.button("❌", key=f"del_event_{sel_day}_{idx}"):
                events.pop(idx)
                if events:
                    calendar_events[sel_day] = events
                else:
                    calendar_events.pop(sel_day)
                save_calendar_events()
                st.experimental_rerun()
    else:
        st.info("No events for this day yet.")

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
        /* Always show vertical scrollbar in sidebar */
        section[data-testid="stSidebar"] > div:first-child {{
            scrollbar-width: auto;
            scrollbar-color: #E2B07A #F5E3D0;
        }}
        section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar {{
            width: 12px;
            background: #F5E3D0;
            border-radius: 8px;
            display: block;
        }}
        section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb {{
            background: #E2B07A;
            border-radius: 8px;
            min-height: 40px;
        }}
        section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb:hover {{
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
            border-left: 8px {border_style_css.get(custom_theme.get('border_style', 'Solid'), 'solid')} {custom_theme.get('primary_color', '#B86L36')};
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
            color: {custom_theme.get('primary_color', '#B86L36')} !important;
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
def load_journal_entries():
    entries_dir = Path(__file__).parent.parent / "journal_entries"
    if not entries_dir.exists():
        return []
    entries = []
    for file in sorted(entries_dir.glob("*.txt"), reverse=True):
        try:
            with open(file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                title = ""
                content = ""
                if lines and lines[0].startswith("Title:"):
                    title = lines[0].replace("Title:", "").strip()
                    content = "".join(lines[2:]).strip() if len(lines) > 2 else ""
                else:
                    title = file.stem
                    content = "".join(lines).strip()
                date_part = file.name.split("-entry.txt")[0]
                entries.append({
                    "filename": str(file),
                    "date": date_part,
                    "title": title,
                    "content": content
                })
        except Exception:
            continue
    return entries

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
        <div style='text-align:center; font-size:2em; font-weight:bold; color:#B86L36; margin-bottom:8px; margin-top:2px;'>
            📝 New Entry  🍂✨
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='font-size:1em; color:#B86L36; text-align:center;'>Logged in as: <b>{st.session_state['user']}</b></div>",
        unsafe_allow_html=True
    )
    show_logout()

    # Add pixel art, coffee gif, and cozy pumpkin latte pixel art above the calendar
    st.markdown(
        """
        <div style='
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 6px;
        '>
            <img src="https://www.pixelartcss.com/images/leaf-pixel-art.gif" width="60" style="margin:2px 0 4px 0; border-radius:8px;" />
            <img src="https://media.giphy.com/media/3o6Zt6ML6BklcajjsA/giphy.gif" width="60" style="margin:2px 0 4px 0; border-radius:8px;" />
            <img src="https://i.imgur.com/7yT7vQy.png" width="60" style="margin:2px 0 4px 0; border-radius:8px;" title="Cozy Pumpkin Latte Pixel Art" />
        </div>
        <div style='
            font-size:1.1em;
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
        """,
        unsafe_allow_html=True
    )

    # Cute calendar with emoji hints (Streamlit doesn't support custom calendar widgets, so add emoji hints above)
    st.markdown(
        """
        <div style='text-align:center; font-size:1.2em; margin-bottom:2px;'>
            <span>🌞🌻🌾🍁🍂🍃🍄☕🎃🧣🧋🍪🍫🍵</span>
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
    entry_title = st.text_input("📝 Entry Title", placeholder="A cozy autumn day")
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
                color: #B86L36;
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

    user_key = f"entries_{st.session_state['user']}"
    if user_key not in st.session_state:
        st.session_state[user_key] = []
    # Add "New Entry" button to clear the editor
    if st.button("🆕 New Entry", key="new_entry_btn"):
        st.session_state["loaded_entry"] = None
        st.session_state["entry_title_loaded"] = ""
        st.session_state["entry_text_loaded"] = ""
        st.experimental_rerun()

    # Entry editor fields
    loaded_entry = st.session_state.get("loaded_entry")
    if loaded_entry:
        entry_title = st.text_input("📝 Entry Title", value=loaded_entry["title"], key="entry_title_loaded")
        entry_text = st.text_area("💬 Write your entry... 💖", value=loaded_entry["content"], height=160, key="entry_text_loaded")
    else:
        entry_title = st.text_input("📝 Entry Title", value="", key="entry_title_loaded")
        entry_text = st.text_area("💬 Write your entry... 💖", value="", height=160, key="entry_text_loaded")

    def save_entry_to_file(username, title, content, date):
        entries_dir = Path(__file__).parent.parent / "journal_entries" / username
        entries_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{date.strftime('%Y-%m-%d')}-entry.txt"
        filepath = entries_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Title: {title}\n")
            f.write("Content:\n")
            f.write(content.strip() + "\n")

    save_clicked = st.button(
        label='''<img class="pixel-icon" src="https://i.imgur.com/8Qf3XyB.png" /> Save Entry''',
        key="save_entry_btn",
        help="Save your cozy memory!",
        use_container_width=False,
    )
    # Patch the button to have the pixel-btn class (Streamlit workaround)
    st.markdown(
        """
        <script>
        const btns = window.parent.document.querySelectorAll('button');
        btns.forEach(btn => {
            if (btn.innerText.includes("Save Entry") && !btn.classList.contains('pixel-btn')) {
                btn.classList.add('pixel-btn');
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
            "title": entry_title,
            "text": entry_text,
            "emoji": st.session_state.get("custom_theme", {}).get("emoji", "🍂")
        }
        st.session_state[user_key].append(entry)
        # Save as a new file in user's folder
        save_entry_to_file(st.session_state["user"], entry_title, entry_text, date)
        st.session_state["loaded_entry"] = None
        st.session_state["entry_title_loaded"] = ""
        st.session_state["entry_text_loaded"] = ""
        st.success(f"Saved to your cozy journal! 🍯✨💖🧡\n\n📅 Saved entry for: {date.strftime('%B %d, %Y')} 💖🍁✨")
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- Calendar Events Storage ---
calendar_events_path = Path(__file__).parent / "calendar_events.json"
if calendar_events_path.exists():
    with open(calendar_events_path, "r", encoding="utf-8") as f:
        calendar_events = json.load(f)
else:
    calendar_events = {}

def save_calendar_events():
    with open(calendar_events_path, "w", encoding="utf-8") as f:
        json.dump(calendar_events, f, indent=2)

# --- Calendar UI with Events ---
st.markdown("## 📅 Calendar: Add Events to Specific Days")

today = datetime.date.today()
selected_month = st.selectbox(
    "Select month",
    options=[(today.year, m) for m in range(1, 13)],
    format_func=lambda ym: f"{datetime.date(ym[0], ym[1], 1):%B %Y}",
    index=today.month - 1
)
year, month = selected_month

# Generate calendar grid
import calendar as pycal
cal = pycal.Calendar()
month_days = list(cal.itermonthdates(year, month))
weeks = [month_days[i:i+7] for i in range(0, len(month_days), 7)]

# Render calendar
st.markdown("<style>.calendar-cell{padding:6px 0;text-align:center;min-width:38px;min-height:38px;display:inline-block;vertical-align:middle;border-radius:8px;cursor:pointer;}.calendar-today{background:#ffe7c2;}.calendar-event{background:#ffb347;color:#fff;}</style>", unsafe_allow_html=True)
selected_day = st.session_state.get("calendar_selected_day", None)

def calendar_cell(day, is_today, has_event):
    style = "calendar-cell"
    if is_today:
        style += " calendar-today"
    if has_event:
        style += " calendar-event"
    return f"<span class='{style}'>{day.day}{' 🍂' if has_event else ''}</span>"

st.markdown("<div style='display:inline-block;width:100%;overflow-x:auto;'>", unsafe_allow_html=True)
st.markdown(
    "<div style='font-weight:bold;display:flex;justify-content:space-between;max-width:340px;'>"
    + "".join(f"<span style='width:38px;text-align:center;'>{d}</span>" for d in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])
    + "</div>",
    unsafe_allow_html=True
)
for week in weeks:
    cols = st.columns(7)
    for i, day in enumerate(week):
        is_this_month = (day.month == month)
        is_today = (day == today)
        has_event = str(day) in calendar_events and calendar_events[str(day)]
        label = calendar_cell(day, is_today, has_event) if is_this_month else ""
        if is_this_month:
            if cols[i].button(label, key=f"cal_{day}"):
                st.session_state["calendar_selected_day"] = str(day)
        else:
            cols[i].markdown(" ")
st.markdown("</div>", unsafe_allow_html=True)

# --- Day Event Window ---
sel_day = st.session_state.get("calendar_selected_day", str(today))
if sel_day:
    st.markdown(f"### 📆 {sel_day}")
    events = calendar_events.get(sel_day, [])
    new_event = st.text_input("Add event for this day", key="calendar_event_input")
    if st.button("Add Event", key="calendar_add_event"):
        if new_event.strip():
            events.append(new_event.strip())
            calendar_events[sel_day] = events
            save_calendar_events()
            st.experimental_rerun()
    if events:
        st.markdown("#### Events:")
        for idx, ev in enumerate(events):
            col1, col2 = st.columns([0.85, 0.15])
            col1.markdown(f"- {ev}")
            if col2.button("❌", key=f"del_event_{sel_day}_{idx}"):
                events.pop(idx)
                if events:
                    calendar_events[sel_day] = events
                else:
                    calendar_events.pop(sel_day)
                save_calendar_events()
                st.experimental_rerun()
    else:
        st.info("No events for this day yet.")

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
        /* Always show vertical scrollbar in sidebar */
        section[data-testid="stSidebar"] > div:first-child {{
            scrollbar-width: auto;
            scrollbar-color: #E2B07A #F5E3D0;
        }}
        section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar {{
            width: 12px;
            background: #F5E3D0;
            border-radius: 8px;
            display: block;
        }}
        section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb {{
            background: #E2B07A;
            border-radius: 8px;
            min-height: 40px;
        }}
        section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb:hover {{
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
            border-left: 8px {border_style_css.get(custom_theme.get('border_style', 'Solid'), 'solid')} {custom_theme.get('primary_color', '#B86L36')};
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
            color: {custom_theme.get('primary_color', '#B86L36')} !important;
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
def load_journal_entries():
    entries_dir = Path(__file__).parent.parent / "journal_entries"
    if not entries_dir.exists():
        return []
    entries = []
    for file in sorted(entries_dir.glob("*.txt"), reverse=True):
        try:
            with open(file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                title = ""
                content = ""
                if lines and lines[0].startswith("Title:"):
                    title = lines[0].replace("Title:", "").strip()
                    content = "".join(lines[2:]).strip() if len(lines) > 2 else ""
                else:
                    title = file.stem
                    content = "".join(lines).strip()
                date_part = file.name.split("-entry.txt")[0]
                entries.append({
                    "filename": str(file),
                    "date": date_part,
                    "title": title,
                    "content": content
                })
        except Exception:
            continue
    return entries

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
        <div style='text-align:center; font-size:2em; font-weight:bold; color:#B86L36; margin-bottom:8px; margin-top:2px;'>
            📝 New Entry  🍂✨
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='font-size:1em; color:#B86L36; text-align:center;'>Logged in as: <b>{st.session_state['user']}</b></div>",
        unsafe_allow_html=True
    )
    show_logout()

    # Add pixel art, coffee gif, and cozy pumpkin latte pixel art above the calendar
    st.markdown(
        """
        <div style='
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 6px;
        '>
            <img src="https://www.pixelartcss.com/images/leaf-pixel-art.gif" width="60" style="margin:2px 0 4px 0; border-radius:8px;" />
            <img src="https://media.giphy.com/media/3o6Zt6ML6BklcajjsA/giphy.gif" width="60" style="margin:2px 0 4px 0; border-radius:8px;" />
            <img src="https://i.imgur.com/7yT7vQy.png" width="60" style="margin:2px 0 4px 0; border-radius:8px;" title="Cozy Pumpkin Latte Pixel Art" />
        </div>
        <div style='
            font-size:1.1em;
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
        """,
        unsafe_allow_html=True
    )

    # Cute calendar with emoji hints (Streamlit doesn't support custom calendar widgets, so add emoji hints above)
    st.markdown(
        """
        <div style='text-align:center; font-size:1.2em; margin-bottom:2px;'>
            <span>🌞🌻🌾🍁🍂🍃🍄☕🎃🧣🧋🍪🍫🍵</span>
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
    entry_title = st.text_input("📝 Entry Title", placeholder="A cozy autumn day")
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
                color: #B86L36;
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

    user_key = f"entries_{st.session_state['user']}"
    if user_key not in st.session_state:
        st.session_state[user_key] = []
    # Add "New Entry" button to clear the editor
    if st.button("🆕 New Entry", key="new_entry_btn"):
        st.session_state["loaded_entry"] = None
        st.session_state["entry_title_loaded"] = ""
        st.session_state["entry_text_loaded"] = ""
        st.experimental_rerun()

    # Entry editor fields
    loaded_entry = st.session_state.get("loaded_entry")
    if loaded_entry:
        entry_title = st.text_input("📝 Entry Title", value=loaded_entry["title"], key="entry_title_loaded")
        entry_text = st.text_area("💬 Write your entry... 💖", value=loaded_entry["content"], height=160, key="entry_text_loaded")
    else:
        entry_title = st.text_input("📝 Entry Title", value="", key="entry_title_loaded")
        entry_text = st.text_area("💬 Write your entry... 💖", value="", height=160, key="entry_text_loaded")

    def save_entry_to_file(username, title, content, date):
        entries_dir = Path(__file__).parent.parent / "journal_entries" / username
        entries_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{date.strftime('%Y-%m-%d')}-entry.txt"
        filepath = entries_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Title: {title}\n")
            f.write("Content:\n")
            f.write(content.strip() + "\n")

    save_clicked = st.button(
        label='''<img class="pixel-icon" src="https://i.imgur.com/8Qf3XyB.png" /> Save Entry''',
        key="save_entry_btn",
        help="Save your cozy memory!",
        use_container_width=False,
    )
    # Patch the button to have the pixel-btn class (Streamlit workaround)
    st.markdown(
        """
        <script>
        const btns = window.parent.document.querySelectorAll('button');
        btns.forEach(btn => {
            if (btn.innerText.includes("Save Entry") && !btn.classList.contains('pixel-btn')) {
                btn.classList.add('pixel-btn');
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
            "title": entry_title,
            "text": entry_text,
            "emoji": st.session_state.get("custom_theme", {}).get("emoji", "🍂")
        }
        st.session_state[user_key].append(entry)
        # Save as a new file in user's folder
        save_entry_to_file(st.session_state["user"], entry_title, entry_text, date)
        st.session_state["loaded_entry"] = None
        st.session_state["entry_title_loaded"] = ""
        st.session_state["entry_text_loaded"] = ""
        st.success(f"Saved to your cozy journal! 🍯✨💖🧡\n\n📅 Saved entry for: {date.strftime('%B %d, %Y')} 💖🍁✨")
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- Calendar Events Storage ---
calendar_events_path = Path(__file__).parent / "calendar_events.json"
if calendar_events_path.exists():
    with open(calendar_events_path, "r", encoding="utf-8") as f:
        calendar_events = json.load(f)
else:
    calendar_events = {}

def save_calendar_events():
    with open(calendar_events_path, "w", encoding="utf-8") as f:
        json.dump(calendar_events, f, indent=2)

# --- Calendar UI with Events ---
st.markdown("## 📅 Calendar: Add Events to Specific Days")

today = datetime.date.today()
selected_month = st.selectbox(
    "Select month",
    options=[(today.year, m) for m in range(1, 13)],
    format_func=lambda ym: f"{datetime.date(ym[0], ym[1], 1):%B %Y}",
    index=today.month - 1
)
year, month = selected_month

# Generate calendar grid
import calendar as pycal
cal = pycal.Calendar()
month_days = list(cal.itermonthdates(year, month))
weeks = [month_days[i:i+7] for i in range(0, len(month_days), 7)]

# Render calendar
st.markdown("<style>.calendar-cell{padding:6px 0;text-align:center;min-width:38px;min-height:38px;display:inline-block;vertical-align:middle;border-radius:8px;cursor:pointer;}.calendar-today{background:#ffe7c2;}.calendar-event{background:#ffb347;color:#fff;}</style>", unsafe_allow_html=True)
selected_day = st.session_state.get("calendar_selected_day", None)

def calendar_cell(day, is_today, has_event):
    style = "calendar-cell"
    if is_today:
        style += " calendar-today"
    if has_event:
        style += " calendar-event"
    return f"<span class='{style}'>{day.day}{' 🍂' if has_event else ''}</span>"

st.markdown("<div style='display:inline-block;width:100%;overflow-x:auto;'>", unsafe_allow_html=True)
st.markdown(
    "<div style='font-weight:bold;display:flex;justify-content:space-between;max-width:340px;'>"
    + "".join(f"<span style='width:38px;text-align:center;'>{d}</span>" for d in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])
    + "</div>",
    unsafe_allow_html=True
)
for week in weeks:
    cols = st.columns(7)
    for i, day in enumerate(week):
        is_this_month = (day.month == month)
        is_today = (day == today)
        has_event = str(day) in calendar_events and calendar_events[str(day)]
        label = calendar_cell(day, is_today, has_event) if is_this_month else ""
        if is_this_month:
            if cols[i].button(label, key=f"cal_{day}"):
                st.session_state["calendar_selected_day"] = str(day)
        else:
            cols[i].markdown(" ")
st.markdown("</div>", unsafe_allow_html=True)

# --- Day Event Window ---
sel_day = st.session_state.get("calendar_selected_day", str(today))
if sel_day:
    st.markdown(f"### 📆 {sel_day}")
    events = calendar_events.get(sel_day, [])
    new_event = st.text_input("Add event for this day", key="calendar_event_input")
    if st.button("Add Event", key="calendar_add_event"):
        if new_event.strip():
            events.append(new_event.strip())
            calendar_events[sel_day] = events
            save_calendar_events()
            st.experimental_rerun()
    if events:
        st.markdown("#### Events:")
        for idx, ev in enumerate(events):
            col1, col2 = st.columns([0.85, 0.15])
            col1.markdown(f"- {ev}")
            if col2.button("❌", key=f"del_event_{sel_day}_{idx}"):
                events.pop(idx)
                if events:
                    calendar_events[sel_day] = events
                else:
                    calendar_events.pop(sel_day)
                save_calendar_events()
                st.experimental_rerun()
    else:
        st.info("No events for this day yet.")

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
        /* Always show vertical scrollbar in sidebar */
        section[data-testid="stSidebar"] > div:first-child {{
            scrollbar-width: auto;
            scrollbar-color: #E2B07A #F5E3D0;
        }}
        section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar {{
            width: 12px;
            background: #F5E3D0;
            border-radius: 8px;
            display: block;
        }}
        section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb {{
            background: #E2B07A;
            border-radius: 8px;
            min-height: 40px;
        }}
        section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb:hover {{
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
            border-left: 8px {border_style_css.get(custom_theme.get('border_style', 'Solid'), 'solid')} {custom_theme.get('primary_color', '#B86L36')};
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
            color: {custom_theme.get('primary_color', '#B86L36')} !important;
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