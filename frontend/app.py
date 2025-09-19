import streamlit as st
import datetime
import json
from pathlib import Path
import hashlib
import os

def calming_transition():
    st.markdown(
        """
        <style>
        .fade-bg {
            position: fixed;
            top:0; left:0; width:100vw; height:100vh;
            background: linear-gradient(120deg, #fffbe9 0%, #ffe7c2 100%);
            z-index: 9999;
            animation: fadeout-bg 1.2s ease-in forwards;
        }
        @keyframes fadeout-bg {
            0% { opacity: 1; }
            80% { opacity: 1; }
            100% { opacity: 0; pointer-events: none; }
        }
        .fade-leaf {
            position: fixed;
            left: 50%; top: 50%;
            transform: translate(-50%,-50%);
            font-size: 3.5em;
            opacity: 0.8;
            animation: fade-leaf 1.2s ease-in forwards;
            z-index: 10000;
        }
        @keyframes fade-leaf {
            0% { opacity: 0.8; transform: translate(-50%,-50%) scale(1);}
            80% { opacity: 1; transform: translate(-50%,-50%) scale(1.2);}
            100% { opacity: 0; transform: translate(-50%,-50%) scale(2);}
        }
        </style>
        <div class="fade-bg"></div>
        <div class="fade-leaf">🍂☕🍁</div>
        """,
        unsafe_allow_html=True
    )
    import time
    time.sleep(1.2)

