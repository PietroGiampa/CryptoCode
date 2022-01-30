###########################
# Analysis.py Code        #
#                         #
# Pietro Giampa, Jan 2022 #
###########################

## Libraries
import numpy as np
import yagmail
import matplotlib.pyplot as plt
import pandas as pd
import TrendPlotting as tp
import Variables as currency
import GetCurrency as gc

# Send Email with Reports
# Need to specify sending email and password, receiver, body and filename
# -----
# user - String
# psw - String
# receiver - String
# body - String
# filename - String
def send_email(user, psw, receiver, body, filename):
    yag = yagmail.SMTP(user,psw)
    yag.send(
        to=receiver,
        subject="Daily Crypto Investment Report",
        contents=body, 
        attachments=filename,
    )
    print('successfully sent the mail')

filename='Reports/Dogecoin_29_1_2022.png'
send_email('giampapietro@gmail.com','qtbhvvwurtedunqb','danikaadam@gmail.com','Daily Crypto Investment Report',filename)
