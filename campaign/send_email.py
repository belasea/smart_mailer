
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import weasyprint
from pdf2image import convert_from_path
import datetime
import os

# Email credentials
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "jibon.belasea@gmail.com"
EMAIL_PASSWORD = "rcqtdxesqufgebtx"  # App password

# HTML string to convert
html_message = """
<html>
<head>
    <style>
        .container {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            padding: 20px;
            border-radius: 10px;
        }
        h2 {
            color: #333;
        }
        p {
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Welcome to Our Service!</h2>
        <p>Hello, this is a <b>test email</b> with an HTML message.</p>
        <p>Thank you for using our service.</p>
    </div>
</body>
</html>
"""

# Generate file names
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
pdf_file = f"html_to_pdf_{timestamp}.pdf"
png_file = f"html_to_image_{timestamp}.png"

# Convert HTML to PDF
weasyprint.HTML(string=html_message).write_pdf(pdf_file)
print(f"✅ HTML converted to PDF: {pdf_file}")

# Convert PDF to PNG
pages = convert_from_path(pdf_file, dpi=300)
pages[0].save(png_file, "PNG")
print(f"✅ PDF converted to PNG: {png_file}")

# Email sending function
def send_png_email(to_emails, subject, attachment_path):
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        for email in to_emails:
            msg = MIMEMultipart()
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = email
            msg["Subject"] = subject

            # Attach PNG
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("image", "png")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_path)}")
                msg.attach(part)

            server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
            print(f"✅ Email sent to: {email}")

        server.quit()
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# Send email
recipient_list = ["jibon.py@gmail.com", "laila.belaface@gmail.com"]
send_png_email(recipient_list, "🖼️ HTML Converted to PNG", png_file)
