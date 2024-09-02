import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import requests
import http.client


class EmailSender:
    def __init__(self, sender_email: str, sender_password: str):
        self.sender_email = sender_email
        self.sender_password = sender_password

    def _send_gmailnator_email(self, receiver_email, subject, body):
        conn = http.client.HTTPSConnection("gmailnator.p.rapidapi.com")

        payload = (
            f'{{"email":"{receiver_email}","subject":"{subject}","body":"{body}"}}'
        )
        headers = {
            "x-rapidapi-key": "465c352967msh695c39899a98d6bp1afb37jsn625df2362b2b",
            "x-rapidapi-host": "gmailnator.p.rapidapi.com",
            "Content-Type": "application/json",
        }

        conn.request("POST", "/generate-email", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    def send_temp_email(self, receiver_email, subject, body, client=None):
        if client == "gmailnator":
            self._send_gmailnator_email(receiver_email, subject, body)
        data = {
            "f": "temp@sharklasers.com",  # Sender's email
            "to": receiver_email,
            "subject": subject,
            "body": body,
        }
        response = requests.post(
            "https://api.guerrillamail.com/ajax.php?f=send_email", data=data
        )
        if response.status_code == 200:
            print("Email sent successfully")
        else:
            print("Failed to send email")

    def send_email(self, receiver_email: str, subject: str, body: str):
        # Define email sender and server details

        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))

        # Create a MIMEText object to represent the email
        # Create a MIMEText object to represent the email
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            # Connect to the SMTP server and send the email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, receiver_email, text)
            print(f"Email sent to {receiver_email}")
        except Exception as e:
            print(f"Failed to send email. Error: {str(e)}")
        finally:
            server.quit()
