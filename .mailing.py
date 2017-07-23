#! /usr/bin/python3

#-----------------------------------------------------------------
#Author: Drew Johnson						 #
#Email: Drew.m.johnson2@gmail.com				 #
#								 #
#This program takes user input from the command line and sends   #
#an email.							 #
#								 #
#								 #
#Program is called by typing "mailing" and the recipients email  #
#address as an argument.					 #
#-----------------------------------------------------------------

import smtplib
import sys

if len(sys.argv) < 2:
        print("Who do you want to email?")
        sys.exit()
        
while True:
        recipient = sys.argv[1]
        subject = input("Subject: ")
        print("Body: (CTRL + D to stop)")

        bodyLst = sys.stdin.readlines()
        body = ''.join(bodyLst)

        sendQ = input("Are you sure you want to send? (y/n): ")

        if sendQ == 'y':
                break
        else:
                continue

mail = smtplib.SMTP('smtp.gmail.com', 587)

type(mail)

mail.ehlo()

mail.starttls()

mail.login('drew.m.johnson2@gmail.com', 'Your Email')    

mail.sendmail('drew.m.johnson2@gmail.com', recipient,
        'Subject:' + subject + ' \n' + body)

mail.quit() 
