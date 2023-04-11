import configparser
import ssl
import base64
ssl._create_default_https_context = ssl._create_unverified_context
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sendgrid.helpers.mail import Attachment, FileContent, FileName, FileType, Disposition

config = configparser.ConfigParser()
config.read("config.ini")


def sendMailUsingSendGrid(API, from_email, to_emails, subject, html_content, attachment_paths):
    if API != None and from_email != None and len(to_emails) > 0:
        message = Mail(from_email=from_email,
                       to_emails=["Email_Address_Here", "Email_Address_Here"],
                       subject=subject,
                       html_content=html_content)

        for attachment_path in attachment_paths:
            with open(attachment_path, "rb") as f:
                file_content = f.read()
            attachment = Attachment()
            attachment.file_content = FileContent(base64.b64encode(file_content).decode())
            attachment.file_name = FileName(attachment_path.split("/")[-1])
            attachment.disposition = Disposition("attachment")
            attachment.file_type = FileType("image/jpeg")
            message.attachment = attachment

        try:
            sg = SendGridAPIClient(API)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(str(e))


try:
    settings = config["SETTINGS"]
except:
    settings = {}

API = settings.get("APIKEY", None)
from_email = settings.get("FROM", None)
to_emails = settings.get("TO", "")
# Email Subject Here
subject = "Praava Bulk Email With Attachment Testing"
# HTML Code Here
html_content = "<html><body><h1>Welcome To Praava!</h1><p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Blanditiis voluptates reprehenderit accusamus animi, nostrum ullam debitis dolorum porro amet cupiditate?</p></body></html>"
# Attachment Add Here
attachment_paths = ["Images/praava.jpeg", "Images/abc.pdf"]

sendMailUsingSendGrid(API, from_email, to_emails, subject, html_content, attachment_paths)