# --- Pastel Fall-Themed Login UI with Lo-fi Music ---
def login_ui():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
        body, .stApp {
            background: 
                repeating-linear-gradient(0deg, #fffbe9 0, #fffbe9 4px, transparent 4px, transparent 40px),
                repeating-linear-gradient(90deg, #fffbe9 0, #fffbe9 4px, transparent 4px, transparent 40px),
                repeating-linear-gradient(0deg, #FFE5B4 0, #FFE5B4 2px, transparent 2px, transparent 20px),
                repeating-linear-gradient(90deg, #FFE5B4 0, #FFE5B4 2px, transparent 2px, transparent 20px),
                linear-gradient(120deg, #fffbe9 0%, #ffe7c2 100%);
            background-size: 40px 40px, 40px 40px, 20px 20px, 20px 20px, 100% 100%;
            background-position: 0 0, 0 0, 0 0, 0 0, 0 0;
        }
        .pastel-login-bg {
            min-height: 100vh;
            width: 100vw;
            position: fixed;
            top: 0; left: 0;
            z-index: 0;
            background: transparent;
            overflow: hidden;
        }
        .pastel-login-card {
            background: rgba(255, 250, 235, 0.98);
            border-radius: 28px;
            box-shadow: 0 8px 32px rgba(186,107,54,0.13), 0 0 0 8px #ffe7c2 inset;
            padding: 2.5em 2em 2em 2em;
            max-width: 410px;
            margin: 32px auto 0 auto;
            border: 2.5px solid #f7e3c2;
            position: relative;
        }
        .pastel-login-card .emoji-header {
            font-size: 2.2em;
            text-align: center;
            margin-bottom: 0.2em;
            margin-top: -0.5em;
        }
        .pastel-login-card .fall-img-inner {
            background: #fffbe9;
            border-radius: 22px;
            box-shadow: 0 4px 24px #ffe7c2, 0 0 0 6px #ffe7c2 inset;
            border: 3px solid #e2b07a;
            padding: 0.5em;
            max-width: 340px;
            margin: 0.5em auto 0.5em auto;
        }
        .pastel-login-card .fall-img-inner img {
            width: 100%;
            height: 120px;
            object-fit: cover;
            border-radius: 18px;
            box-shadow: 0 2px 12px #e2b07a44;
            border: 2px solid #ffe7c2;
        }
        .pastel-login-card .elegant-heading {
            font-family: 'Playfair Display', 'Georgia', serif;
            color: #b97a56;
            font-size: 2.1em;
            text-align: center;
            margin-bottom: 0.2em;
            margin-top: 0.2em;
            letter-spacing: 1px;
            font-weight: 700;
        }
        /* Pixel input fields */
        .pixel-input {
            font-family: 'Press Start 2P', 'Comic Sans MS', cursive, sans-serif !important;
            background: #fffbe9;
            border: 3px solid #e2b07a !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 0 #ffe7c2, 0 0 0 4px #ffe7c2 inset;
            font-size: 1em !important;
            color: #b97a56 !important;
            padding: 0.7em 1.2em !important;
            margin-bottom: 1.1em !important;
            outline: none !important;
            transition: border 0.2s, box-shadow 0.2s;
            letter-spacing: 1px;
            animation: pixel-pop 0.6s;
        }
        .pixel-input:focus {
            border: 3px solid #ffb347 !important;
            background: #fff7e0 !important;
            box-shadow: 0 4px 16px #ffe7c2;
        }
        @keyframes pixel-pop {
            0% { box-shadow: 0 0 0 #ffe7c2; }
            60% { box-shadow: 0 0 8px #ffe7c2; }
            100% { box-shadow: 0 2px 0 #ffe7c2, 0 0 0 4px #ffe7c2 inset; }
        }
        /* Pixel button */
        .pixel-btn {
            background: url('https://i.imgur.com/6Q8QvQj.png') repeat, linear-gradient(90deg, #ffd9a0 60%, #ffe7c2 100%);
            background-size: 40px 40px, 100% 100%;
            border: 3px solid #a05a2c;
            border-radius: 12px;
            color: #B86B36;
            font-size: 1.08em;
            font-family: 'Press Start 2P', 'Comic Sans MS', cursive, sans-serif;
            font-weight: bold;
            padding: 0.7em 1.2em;
            margin-top: 2px;
            margin-bottom: 2px;
            box-shadow: 0 2px 8px rgba(186,107,54,0.18), 0 0 0 4px #ffe7c2 inset;
            cursor: pointer;
            transition: 0.2s;
            outline: none !important;
            text-shadow: 1px 1px #fffbe9, 2px 2px #E2B07A;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            gap: 8px;
            animation: pixel-pop 0.6s;
        }
        .pixel-btn:hover {
            background: url('https://i.imgur.com/6Q8QvQj.png') repeat, linear-gradient(90deg, #ffe7c2 60%, #ffd9a0 100%);
            filter: brightness(1.08);
            border-color: #ffb347;
            box-shadow: 0 4px 16px #ffe7c2;
        }
        .pop-anim {
            animation: pop-anim 0.25s cubic-bezier(.68,-0.55,.27,1.55);
        }
        @keyframes pop-anim {
            0% { transform: scale(1);}
            50% { transform: scale(1.13);}
            100% { transform: scale(1);}
        }
        </style>
        <div class="pastel-login-bg"></div>
        <div class="fall-leaf-pastel fall-leaf-pastel1">🍂</div>
        <div class="fall-leaf-pastel fall-leaf-pastel2">🍁</div>
        <div class="fall-leaf-pastel fall-leaf-pastel3">🌰</div>
        <div class="fall-leaf-pastel fall-leaf-pastel4">🍃</div>
        <div class="fall-leaf-pastel fall-leaf-pastel5">🍂</div>
        <script>
        // Add pop animation to all buttons on click
        window.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('button').forEach(btn => {
                btn.addEventListener('click', function() {
                    btn.classList.remove('pop-anim');
                    void btn.offsetWidth; // trigger reflow
                    btn.classList.add('pop-anim');
                });
            });
        });
        </script>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <audio id="lofi-music" src="https://cdn.pixabay.com/audio/2022/10/16/audio_12b6b6e2e6.mp3" autoplay loop>
        </audio>
        <script>
        window.addEventListener('DOMContentLoaded', function() {
            var audio = document.getElementById('lofi-music');
            if (audio) { audio.volume = 0.25; }
        });
        </script>
        """,
        unsafe_allow_html=True
    )
    assets_dir = Path(__file__).parent / "assets"
    header_img_path = assets_dir / "fall.jpg"
    img_html = ""
    if header_img_path.exists():
        import base64
        img_bytes = header_img_path.read_bytes()
        img_b64 = base64.b64encode(img_bytes).decode()
        img_html = f"""
            <div class="fall-img-inner">
                <img src="data:image/jpg;base64,{img_b64}" alt="Cozy Fall" />
            </div>
        """
    tab_login, tab_register = st.tabs(["☕ Login", "🍁 Register"])
    with tab_login:
        st.markdown(
            f"""
            <div class="pastel-login-card">
                <div class="emoji-header">🍁🍂☕🌰</div>
                {img_html}
                <div class="elegant-heading">Cozy Fall Journal</div>
                <div class="emoji-header">🍁🍂☕🌰</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        username = st.text_input("👤 Username", key="login_username", placeholder="👤 username", label_visibility="collapsed")
        password = st.text_input("🔑 Password", type="password", key="login_password", placeholder="🔑 password", label_visibility="collapsed")
        st.markdown(
            """
            <style>
            /* Patch Streamlit input fields to pixel style */
            [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
                font-family: 'Press Start 2P', 'Comic Sans MS', cursive, sans-serif !important;
                background: #fffbe9;
                border: 3px solid #e2b07a !important;
                border-radius: 10px !important;
                box-shadow: 0 2px 0 #ffe7c2, 0 0 0 4px #ffe7c2 inset;
                font-size: 1em !important;
                color: #b97a56 !important;
                padding: 0.7em 1.2em !important;
                margin-bottom: 1.1em !important;
                outline: none !important;
                transition: border 0.2s, box-shadow 0.2s;
                letter-spacing: 1px;
                animation: pixel-pop 0.6s;
            }
            [data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus {
                border: 3px solid #ffb347 !important;
                background: #fff7e0 !important;
                box-shadow: 0 4px 16px #ffe7c2;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        login_btn = st.button("☕  Login", key="login_btn", help="Login to your cozy journal!", use_container_width=True)
        # Patch the button to have pixel-btn class
        st.markdown(
            """
            <script>
            window.addEventListener('DOMContentLoaded', function() {
                document.querySelectorAll('button').forEach(btn => {
                    if (btn.innerText.includes("Login") && !btn.classList.contains('pixel-btn')) {
                        btn.classList.add('pixel-btn');
                    }
                });
            });
            </script>
            """,
            unsafe_allow_html=True
        )
        if login_btn:
            if login_user(username, password):
                st.session_state["user"] = username
                calming_transition()
                st.success("Login successful! 🍁")
                st.rerun()
            else:
                st.error("Invalid username or password.")
    with tab_register:
        st.markdown(
            f"""
            <div class="pastel-login-card">
                <div class="emoji-header">🍁🍂🌰☕</div>
                {img_html}
                <div class="elegant-heading">Cozy Fall Journal</div>
                <div class="emoji-header">🍁🍂☕🌰</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        new_username = st.text_input("👤 New Username", key="register_username", placeholder="👤 new username", label_visibility="collapsed")
        new_password = st.text_input("🔑 New Password", type="password", key="register_password", placeholder="🔑 new password", label_visibility="collapsed")
        st.markdown(
            """
            <style>
            [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
                font-family: 'Press Start 2P', 'Comic Sans MS', cursive, sans-serif !important;
                background: #fffbe9;
                border: 3px solid #e2b07a !important;
                border-radius: 10px !important;
                box-shadow: 0 2px 0 #ffe7c2, 0 0 0 4px #ffe7c2 inset;
                font-size: 1em !important;
                color: #b97a56 !important;
                padding: 0.7em 1.2em !important;
                margin-bottom: 1.1em !important;
                outline: none !important;
                transition: border 0.2s, box-shadow 0.2s;
                letter-spacing: 1px;
                animation: pixel-pop 0.6s;
            }
            [data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus {
                border: 3px solid #ffb347 !important;
                background: #fff7e0 !important;
                box-shadow: 0 4px 16px #ffe7c2;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        register_btn = st.button("☕  Register", key="register_btn", help="Create your cozy account!", use_container_width=True)
        st.markdown(
            """
            <script>
            window.addEventListener('DOMContentLoaded', function() {
                document.querySelectorAll('button').forEach(btn => {
                    if (btn.innerText.includes("Register") && !btn.classList.contains('pixel-btn')) {
                        btn.classList.add('pixel-btn');
                    }
                });
            });
            </script>
            """,
            unsafe_allow_html=True
        )
        if register_btn:
            ok, msg = register_user(new_username, new_password)
            if ok:
                st.success(msg)
                st.session_state["user"] = new_username
                calming_transition()
                st.rerun()
            else:
                st.error(msg)

# --- User Auth ---
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

def require_login():
    if "user" not in st.session_state:
        login_ui()
        st.stop()
    user_folder = Path(__file__).parent.parent / "journal_entries" / st.session_state["user"]
    user_folder.mkdir(parents=True, exist_ok=True)

def show_logout():
    if "user" in st.session_state:
        if st.button("🚪 Logout", key="logout_btn"):
            logout_user()
            st.rerun()

# --- Require Login ---
require_login()
user_key = f"entries_{st.session_state['user']}"
if user_key not in st.session_state:
    st.session_state[user_key] = []

# --- Journal Entry Save/Load ---
def save_entry_to_file(username, title, content, date):
    entries_dir = Path(__file__).parent.parent / "journal_entries" / username
    entries_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{date.strftime('%Y-%m-%d-%H%M%S')}-entry.txt"
    filepath = entries_dir / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Title: {title}\n")
        f.write("Content:\n")
        f.write(content.strip() + "\n")

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
                    if len(lines) > 2:
                        content = "".join(lines[2:]).strip()
                    else:
                        content = ""
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
        except Exception as e:
            st.warning(f"Could not read entry file {file.name}: {e}")
    return entries

# --- Streamlit App ---
st.title("Cozy Fall Journal 🍂")
st.write("Reflect, Relax, and Rejuvenate in your personal online journal.")

# --- Pixel Art UI Theme ---
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
        scrollbar-color: #B86K4B #e7c49a;
    }
    .pop-anim {
        animation: pop-anim 0.25s cubic-bezier(.68,-0.55,.27,1.55);
    }
    @keyframes pop-anim {
        0% { transform: scale(1);}
        50% { transform: scale(1.13);}
        100% { transform: scale(1);}
    }
    </style>
    <script>
    // Add pop animation to all buttons on click (main app)
    window.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('button').forEach(btn => {
            btn.addEventListener('click', function() {
                btn.classList.remove('pop-anim');
                void btn.offsetWidth;
                btn.classList.add('pop-anim');
            });
        });
    });
    </script>
    """,
    unsafe_allow_html=True
)