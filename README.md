# Resource Sharing Platform

A community-based **Streamlit** application that allows people living in the same area to request and provide help to their neighbors. The application uses **SQLite** for data storage, **bcrypt** for secure password hashing, and **UltraMsg WhatsApp API** for OTP verification and notifications.

---

# 📌 Features

### 👤 User Registration

* Register using:

  * Full Name
  * Phone Number
  * Address
  * Area Code
  * Password
* OTP verification through WhatsApp.
* Passwords securely hashed using **bcrypt**.

---

### 🔐 User Login

* Secure login using phone number and password.
* Password verification with bcrypt.
* Session management using Streamlit session state.

---

### 🆘 Request Help

Users can:

* Submit help requests.
* Automatically notify neighbors living in the same area.
* Store requests in the SQLite database.

---

### 🤝 Fulfill Requests

Neighbors can:

* View active help requests from their area.
* Contact the requester directly.
* Send response messages through WhatsApp.

---

### 👤 Account Management

Users can:

* View profile information.
* Delete their account after OTP verification.
* Remove all associated help requests upon account deletion.

---

### 🔒 Security

* Password hashing with bcrypt.
* OTP expires after **5 minutes**.
* Input validation for:

  * Phone number
  * Area code
  * Password length
* SQLite parameterized queries help prevent SQL injection.

---

# 🛠️ Technologies Used

* Python 3
* Streamlit
* SQLite3
* bcrypt
* Requests
* UltraMsg WhatsApp API

---

# 📂 Project Structure

```text
Neighbor-Help-Connect/
│
├── app.py                 # Main Streamlit application
├── work.db                # SQLite database (generated automatically)
├── requirements.txt
├── README.md
└── assets/                # Optional images/icons
```

---

# ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Neighbor-Help-Connect.git

cd Neighbor-Help-Connect
```

### 2. Create a virtual environment (Optional)

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 📦 Required Packages

Example `requirements.txt`

```text
streamlit
requests
bcrypt
```

---

# 🗄️ Database

The application automatically creates a SQLite database named:

```text
work.db
```

Tables:

### users

| Column   | Description     |
| -------- | --------------- |
| name     | User name       |
| phone    | Primary Key     |
| address  | User address    |
| area     | Area code       |
| password | Hashed password |

---

### help_requests

| Column  | Description      |
| ------- | ---------------- |
| id      | Primary Key      |
| name    | Requester's name |
| phone   | Phone number     |
| address | Address          |
| area    | Area code        |
| request | Help request     |
| time    | Timestamp        |

---

# 📲 WhatsApp Integration

This project uses the **UltraMsg API** to:

* Send OTPs
* Notify neighbors
* Send response messages

Update the following variables with your own credentials before deployment:

```python
INSTANCE_ID = "YOUR_INSTANCE_ID"

TOKEN = "YOUR_API_TOKEN"

API_URL = "https://api.ultramsg.com/YOUR_INSTANCE_ID/"
```

> **Important:** Never commit real API keys or tokens to a public GitHub repository. Use environment variables or a `.env` file for production deployments.

---

# 🚀 Workflow

1. User registers.
2. OTP is sent via WhatsApp.
3. User verifies OTP.
4. Password is securely stored.
5. User logs in.
6. User submits a help request.
7. Neighbors in the same area receive notifications.
8. Neighbors respond through the application.
9. Requester receives responder details via WhatsApp.

---

# 🔮 Future Improvements

* Forgot Password functionality
* Google Maps integration
* Live chat between users
* Volunteer verification
* Admin dashboard
* Request status (Pending/Accepted/Completed)
* Image upload support
* Email notifications
* Location-based matching using GPS
* Cloud database (MySQL/PostgreSQL/Firebase)
* Docker support
* Deployment on Streamlit Community Cloud or Render

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a new branch.

```bash
git checkout -b feature-name
```

3. Commit your changes.

```bash
git commit -m "Added new feature"
```

4. Push to your branch.

```bash
git push origin feature-name
```

5. Open a Pull Request.

---

# 👨‍💻 Developer

**Sahil Rabani**

GitHub: https://github.com/sahil-rabani

---

## ⭐ If you found this project useful, consider giving it a star on GitHub!
