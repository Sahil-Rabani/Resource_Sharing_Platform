import mysql.connector
import streamlit as st
import requests
import random
import datetime
import bcrypt
from mysql.connector import Error

INSTANCE_ID = "instance:116840"
TOKEN = "ke9cie56ll57nyo6"
API_URL = "https://api.ultramsg.com/instance116840/"


def get_db_connection():
    try:
        db = mysql.connector.connect(
        host="your-remote-host.com",
        user="remote_user",
        password="remote_password",
        database="your_database",
        port=3306
    )

        cursor = db.cursor()
        return db, cursor
    except Error as e:
        st.error(f"Database connection failed: {e}")
        st.stop()

def initialize_database():
    db, cursor = get_db_connection()
    try:
        cursor.execute("SHOW TABLES LIKE 'users'")
        if not cursor.fetchone():
            cursor.execute("""
                CREATE TABLE users (
                    name VARCHAR(45),
                    phone VARCHAR(10) PRIMARY KEY,
                    address VARCHAR(90),
                    area VARCHAR(6),
                    password VARCHAR(255)
                )
            """)
            db.commit()

        cursor.execute("SHOW TABLES LIKE 'help_requests'")
        if not cursor.fetchone():
            cursor.execute("""
                CREATE TABLE help_requests (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(45),
                    phone VARCHAR(10),
                    address VARCHAR(90),
                    area VARCHAR(6),
                    request TEXT,
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            db.commit()
    except Error as e:
        st.error(f"Database initialization failed: {e}")
        st.stop()
    finally:
        cursor.close()
        db.close()

initialize_database()

def generate_otp():
    otp = random.randint(10000000, 99999999)
    generation_time = datetime.datetime.now()
    return otp, generation_time

def send_otp(phone_number, message, silent=False):
    if not (len(phone_number) == 10 and phone_number.isdigit()):
        if not silent:
            st.error("Invalid phone number format")
        return False
    
    formatted_number = "+91" + phone_number

    try:
        response = requests.post(
            API_URL + "messages/chat",
            data={
                "token": TOKEN,
                "to": formatted_number,
                "body": message
            },
            timeout=10
        )
        response.raise_for_status()
        if not silent:
            st.success("Message sent successfully!")
        return True
    except requests.exceptions.RequestException as e:
        if not silent:
            st.error(f"Failed to send message: {e}")
        return False

def verify_otp(user_otp, generated_otp, generation_time):
    try:
        user_otp = int(user_otp)
    except (ValueError, TypeError):
        return False
    
    time_limit = 5
    current_time = datetime.datetime.now()
    time_diff = (current_time - generation_time).total_seconds() / 60

    return time_diff <= time_limit and user_otp == generated_otp

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def register_page():
    st.title("Register")
    
    with st.form("register_form"):
        name = st.text_input("Full Name", max_chars=45)
        phone = st.text_input("Phone Number (10 digits)", max_chars=10)
        address = st.text_area("Address", max_chars=90)
        area = st.text_input("Area Code (6 digits)", max_chars=6)
        password = st.text_input("Password", type="password", max_chars=255)
        confirm_password = st.text_input("Confirm Password", type="password", max_chars=255)
        
        if st.form_submit_button("Register"):
            errors = []
            if not name.strip():
                errors.append("Name is required")
            if not (len(phone) == 10 and phone.isdigit()):
                errors.append("Phone must be 10 digits")
            if not address.strip():
                errors.append("Address is required")
            if not (len(area) == 6 and area.isdigit()):
                errors.append("Area code must be 6 digits")
            if len(password) < 8:
                errors.append("Password must be at least 8 characters")
            if password != confirm_password:
                errors.append("Passwords do not match")

            if errors:
                for error in errors:
                    st.error(error)
            else:
                db, cursor = get_db_connection()
                try:
                    cursor.execute("SELECT phone FROM users WHERE phone = %s", (phone,))
                    if cursor.fetchone():
                        st.error("This phone number is already registered")
                    else:
                        otp, generation_time = generate_otp()
                        if send_otp(phone, f"Your OTP is: {otp}"):
                            st.session_state.registration_data = {
                                "name": name,
                                "phone": phone,
                                "address": address,
                                "area": area,
                                "password": password,
                                "otp": otp,
                                "generation_time": generation_time
                            }
                            st.session_state.registration_step = "verify_otp"
                finally:
                    cursor.close()
                    db.close()

    if st.session_state.get("registration_step") == "verify_otp":
        with st.form("otp_verification"):
            user_otp = st.text_input("Enter 8-digit OTP", max_chars=8)
            if st.form_submit_button("Verify OTP"):
                if verify_otp(
                    user_otp,
                    st.session_state.registration_data["otp"],
                    st.session_state.registration_data["generation_time"]
                ):
                    db, cursor = get_db_connection()
                    try:
                        hashed_password = hash_password(st.session_state.registration_data["password"])
                        cursor.execute(
                            "INSERT INTO users (name, phone, address, area, password) VALUES (%s, %s, %s, %s, %s)",
                            (
                                st.session_state.registration_data["name"],
                                st.session_state.registration_data["phone"],
                                st.session_state.registration_data["address"],
                                st.session_state.registration_data["area"],
                                hashed_password
                            )
                        )
                        db.commit()
                        st.success("Registration successful! Please login.")
                        del st.session_state.registration_data
                        del st.session_state.registration_step
                        st.session_state.page = "login"
                        st.rerun()
                    except Error as e:
                        st.error(f"Registration failed: {e}")
                    finally:
                        cursor.close()
                        db.close()
                else:
                    st.error("Invalid OTP or OTP has expired")

def login_page():
    st.title("Login")
    
    with st.form("login_form"):
        phone = st.text_input("Phone Number", max_chars=10)
        password = st.text_input("Password", type="password", max_chars=255)

        if st.form_submit_button("Login"):
            if len(phone) == 10 and phone.isdigit():
                db, cursor = get_db_connection()
                try:
                    cursor.execute(
                        "SELECT phone, password FROM users WHERE phone = %s",
                        (phone,)
                    )
                    user = cursor.fetchone()

                    if user:
                        if check_password(password, user[1]):
                            st.session_state.logged_in = True
                            st.session_state.user_phone = phone

                            cursor.execute(
                                "SELECT name, address FROM users WHERE phone = %s",
                                (phone,)
                            )
                            user_info = cursor.fetchone()
                            if user_info:
                                st.session_state.user_name = user_info[0]
                                st.session_state.user_address = user_info[1]

                            st.session_state.page = "dashboard"
                            st.rerun()
                    else:
                        st.error("User not found\nPlease Complete registration")
                finally:
                    cursor.close()
                    db.close()
        
                            
    st.write("Don't have an account?")
    if st.button("Register"):
        st.session_state.page = "register"
        st.rerun()

def request_help():
    st.title("Request Help")

    db, cursor = get_db_connection()
    try:
        cursor.execute(
            "SELECT name, address, area FROM users WHERE phone = %s",
            (st.session_state.user_phone,)
        )
        user_data = cursor.fetchone()
    finally:
        cursor.close()
        db.close()

    if not user_data:
        st.error("User data not found")
        return

    name, address, area = user_data

    with st.form("help_request"):
        request_text = st.text_area("How can we help you?")
        if st.form_submit_button("Submit Request"):
            if not request_text.strip():
                st.error("Please enter your request")
            else:
                db, cursor = get_db_connection()
                try:
                    cursor.execute(
                        "INSERT INTO help_requests (name, phone, address, area, request) VALUES (%s, %s, %s, %s, %s)",
                        (name, st.session_state.user_phone, address, area, request_text)
                    )
                    db.commit()

                    cursor.execute(
                        "SELECT phone FROM users WHERE area = %s AND phone != %s",
                        (area, st.session_state.user_phone)
                    )
                    neighbors = cursor.fetchall()

                    message = (
                        f"New Help Request in your area from {name}\n"
                        f"Address: {address}\n"
                        f"Request: {request_text}\n\n"
                        f"Please respond through the app if you can help."
                    )

                    for neighbor in neighbors:
                        send_otp(neighbor[0], message, silent=True)

                    st.success("Your request has been submitted and neighbors have been notified!")
                finally:
                    cursor.close()
                    db.close()

def backgroundimg():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("data:image/jpeg;base64,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");
             background-attachment: fixed;
             background-size: cover;
             background-position: center;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

def fulfill_requests():
    st.title("Available Requests")

    db, cursor = get_db_connection()
    try:
        cursor.execute(
            "DELETE FROM help_requests WHERE time < NOW() - INTERVAL 12 HOUR"
        )
        db.commit()

        cursor.execute(
            "SELECT area FROM users WHERE phone = %s",
            (st.session_state.user_phone,)
        )
        user_area = cursor.fetchone()
    finally:
        cursor.close()
        db.close()

    if not user_area:
        st.error("Could not determine your area")
        return

    area = user_area[0]

    db, cursor = get_db_connection()
    try:
        cursor.execute(
            "SELECT id, name, phone, address, request, time FROM help_requests WHERE area = %s ORDER BY time DESC",
            (area,)
        )
        help_requests_list = cursor.fetchall()
    finally:
        cursor.close()
        db.close()

    if not help_requests_list:
        st.info("No help requests in your area currently")
        return

    for req in help_requests_list:
        req_id, name, phone, address, request_text, request_time = req
        with st.expander(f"Request from {name} at {request_time}"):
            st.write(f"**Address:** {address}")
            st.write(f"**Request:** {request_text}")

            if st.button(f"Contact {name}", key=f"contact_btn_{req_id}"):
                st.session_state[f"contact_clicked_{req_id}"] = True

            if st.session_state.get(f"contact_clicked_{req_id}", False):
                your_message = st.text_input(f"Enter your message for {name}", key=f"message_input_{req_id}")
                if st.button("Send Message", key=f"send_message_{req_id}"):
                    if your_message.strip():
                        responder_name = st.session_state.user_name
                        responder_phone = st.session_state.user_phone
                        responder_address = st.session_state.user_address

                        message = (
                            f"Someone responded to your help request!\n\n"
                            f"Message: {your_message}\n\n"
                            f"Responder Details:\n"
                            f"Name: {responder_name}\n"
                            f"Phone: {responder_phone}\n"
                            f"Address: {responder_address}"
                        )

                        if send_otp(phone, message):
                            st.success("Message sent! The requester will contact you if needed.")
                        else:
                            st.error("Failed to send message.")
                    else:
                        st.error("Please enter a message.")

def account_info():
    st.title("👤 Account Information")

    db, cursor = get_db_connection()
    try:
        cursor.execute(
            "SELECT name, phone, address, area FROM users WHERE phone = %s",
            (st.session_state.user_phone,)
        )
        user_info = cursor.fetchone()
    finally:
        cursor.close()
        db.close()

    if user_info:
        with st.container():
            st.markdown("""
                <div style="
                    background-color: #ffffff10;
                    padding: 25px;
                    border-radius: 15px;
                    box-shadow: 0px 0px 20px rgba(0,0,0,0.2);
                    color: white;
                ">
                    <h2 style="text-align:center;">👤 {}</h2>
                    <p><strong>📱 Phone:</strong> {}</p>
                    <p><strong>🏠 Address:</strong> {}</p>
                    <p><strong>📍 Area Code:</strong> {}</p>
                </div>
            """.format(user_info[0], user_info[1], user_info[2], user_info[3]), unsafe_allow_html=True)

            st.markdown("---")


            if st.button("❌ Delete My Account", use_container_width=True):
                otp, generation_time = generate_otp()
                if send_otp(st.session_state.user_phone, f"Your account deletion OTP is: {otp}"):
                    st.session_state.delete_data = {
                        "otp": otp,
                        "generation_time": generation_time
                    }
                    st.session_state.delete_step = "verify_otp"

    if st.session_state.get("delete_step") == "verify_otp":
        with st.form("delete_verification"):
            user_otp = st.text_input("Enter OTP received on your phone", max_chars=8)
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("✅ Confirm Delete"):
                    if verify_otp(
                        user_otp,
                        st.session_state.delete_data["otp"],
                        st.session_state.delete_data["generation_time"]
                    ):
                        db, cursor = get_db_connection()
                        try:
                            cursor.execute("DELETE FROM users WHERE phone = %s", (st.session_state.user_phone,))
                            cursor.execute("DELETE FROM help_requests WHERE phone = %s", (st.session_state.user_phone,))
                            db.commit()
                            st.success("Account deleted successfully")
                            st.session_state.logged_in = False
                            del st.session_state.user_phone
                            del st.session_state.delete_data
                            del st.session_state.delete_step
                            st.session_state.page = "login"
                            st.rerun()
                        finally:
                            cursor.close()
                            db.close()
                    else:
                        st.error("Invalid OTP or OTP has expired")
            with col2:
                if st.form_submit_button("❎ Cancel"):
                    del st.session_state.delete_data
                    del st.session_state.delete_step
                    st.rerun()


def dashboard_page():

    st.sidebar.title("Menu")
    page = st.sidebar.radio(
        "Navigation",
        ["Request Help", "Fulfill Requests", "Account Info", "Logout"]
    )
    if page == "Request Help":
        request_help()
    elif page == "Fulfill Requests":
        fulfill_requests()
    elif page == "Account Info":
        account_info()
    elif page == "Logout":
        st.session_state.logged_in = False
        del st.session_state.user_phone
        st.session_state.page = "login"
        st.rerun()

def main():
    backgroundimg()
    
    if "page" not in st.session_state:
        st.session_state.page = "login"

    if not st.session_state.get("logged_in", False):
        if st.session_state.page == "register":
            register_page()
        else:
            login_page()
    else:
        dashboard_page()

if __name__ == "__main__":
    main()
