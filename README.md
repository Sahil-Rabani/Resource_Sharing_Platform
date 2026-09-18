# 🤝 Resource Sharing Platform — Sahil Rabani

> **Resource Sharing Platform by Sahil Rabani** — a community-driven platform that connects people who need help with neighbors who are willing to provide it.

**Resource Sharing Platform** is a **Python and Streamlit-based community assistance application developed by Sahil Rabani**. The platform allows people within the same locality to request help, discover nearby requests, and communicate with other community members through WhatsApp.

The application combines **Python, Streamlit, SQLite, bcrypt, and the UltraMsg WhatsApp API** to provide user authentication, OTP verification, localized help requests, and WhatsApp-based notifications.

---

## 👨‍💻 About the Project

The **Resource Sharing Platform by Sahil Rabani** was created to provide a simple and accessible way for people in the same community to help one another.

Users can:

- Create an account and verify their phone number.
- Submit requests for assistance.
- Discover active help requests from their local area.
- Respond to requests and communicate through WhatsApp.
- Manage their account and associated requests securely.

This project demonstrates practical experience in **Python development, web application development, database management, authentication, API integration, and application security**.

---

## ✨ Key Features

### 👤 User Registration

Users can create an account using:

- Full Name
- Phone Number
- Address
- Area Code
- Password

Registration includes:

- WhatsApp-based OTP verification
- Password hashing using **bcrypt**
- Input validation
- Secure account creation

---

### 🔐 Authentication & Login

The application provides authenticated access using:

- Phone number and password
- bcrypt password verification
- Streamlit session-state based session management
- OTP-based verification for sensitive account operations

---

### 🆘 Request Help

Users can create help requests for people in their local community.

Features include:

- Submit a description of the required help
- Associate requests with a specific area
- Store requests in SQLite
- Notify relevant neighbors through WhatsApp

---

### 🤝 Fulfill Community Requests

Community members can:

- View active help requests from their area
- Review request information
- Contact the requester
- Respond through WhatsApp

This creates a simple communication workflow between people requesting assistance and people willing to help.

---

### 👤 Account Management

Users can:

- View their profile information
- Manage their account
- Delete their account after OTP verification
- Remove associated help requests when deleting their account

---

## 🔒 Security

Security considerations implemented in the application include:

- **bcrypt** password hashing
- OTP expiration after **5 minutes**
- Phone number validation
- Area-code validation
- Password-length validation
- SQLite parameterized queries to help prevent SQL injection
- OTP verification for sensitive account operations

> **Security Note:** Never commit real API credentials, passwords, tokens, or other secrets to a public GitHub repository.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **Python 3** | Application development |
| **Streamlit** | Web application framework |
| **SQLite3** | Database and persistent storage |
| **bcrypt** | Secure password hashing |
| **Requests** | HTTP/API communication |
| **UltraMsg API** | WhatsApp messaging and OTP delivery |

---

## 🏗️ Architecture Overview

