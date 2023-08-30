import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_response(reciever, subject, message):
    try:
        password = ""
        with open("imap_cred.txt", "r") as f:
            password = f.read().strip()
            f.close()

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("arcsys.importer@gmail.com", password)

        message_pack = MIMEMultipart()
        message_pack['From'] = "arcsys.importer@gmail.com"
        message_pack['To'] = reciever
        message_pack['Subject'] = subject
        message_pack.attach(MIMEText(message, 'plain'))

        # sending the mail
        s.sendmail("arcsys.importer@gmail.com", reciever, message_pack.as_string())
        s.quit()
        return
    except Exception as e:
        print(f"Responder error! ::: {e}")
        return
