from datetime import datetime
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl
import re


def creds(key):
    credentials = open("config/logger.config")
    found = 0
    for line in credentials:
        search = re.findall(f'{key}=(.*)',line)
        if search:
            found += 1
            return(search[0])
    if found == 0:
        return "key not found"


class Logger:
    '''creates log files/entries
    log = Logger("log.txt", "LOG TEST")
    log.text("Message to log.")
    print last n lines of text
    log.debug(int)
    '''

    def __init__(self, filename, logging_header, gmail_email = None, gmail_password = None, email_list = None, email_subject = None):
        self.filename = filename
        self.logging_header = logging_header
        self.gmail_email = gmail_email
        self.gmail_password = gmail_password
        self.email_list = email_list
        self.email_subject = email_subject


    def text(self, log_text, send_mail=False,):
        '''print string argument to log.filename'''

        log_line = (f"{datetime.strftime(datetime.now(),'[ %m-%d-%Y %I:%M:%S %p ]')} "\
                    f"[{self.logging_header}] {log_text} \r")

        print(log_line)
        os.makedirs(os.path.dirname('logs/'), exist_ok=True)
        log_file = open(f"logs/{self.filename}", 'a+', encoding='utf-8')
        log_file.write(log_line)
        log_file.close()

        if send_mail == True:
            email_body = log_line
            email_html = f"<p>{log_line}</p>"

            sender_email = self.gmail_email
            password = self.gmail_password

            email_list = self.email_list


            for receiver_email in email_list:
                message = MIMEMultipart("alternative")
                message["Subject"] = self.email_subject
                message["From"] = sender_email
                message["To"] = receiver_email

                # Create the plain-text and HTML version of your message
                text = f"""\
                {email_body}
                Updated {datetime.now()}"""
                html = f"""\
                <html>
                    <body>
                    {email_html}
                    </body>
                </html>
                """

                # Turn these into plain/html MIMEText objects
                part1 = MIMEText(text, "plain")
                part2 = MIMEText(html, "html")

                # Add HTML/plain-text parts to MIMEMultipart message
                # The email client will try to render the last part first
                message.attach(part1)
                message.attach(part2)

                # Create secure connection with server and send email
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(
                        sender_email, receiver_email, message.as_string()
                    )




    def debug(self, lines, hide_errors=False):
        '''print string argument to log.filename'''

        if not os.path.isdir("logs/"):
            print("[ DEBUG ] Logs directory not found.")
        else:
            if not os.path.isfile(f"logs/{self.filename}"):
                print("[ DEBUG ] Log file not found.")
            else:

                log_file = open(f"logs/{self.filename}", 'r', encoding='utf-8')
                log_lines = log_file.readlines()

                if len(log_lines) >= lines:
                    for line in reversed(range(lines)):
                        print((f"[ DEBUG ] {log_lines[-(line+1)]}").rstrip('\n'))
                else:
                    for line in reversed(range(len(log_lines))):
                        print((f"[ DEBUG ] {log_lines[-(line+1)]}").rstrip('\n'))
                    if hide_errors is False:
                        print(f'[ DEBUG ] Unable to print {lines-len(log_lines)}/{lines}'\
                              f' requested lines. Lines in file: {len(log_lines)}')