###########################
# Analysis.py Code        #
#                         #
# Pietro Giampa, Jan 2022 #
###########################

## Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Adding Averages to the DataFrame
# Need to specify origin DataFrame, original category, and # of days
# -----
# crypto - Pandas DataFrame
# category - String
# days - Integer
import smtplib, ssl

def send_email_1(user, pwd, recipient, subject, body):
    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body
    message = 'From: %s\nTo: %s\nSubject: %s\n\n%s' % (FROM, ", ".join(TO), SUBJECT, TEXT)
    # SMTP_SSL Example
    server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server_ssl.ehlo() # optional, called by login()
    server_ssl.login(user, pwd)  
    # ssl server doesn't support or need tls, so don't call server_ssl.starttls() 
    server_ssl.sendmail(user, TO, message)
    server_ssl.close()
    print('successfully sent the mail')
    

send_email_1('giampapietro@gmail.com', 'qtbhvvwurtedunqb', 'danikaadam@gmail.com', 'Test Email from Python', 'Hi Gorgeous, I love you. \n Pietro')
