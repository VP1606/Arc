import email
import os
import csv_handler
import config_holder

def handle(message):
    approved_senders = config_holder.fetch_configs()
    print(approved_senders)
    if (email.utils.parseaddr(message["from"])[1]) in approved_senders:
        print("From Approved Sender!")
        if message.is_multipart():
            found = False
            for part in message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                fileName = part.get_filename()
                if bool(fileName) and '.csv' in fileName:
                    print(f"Found CSV! {fileName}")
                    found = True

                    filePath = os.path.join('../temp/collected.csv')
                    fp = open(filePath, 'w')
                    fp.write(part.get_payload(decode=True).decode("utf-8"))
                    fp.close()

                    break
                
            if found is False:
                print("Cannot find CSV!")
                return
            
            final_result = csv_handler.handle(sql_url=approved_senders[email.utils.parseaddr(message["from"])[1]])
            print(final_result)
            return

        else:
            print("NOT MULTIPART --- Cannot find attachment!")
            return

    else:
        print("Unknown Sender!")
        return
