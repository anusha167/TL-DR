import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_notification(to_email, title, url):
    """Sends an email notification when an article is summarized"""
    
    from_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    
    if not from_email or not password:
        print("Email credentials not set — skipping email")
        return
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"TL;DR — Your article is ready!"
    msg["From"] = from_email
    msg["To"] = to_email
    
    html = f"""
    <html>
    <body style="font-family: Inter, sans-serif; background: #0f0f0f; color: #ffffff; padding: 40px;">
        <h1 style="color: #7C3AED;">TL;DR ✦</h1>
        <p style="font-size: 18px;">Your article has been summarized and is ready to read!</p>
        <h2 style="color: #ffffff;">{title}</h2>
        <p style="color: #aaaaaa;">Original: <a href="{url}" style="color: #7C3AED;">{url}</a></p>
        <a href="http://localhost:3000" 
           style="background: #7C3AED; color: white; padding: 12px 24px; 
                  border-radius: 8px; text-decoration: none; display: inline-block; margin-top: 16px;">
            View Summary on Dashboard →
        </a>
        <p style="color: #555; margin-top: 40px; font-size: 12px;">TL;DR — because you saved it but never read it.</p>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(html, "html"))
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Email failed: {e}")