import imaplib
import smtplib
import ssl

import streamlit as st


# Page 1: Account Connection
def connect_account():
    st.title("Connect Your Email Account")
    st.write("Please enter your email credentials to connect your account.")

    sender_email = st.text_input("Email Address:")
    sender_password = st.text_input("Password:", type="password")
    connect_button = st.button("Connect")

    if connect_button:
        # Check if the provided credentials are valid
        if is_valid_credentials(sender_email, sender_password):
            st.success("Account connected successfully!")
            st.write("You can now go to the 'Send Emails' page to send emails.")
            st.write("[Send Emails](#send-emails)")
            # Store the credentials for later use
            st.session_state["sender_email"] = sender_email
            st.session_state["sender_password"] = sender_password
        else:
            st.error("Invalid email address or password. Please try again.")

# Function to validate email credentials (You can implement your own validation logic)
def is_valid_credentials(email, password):
    try:
        # Connect to the IMAP server
        imap_server = imaplib.IMAP4_SSL("imap.gmail.com")
        # Log in with the provided email and password
        imap_server.login(email, password)
        # Close the connection
        imap_server.logout()
        return True
    except imaplib.IMAP4.error as e:
        print(f"IMAP error: {e}")
        return False

# Page 2: Send Emails

def send_email(sender_email, sender_password, receiver_email, subject, body):
    host = "smtp.gmail.com"
    port = 465
    context = ssl.create_default_context()

    message = f"""\
    Subject: {subject}

    {body}
    """

    with smtplib.SMTP_SSL(host,port,context=context) as server :
        server.login(sender_email,sender_password)
        server.sendmail(sender_email,receiver_email,message )


def send_emails():
    st.title("Send Emails")
    st.write("Welcome to the Bulk Email Sender!")
    sender_email = st.session_state.get("sender_email")
    sender_password = st.session_state.get("sender_password")

    if sender_email is None or sender_password is None:
        st.warning("Please connect your email account first.")
        st.write("[Connect Your Email Account](#connect-your-email-account)")
        return

    subject = st.text_input("Subject:")
    body = st.text_area(label="", value="Write your email...")
    email_list = st.file_uploader("Upload Email list")

    if email_list is not None:
        file_contents = [line.decode("utf-8").strip() for line in email_list]

    send_button = st.button("Send")

    if send_button:
        for receiver_email in file_contents:
            status = send_email(sender_email, sender_password, receiver_email, subject, body)
            st.write(f"Email sent successfully to {receiver_email}")

# Main function to run the app
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Connect Your Email Account", "Send Emails"])

    if page == "Connect Your Email Account":
        connect_account()
    elif page == "Send Emails":
        send_emails()

if __name__ == "__main__":
    main()