`
                         ┌─────────────────────┐
                         │       User          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Streamlit UI    │
                         └──────────┬──────────┘
                                    │
                   ┌────────────────┼────────────────┐
                   │                │                │
                   ▼                ▼                ▼
             Authentication    Help Requests    Account Management
                   │                │                │
                   └────────────────┼────────────────┘
                                    │
                      ┌─────────────┴─────────────┐
                      │                           │
                      ▼                           ▼
               ┌─────────────┐            ┌─────────────┐
               │   SQLite    │            │  UltraMsg   │
               │   Database  │            │ WhatsApp API│
               └─────────────┘            └─────────────┘


---

 ## 📂 Project Structure


Resource_Sharing_Platform/
│
├── app.py                 # Main Streamlit application
├── work.db                # SQLite database (generated automatically)
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── assets/                # Images, icons, and other assets

---

## ⚙️ Installation

### 1\. Clone the Repository

git clone https://github.com/Sahil-Rabani/Neighbor-Help-Connect.git

cd Neighbor-Help-Connect


 ### 2\. Create a Virtual Environment

 Creating a virtual environment is recommended.

 #### Windows


python -m venv venv

venv\Scripts\activate


 #### Linux / macOS


python3 -m venv venv

source venv/bin/activate


 ### 3\. Install Dependencies


pip install -r requirements.txt


---

 ## 🔑 Configuration

 The application uses the **UltraMsg WhatsApp API** for OTP verification and notifications.

 Configure your API credentials securely using environment variables or another secret-management solution.

 Example:


INSTANCE_ID = "YOUR_INSTANCE_ID"
TOKEN = "YOUR_API_TOKEN"
API_URL = "https://api.ultramsg.com/YOUR_INSTANCE_ID/"


 ### ⚠️ Important

 Never commit real API credentials to GitHub.

 For production deployments, consider using:

 - Environment variables
- '.env' files excluded through '.gitignore'
- Platform-specific secret management

---

 ## ▶️ Running the Application

 Start the Streamlit application using:

streamlit run app.py

 The application will then be available through the local URL provided by Streamlit.

---

 ## 📦 Dependencies

 The primary dependencies include:

streamlit
requests
bcrypt

 Install them using:

pip install -r requirements.txt

---

 ## 🗄️ Database

 The application uses **SQLite** for persistent data storage.

 A database named:

work.db

 is created automatically by the application.

 ### `users`

 | Column | Description |
| --- | --- |
| `name` | User's full name |
| `phone` | User's phone number / primary identifier |
| `address` | User's address |
| `area` | Local area code |
| `password` | bcrypt-hashed password |

### `help_requests`

 | Column | Description |
| --- | --- |
| `id` | Unique request identifier |
| `name` | Requester's name |
| `phone` | Requester's phone number |
| `address` | Requester's address |
| `area` | Requester's area |
| `request` | Description of required help |
| `time` | Request creation timestamp |

---

 ## 📲 WhatsApp Integration

 The **Resource Sharing Platform by Sahil Rabani** integrates the **UltraMsg WhatsApp API** to provide communication and notification functionality.

 WhatsApp is used for:

 - 📱 OTP verification
- 🔔 Help-request notifications
- 💬 Response communication
- 📩 Sharing responder/requester information

---

 ## 🔄 Application Workflow

1. User creates an account
          ↓
2. OTP is sent through WhatsApp
          ↓
3. User verifies the OTP
          ↓
4. Password is securely hashed
          ↓
5. User logs into the application
          ↓
6. User submits a help request
          ↓
7. Relevant neighbors are notified
          ↓
8. Neighbor reviews the request
          ↓
9. Neighbor responds
          ↓
10. Requester receives responder information

---

 ## 🎯 Project Highlights

 This project demonstrates practical experience with:

 - **Python application development**
- **Streamlit web application development**
- **SQLite database management**
- **User authentication**
- **Password hashing**
- **OTP-based verification**
- **REST API integration**
- **WhatsApp API integration**
- **Session management**
- **Input validation**
- **Parameterized SQL queries**
- **Community-oriented application design**

---

 ## 🚀 Future Enhancements

 Potential improvements include:

- [ ] Forgot-password functionality
- [ ] Request status management
- [ ] Pending / Accepted / Completed request states
- [ ] Google Maps integration
- [ ] GPS-based location matching
- [ ] Live user-to-user chat
- [ ] Volunteer verification
- [ ] Admin dashboard
- [ ] Image attachments for requests
- [ ] Email notifications
- [ ] Improved notification preferences
- [ ] Cloud database support
- [ ] Docker containerization
- [ ] Deployment on Streamlit Community Cloud or Render
- [ ] Improved scalability and production deployment architecture

---

 ## 🤝 Contributing

 Contributions, suggestions, and improvements are welcome.

 ### 1\. Fork the Repository

 Create your own fork of the project.

 ### 2\. Create a Feature Branch

git checkout -b feature-name

 ### 3\. Make Your Changes

 Implement your feature or improvement.

 ### 4\. Commit Your Changes

git add .
git commit -m "Add new feature"

 ### 5\. Push Your Branch

git push origin feature-name

 ### 6\. Open a Pull Request

 Submit a Pull Request with a clear description of your changes.

---

 ## 👨‍💻 Developer

 ### Sahil Rabani

 **Python Developer | Software Developer**

 **Resource Sharing Platform** was designed and developed by **Sahil Rabani**.

 GitHub:\
 https://github.com/Sahil-Rabani

---

 ## ⭐ Support the Project

 If you find **Resource Sharing Platform** useful or interesting, consider giving the repository a ⭐ on GitHub.

 Your feedback, suggestions, and contributions are welcome!

---

 ## 📄 License

Resource Sharing Platform by Sahil Rabani — a community help platform built with Python, Streamlit, SQLite, bcrypt, and WhatsApp API.

# **Ignore Tags**
sahil-rabani
Sahil-Rabani
resource-sharing
community-platform
community-help
python
streamlit
sqlite
bcrypt
whatsapp-api
ultramsg
otp-authentication
