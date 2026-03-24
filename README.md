# SecVault 🔐

A secure password manager built using Flask that allows users to safely store and manage their credentials using modern encryption techniques.

---

## 🚀 Features

* 🔑 **User Authentication**

  * Secure login and registration system
  * Passwords hashed using **bcrypt**

* 🔐 **Encryption**

  * Stored credentials encrypted using **Fernet (AES-based symmetric encryption)**

* 🛡️ **Security Practices**

  * Environment variables for sensitive data (`.env`)
  * No hardcoded secrets
  * Session-based authentication

* 📂 **Vault System**

  * Add, view, and delete stored passwords
  * User-specific data isolation

* 🎨 **UI**

  * Clean responsive interface using Bootstrap
  * Search and copy-to-clipboard functionality

---

## 🧱 Tech Stack

* **Backend:** Flask (Python)
* **Database:** MySQL
* **Encryption:** Cryptography (Fernet)
* **Hashing:** bcrypt
* **Frontend:** HTML, CSS, Bootstrap

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Coddr77/Secvault.git
cd Secvault
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create `.env` file

```env
SECRET_KEY=your_secret_key
FERNET_KEY=your_fernet_key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=secure_vault
```

### 4. Run the application

```bash
python app.py
```

---

## 🗄️ Database Schema

### Users Table

| Column               | Type     |
| -------------------- | -------- |
| user_id              | INT (PK) |
| username             | VARCHAR  |
| master_password_hash | TEXT     |

### Vault Table

| Column             | Type     |
| ------------------ | -------- |
| vault_id           | INT (PK) |
| user_id            | INT (FK) |
| site_name          | VARCHAR  |
| site_username      | VARCHAR  |
| encrypted_password | TEXT     |

---

## 🔒 Security Overview

* Passwords are **hashed using bcrypt** (not reversible)
* Stored credentials are **encrypted using Fernet**
* Secrets are managed via **environment variables**
* Basic access control enforced per user

---

## ⚠️ Disclaimer

This project is for educational purposes and demonstrates fundamental security practices. It is not production-ready and may require additional hardening for real-world deployment.

---

