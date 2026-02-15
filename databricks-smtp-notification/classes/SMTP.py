import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

class GmailSMTP:
    def __init__(self, email_address: str, app_password: str):
        """
        Initialize the Gmail SMTP client.
        :param email_address: Your Gmail email address
        :param app_password: Gmail App Password (not your normal password)
        """
        self.email_address = email_address
        self.app_password = app_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_email(self, to_address: str, subject: str, body: str, attachments: list = None):
        """
        Send an email via Gmail SMTP.
        :param to_address: Recipient email
        :param subject: Email subject
        :param body: Email body (plain text)
        :param attachments: Optional list of file paths to attach
        """
        # Create a MIMEMultipart message
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = to_address
        msg['Subject'] = subject

        # Attach the body
        msg.attach(MIMEText(body, 'html'))

        # Attach files if any
        if attachments:
            for file_path in attachments:
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename={os.path.basename(file_path)}'
                    )
                    msg.attach(part)
                else:
                    print(f"Warning: File {file_path} not found, skipping attachment.")

        # Send email via SMTP
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.app_password)
                server.send_message(msg)
                print(f"Email sent successfully to {to_address}")
        except Exception as e:
            print(f"Failed to send email: {e}")


