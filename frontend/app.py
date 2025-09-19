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
                calming_transition()
                st.success("Login successful! 🍁")
                st.rerun()
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

# --- Journal Entry Form ---
with st.form("journal_entry_form", clear_on_submit=True):
    st.subheader("New Journal Entry")
    entry_title = st.text_input("Entry Title", placeholder="What’s on your mind?", max_chars=100)
    entry_content = st.text_area("Entry Content", placeholder="Dear Journal...", height=150)
    submit_entry = st.form_submit_button("📖  Save Entry", use_container_width=True)

if submit_entry and entry_title and entry_content:
    # Save entry to file
    date_now = datetime.datetime.now()
    save_entry_to_file(st.session_state["user"], entry_title, entry_content, date_now)
    st.success("Entry saved!")
    # Update session state
    st.session_state[user_key].append({
        "title": entry_title,
        "content": entry_content,
        "date": date_now.strftime("%Y-%m-%d %H:%M:%S")
    })
    st.experimental_rerun()

# --- Journal Entries ---
st.subheader("Your Journal Entries")
entries = load_journal_entries(st.session_state["user"])
if not entries:
    st.write("No entries found. Start by writing your first entry!")
else:
    for entry in entries:
        entry_date = datetime.datetime.strptime(entry["date"], "%Y-%m-%d %H%M%S")
        st.write(f"### {entry['title']}")
        st.write(f"*{entry_date.strftime('%Y-%m-%d %H:%M')}*")
        st.write(entry["content"])
        st.write("")
        # Download link
        file_path = entry["filename"]
        file_name = Path(file_path).name
        with open(file_path, "rb") as f:
            st.download_button(
                label="📥 Download Entry",
                data=f,
                file_name=file_name,
                mime="text/plain",
                key=f"download_{file_name}"
            )
        st.markdown("---")

# --- Footer ---
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(255, 250, 235, 0.9);
        color: #b97a56;
        text-align: center;
        padding: 0.5em 0;
        border-top: 2px solid #f7e3c2;
    }
    </style>
    <div class="footer">
        <p>🍂 Cozy Fall Journal - Your personal space to reflect and relax.</p>
    </div>
    """,
    unsafe_allow_html=True
)