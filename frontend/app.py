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

# --- Pastel Fall-Themed Login UI with Pixel Tree, Falling Leaves, and Lofi Music ---
def login_ui():
    # --- Load pixel tree image as base64 ---
    assets_dir = Path(__file__).parent / "assets"
    tree_img_path = assets_dir / "pixel_fall_tree.png"
    if tree_img_path.exists():
        import base64
        tree_img_bytes = tree_img_path.read_bytes()
        tree_img_b64 = base64.b64encode(tree_img_bytes).decode()
        tree_img_html = f'<img src="data:image/png;base64,{tree_img_b64}" class="pixel-tree-img" alt="Pixel Fall Tree" />'
    else:
        tree_img_html = '<div class="pixel-tree-img" style="width:320px;height:400px;background:#e2b07a;border-radius:18px;box-shadow:0 4px 32px #e2b07a55;display:flex;align-items:center;justify-content:center;font-size:2.5em;">🌳</div>'

    # --- Load fall.jpg as base64 ---
    fall_img_path = assets_dir / "fall.jpg"
    if fall_img_path.exists():
        import base64
        fall_img_bytes = fall_img_path.read_bytes()
        fall_img_b64 = base64.b64encode(fall_img_bytes).decode()
        fall_img_html = f'<img src="data:image/jpg;base64,{fall_img_b64}" class="fall-header-img" alt="Cozy Fall" />'
    else:
        fall_img_html = ""

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
        [data-testid="stAppViewContainer"], .stApp {{
            background: 
                repeating-linear-gradient(0deg, #fffbe9 0, #fffbe9 4px, transparent 4px, transparent 40px),
                repeating-linear-gradient(90deg, #fffbe9 0, #fffbe9 4px, transparent 4px, transparent 40px),
                repeating-linear-gradient(0deg, #FFE5B4 0, #FFE5B4 2px, transparent 2px, transparent 20px),
                repeating-linear-gradient(90deg, #FFE5B4 0, #FFE5B4 2px, transparent 2px, transparent 20px),
                linear-gradient(120deg, #fffbe9 0%, #ffe7c2 100%);
            background-size: 40px 40px, 40px 40px, 20px 20px, 20px 20px, 100% 100%;
            background-position: 0 0, 0 0, 0 0, 0 0, 0 0;
        }}
        .login-flex {{
            display: flex;
            flex-direction: row;
            align-items: flex-start;
            justify-content: center;
            min-height: 90vh;
            width: 100vw;
            position: relative;
            z-index: 2;
        }}
        .login-left {{
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            margin-top: 48px;
            z-index: 3;
            position: relative;
        }}
        .login-title {{
            font-family: 'Playfair Display', 'Georgia', serif;
            color: #b97a56;
            font-size: 2.3em;
            text-align: center;
            margin-bottom: 0.5em;
            margin-top: 0.2em;
            letter-spacing: 1px;
            font-weight: 700;
            text-shadow: 0 2px 8px #ffe7c2;
        }}
        .fall-header-img {{
            width: 420px;
            height: 140px;
            object-fit: cover;
            border-radius: 20px;
            box-shadow: 0 4px 24px #ffe7c2, 0 0 0 6px #ffe7c2 inset;
            border: 3px solid #e2b07a;
            margin-bottom: 1.5em;
        }}
        .login-form-box {{
            width: 100%;
            max-width: 370px;
            margin-top: 1.5em;
        }}
        .pixel-tree-img {{
            width: 340px;
            height: 420px;
            opacity: 0.62;
            filter: drop-shadow(0 8px 32px #e2b07a88);
            image-rendering: pixelated;
            margin-left: 2vw;
            margin-bottom: 0;
            background: transparent;
            position: relative;
            z-index: 2;
        }}
        .pixel-tree-side {{
            flex: 1;
            display: flex;
            align-items: flex-end;
            justify-content: flex-end;
            min-height: 90vh;
        }}
        /* Falling leaf sprites overlaying tree edge */
        .fall-leaf-particle {{
            position: fixed;
            z-index: 3;
            pointer-events: none;
            opacity: 0.85;
            animation: fall-leaf-particle 8s linear infinite;
        }}
        @keyframes fall-leaf-particle {{
            0% {{ transform: translateY(-60px) rotate(-10deg); opacity: 0.8; }}
            70% {{ opacity: 1; }}
            100% {{ transform: translateY(100vh) rotate(30deg); opacity: 0.2; }}
        }}
        .fall-leaf-particle1 {{ right: 10vw; font-size: 2.6em; animation-delay: 0s; }}
        .fall-leaf-particle2 {{ right: 16vw; font-size: 2.2em; animation-delay: 2s; }}
        .fall-leaf-particle3 {{ right: 22vw; font-size: 2.8em; animation-delay: 3.5s; }}
        .fall-leaf-particle4 {{ right: 28vw; font-size: 2em; animation-delay: 1.2s; }}
        .fall-leaf-particle5 {{ right: 13vw; font-size: 2.3em; animation-delay: 4.2s; }}
        .fall-leaf-particle6 {{ right: 25vw; font-size: 2.1em; animation-delay: 5.1s; }}
        .pop-anim {{
            animation: pop-anim 0.25s cubic-bezier(.68,-0.55,.27,1.55);
        }}
        @keyframes pop-anim {
            0% { transform: scale(1);}
            50% { transform: scale(1.13);}
            100% { transform: scale(1);}
        }
        </style>
        <div class="login-flex">
            <div class="login-left">
                <div class="login-title">Cozy Fall Journal</div>
                {fall_img_html}
                <div class="login-form-box">
        """,
        unsafe_allow_html=True
    )

    # Login and Register Tabs
    tab_login, tab_register = st.tabs(["☕ Login", "🍁 Register"])
    with tab_login:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        login_btn = st.button("☕  Login", key="login_btn", help="Login to your cozy journal!", use_container_width=True)
        if login_btn:
            if login_user(username, password):
                st.session_state["user"] = username
                calming_transition()
                st.success("Login successful! 🍁")
                st.rerun()
            else:
                st.error("Invalid username or password.")
    with tab_register:
        new_username = st.text_input("New Username", key="register_username")
        new_password = st.text_input("New Password", type="password", key="register_password")
        register_btn = st.button("☕  Register", key="register_btn", help="Create your cozy account!", use_container_width=True)
        if register_btn:
            ok, msg = register_user(new_username, new_password)
            if ok:
                st.success(msg)
                st.session_state["user"] = new_username
                calming_transition()
                st.rerun()
            else:
                st.error(msg)

    st.markdown(
        """
                </div>
            </div>
            <div class="pixel-tree-side">
                {tree_img_html}
            </div>
        </div>
        <div class="fall-leaf-particle fall-leaf-particle1">🍂</div>
        <div class="fall-leaf-particle fall-leaf-particle2">🍁</div>
        <div class="fall-leaf-particle fall-leaf-particle3">🍃</div>
        <div class="fall-leaf-particle fall-leaf-particle4">🍁</div>
        <div class="fall-leaf-particle fall-leaf-particle5">🍂</div>
        <div class="fall-leaf-particle fall-leaf-particle6">🍃</div>
        <script>
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
        """.format(tree_img_html=tree_img_html),
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
    # Render Streamlit login form inside the left column
    col1, col2 = st.columns([1, 1])
    with col1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        login_btn = st.button("☕  Login", key="login_btn", help="Login to your cozy journal!", use_container_width=True)
        if login_btn:
            if login_user(username, password):
                st.session_state["user"] = username
                calming_transition()
                st.success("Login successful! 🍁")
                st.rerun()
            else:
                st.error("Invalid username or password.")
        new_username = st.text_input("New Username", key="register_username")
        new_password = st.text_input("New Password", type="password", key="register_password")
        register_btn = st.button("☕  Register", key="register_btn", help="Create your cozy account!", use_container_width=True)
        if register_btn:
            ok, msg = register_user(new_username, new_password)
            if ok:
                st.success(msg)
                st.session_state["user"] = new_username
                calming_transition()
                st.rerun()
            else:
                st.error(msg)
    # col2 is intentionally left empty for the tree image (handled by CSS/HTML above)

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