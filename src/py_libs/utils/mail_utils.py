from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from src.private_env import mail_password, sender_mail_id, receiver_mail_ids

def send_mails(subject:str, body_text:str):
    # list of email_id to send the mail
    for dest in receiver_mail_ids:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(sender_mail_id, mail_password)
        message = "Message_you_need_to_sendXDDDD"


        msg = MIMEMultipart()  # instance of MIMEMultipart
        msg['From'] = sender_mail_id
        msg['To'] = dest
        msg['Subject'] = subject
        msg.attach(MIMEText(body_text, 'plain'))

        text = msg.as_string()

        s.sendmail(sender_mail_id, dest, text)
        s.quit()