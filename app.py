import streamlit as st  # For web app
from cryptography.fernet import Fernet  # For encryption
import hashlib  # For hashing
import time  # For timing tasks

# ---------------------- Session State Initialization ----------------------

# Store encrypted data
if "data_store" not in st.session_state:
    st.session_state.data_store = {}

# Track current page user is on
if "page" not in st.session_state:
    st.session_state.page = "home"

# Track failed login attempts per data ID
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = {}

# Track whether the user is authenticated
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Used to auto-redirect after login
if "just_logged_in" not in st.session_state:
    st.session_state.just_logged_in = False

# ---------------------- Utility Functions ----------------------

# Hash the passkey using SHA-256 for secure storage
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Generate a key from the passkey (not directly used in this app)
def generate_key(passkey):
    return hashlib.sha256(passkey.encode()).digest()[:32]

# Encrypt the input text using Fernet symmetric encryption
def encrypt_data(text, passkey):
    key = Fernet.generate_key()  # Random secure key
    f = Fernet(key)
    encrypted = f.encrypt(text.encode())  # Encrypt the text
    return encrypted.decode(), key.decode()  # Return encrypted text and key

# Decrypt the encrypted text using the saved key
def decrypt_data(encrypted_text, key):
    f = Fernet(key.encode())
    return f.decrypt(encrypted_text.encode()).decode()

# Navigate to another page
def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()  # Refresh the Streamlit app

# ---------------------- Pages ----------------------

# Home Page
def home_page():
    st.title("🔐 Encrypted Data Vault")
    st.write("Welcome. Please select an operation:")

    if st.button("➕ Store New Data"):
        go_to("store")

    if st.button("🔓 Retrieve Encrypted Data"):
        go_to("retrieve")

# Page to store encrypted data
def store_page():
    st.title("➕ Store New Data")

    # User inputs
    data_id = st.text_input("Enter a unique Data ID:")
    text = st.text_area("Enter the text to encrypt:")
    passkey = st.text_input("Enter a secure passkey:", type="password")

    if st.button("🔒 Store"):
        if not data_id or not text or not passkey:
            st.warning("Please fill in all fields.")
        elif data_id in st.session_state.data_store:
            st.error("This Data ID already exists!")
        else:
            # Encrypt and store the data
            encrypted, key = encrypt_data(text, passkey)
            st.session_state.data_store[data_id] = {
                "encrypted_text": encrypted,
                "fernet_key": key,
                "passkey_hash": hash_passkey(passkey),
            }
            st.success("✅ Data securely stored!")

    if st.button("⬅️ Back to Home"):
        go_to("home")

# Page to retrieve and decrypt data
def retrieve_page():
    st.title("🔓 Retrieve Encrypted Data")

    data_id = st.text_input("Enter Data ID:")
    passkey = st.text_input("Enter your passkey:", type="password")

    # If data ID doesn't exist
    if data_id not in st.session_state.data_store:
        if st.button("Retrieve"):
            st.error("❌ Data ID not found.")
        return

    # If too many failed attempts, redirect to login
    if st.session_state.failed_attempts.get(data_id, 0) >= 3 and not st.session_state.authenticated:
        go_to("login")
        return

    # Try retrieving the data
    if st.button("Retrieve"):
        stored = st.session_state.data_store[data_id]
        if hash_passkey(passkey) == stored["passkey_hash"]:
            decrypted = decrypt_data(stored["encrypted_text"], stored["fernet_key"])
            st.success("✅ Decrypted Text:")
            st.code(decrypted)
            st.session_state.failed_attempts[data_id] = 0  # Reset failed attempts
        else:
            # Incorrect passkey
            st.session_state.failed_attempts[data_id] = st.session_state.failed_attempts.get(data_id, 0) + 1
            attempts = st.session_state.failed_attempts[data_id]
            if attempts >= 3:
                st.error("❌ Too many failed attempts. Please re-login.")
                go_to("login")
            else:
                st.error(f"❌ Incorrect passkey. Attempt {attempts} of 3.")

    if st.button("⬅️ Back to Home"):
        go_to("home")

# Page to login after 3 failed attempts
def login_page():
    st.title("🔐 Re-Authorization Required")
    st.warning("Too many failed attempts. Please login to continue.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Simple login system (hardcoded)
        if username == "admin" and password == "admin123":
            st.success("✅ Login successful!")
            st.session_state.authenticated = True
            st.session_state.just_logged_in = True
            time.sleep(1)
            go_to("home")
        else:
            st.error("❌ Invalid credentials.")

# ---------------------- Auto-redirect after Login ----------------------

# If just logged in, go to retrieve page automatically
if st.session_state.just_logged_in:
    st.session_state.just_logged_in = False
    go_to("retrieve")

# ---------------------- Routing ----------------------

# Page rendering based on current session state
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "store":
    store_page()
elif st.session_state.page == "retrieve":
    # If not logged in and any data ID has 3+ failed attempts, force login
    if not st.session_state.authenticated and any(v >= 3 for v in st.session_state.failed_attempts.values()):
        go_to("login")
    else:
        retrieve_page()
elif st.session_state.page == "login":
    login_page()

# ---------------------- Footer ----------------------    
# Adds two HTML line breaks and displays the developer credit in bold (HTML used for more control)

st.markdown("<br><br><br><strong>Developed by Ambreen Adnan</strong>", unsafe_allow_html=True)
