Bilkul! Yahaan aapka polished and nicely formatted **`README.md`** content hai — aap isey as it is copy-paste kar sakte ho into your README file:

---

```markdown
# 🔐 Python-05-Assignment: Secure Data Encryption System Using Streamlit

## 🔒 Encrypted Data Vault  
A simple yet secure Streamlit web application to **encrypt, store, and retrieve** sensitive text data using passkey-based symmetric encryption.

📚 _Built as part of the Modern AI Python Programming assignment._

---

## ✨ Features

- 🔐 **Fernet Encryption** – Secure your data with symmetric encryption.  
- 🔑 **Passkey Protection** – Each entry is secured with a unique passkey.  
- 🧠 **Session Management** – User progress is maintained via session state.  
- 🚫 **Brute-force Protection** – 3 failed attempts trigger login validation.  
- 🛡️ **Hashing with SHA-256** – Ensures passkey security and integrity.  

---

## 🧪 Technologies Used

| Technology     | Purpose                        |
|----------------|--------------------------------|
| `Streamlit`    | Web UI                         |
| `cryptography` | Encryption (Fernet)            |
| `hashlib`      | Passkey hashing                |
| `time`         | Session & delay handling       |

---

## ⚙️ Installation

Install the required packages:

```bash
pip install streamlit cryptography
```

> Or if you're using `uv`:

```bash
uv add streamlit cryptography
```

---

## 🚀 Run the App

```bash
streamlit run app.py
```

---

## 🔐 Re-login Protection

If a user enters the wrong passkey **3 times**, they are redirected to a **login page** for verification.

**Default Login Credentials:**

- 👤 Username: `admin`  
- 🔒 Password: `admin123`

---

## 🧭 Application Flow

1. **Home Page** – Choose to store or retrieve encrypted data  
2. **Store Page** – Enter unique Data ID, text, and secure passkey  
3. **Retrieve Page** – Retrieve and decrypt using Data ID and passkey  
4. **Login Page** – Triggered after 3 failed attempts for added security

---

## 📌 Notes

- Encrypted data and session state are stored **in memory (Streamlit session only)**  
- This project is for **educational/demo purposes only** and not recommended for production without additional security measures.

---

##  Developer

**Ambreen Adnan**  
