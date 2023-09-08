import email
import os
import csv_handler
import config_holder
import responder
import pdf_handler

def handle(message):

    approved_senders = config_holder.fetch_configs()
    sender = email.utils.parseaddr(message["from"])[1]

    if (email.utils.parseaddr(message["from"])[1]) in approved_senders:
        print("From Approved Sender!")
        approved_types = approved_senders[email.utils.parseaddr(message["from"])[1]][1]

        if message.is_multipart():
            found = False
            PDF_Mode = False
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
                elif bool(fileName) and '.pdf' in fileName:
                    print(f"Found PDF! {fileName}")
                    if 'pdf' in approved_types:
                        found = True
                        PDF_Mode = True
                        filePath = os.path.join('../temp/collected.pdf')
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
                    else:
                        print("Sender Not allowed to send PDF!")
                        found = False
                    break
                
            if found is False:
                print("Cannot find CSV!")
                response = 'Hello, \n There was an error in reading your email; the attached CSV file could not be found. \n Please verify that the attachment was included and try again.'
                responder.send_response(reciever=sender, subject='ARC Importer: No attachment!', message=response)
                return
            
            if PDF_Mode:
                print("PDF MODE...")
                if 'vcpremakantha' in email.utils.parseaddr(message["from"])[1]:
                    print("TEST MODE!")
                    final_result = pdf_handler.handle_wrapper_verbose(testing=True)
                else:
                    final_result = pdf_handler.handle_wrapper(testing=False)
            else:
                final_result = csv_handler.handle(sql_urls=approved_senders[email.utils.parseaddr(message["from"])[1]][0])
                print(final_result)

            if final_result[0] is True:
                if PDF_Mode:
                    response = 'Good Day User, \n Your PDF email submission was processed sucessfully! \n Thanks'
                else:
                    response = 'Good Day User, \n Your CSV email submission was processed sucessfully! \n Thanks'
                responder.send_response(reciever=sender, subject='ARC Importer: Success!', message=response)
            else:
                if PDF_Mode is True:
                    response = f'Hello User, \n An error occurred when processing the PDF file you submitted. Here is the raw output: \n {final_result[1]}. \n Thanks!'
                    responder.send_response(reciever=sender, subject='ARC Importer: PDF Error!', message=response)

                else:
                    if final_result[1] == 'SQL Commiting Error':
                        response = f'Hello User, \n There was an error in the SQL saving process, so we have been unable to log your invoice onto the server. \n Here is the raw error: \n {str(final_result[2])} \n Please share this with the Administrator. \n Sorry for the inconvenience.'
                        responder.send_response(reciever=sender, subject='ARC Importer: SQL Error!', message=response)
                    else:
                        response = 'Hello User, \n There was an error in validating the CSV file you attached to the email; there were some rows that we were expecting to be there, however they were not included. \n Please re-check the file and try again. \n Thanks!'
                        responder.send_response(reciever=sender, subject='ARC Importer: CSV Error!', message=response)

            return

        else:
            print("NOT MULTIPART --- Cannot find attachment!")
            response = 'Hello, \n There was an error in reading your email; the attached CSV file could not be found. \n Please verify that the attachment was included and try again.'
            responder.send_response(reciever=sender, subject='ARC Importer: No attachment!', message=response)
            return

    else:
        print("Unknown Sender!")
        return
