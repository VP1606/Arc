import imaplib
import email
import time
import importlib
import email_handler, csv_handler, config_holder, responder, pdf_handler

def get_mail_client(email_address):
    print("Connecting IMAP...")
    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT = 993
    
    password = ""
    with open("imap_cred.txt", "r") as f:
        password = f.read().strip()

    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(email_address, password)
    print("Connected IMAP!")
    return mail

mail = get_mail_client("arcsys.importer@gmail.com")
print("Launched!")
print("")

while True:
    importlib.reload(email_handler)
    importlib.reload(csv_handler)
    importlib.reload(config_holder)
    importlib.reload(responder)
    importlib.reload(pdf_handler)
    # print("SCAN")

    try:
        mail.select("inbox")
        result, data = mail.search(None, "UNSEEN")  # Search for unread messages
        
        if result == "OK":
            for num in data[0].split():
                typ, msg_data = mail.fetch(num, "(RFC822)")
                if typ == "OK":
                    email_message = email.message_from_bytes(msg_data[0][1])
                    print("New email received:")
                    print("Subject:", email_message["subject"])
                    print("From:", email.utils.parseaddr(email_message["from"])[1])
                    print("----\n")
                    email_handler.handle(message=email_message)
        else:
            print("Error searching for emails.")

    except imaplib.IMAP4.abort as e:
        print(f"Caught IMAP4 Abort error! ::: {str(e)}")
        print("Restarting IMAP Connection...")
        mail = get_mail_client("arcsys.importer@gmail.com")
        print("Launched!")
        print("")

    except Exception as e:
        print(f"Unexpected error! ::: {str(e)}")
        print("Restarting IMAP Connection...")
        mail = get_mail_client("arcsys.importer@gmail.com")
        print("Launched!")
        print("")
    
    time.sleep(5)