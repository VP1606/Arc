import email
approved_senders = ["vcpremakantha@gmail.com"]

def handle(message):
    if (email.utils.parseaddr(message["from"])[1]) in approved_senders:
        print("From Approved Sender!")
        if message.is_multipart():
            for part in message.walk():
                content_type = part.get_content_type()
                filename = part.get_filename()

                if content_type == "text/csv" and filename:
                    print("CSV attachment found:", filename)
                else:
                    print(f"Unknown File type! ---> {content_type}")
        else:
            print("Cannot find attachment!")

    else:
        print("Unknown Sender!")
        return