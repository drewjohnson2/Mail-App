#! /usr/bin/python3
#-------------------------------------------------------------------------
#Author: Drew Johnson							 #
#Email: drew.m.johnson2@gmail.com					 #
#									 #
#									 #
#This script retrieves a users emails from their accout, parses when	 #
#necessary, formats, and then displays unread emails for the user	 #
#to view.								 #
#									 #
#									 #
#Script is run by typing 'getmail' into a terminal window.		 #
#									 #
#-------------------------------------------------------------------------
import imapclient, pyzmail, getpass, sys, os, bs4


def createFile(htmlString):
	
	#Creates HTML file for storing HTML until time for parsing..
	htmlFile = open('hold.html', 'a')
	htmlFile.write(htmlString)
	htmlFile.close()

def printFile():
	
	f = open('hold.html')
	parsedHTML = bs4.BeautifulSoup(f, 'html5lib')


	#removes all scrpit and style tags
	for script in parsedHTML(["script", "style" ]):
		script.extract()

	cleanText = parsedHTML.get_text()

	#breaks into lines, removes excess whitespace
	lines = (line.strip() for line in cleanText.splitlines())

	#Break mult-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split(" "))

	#Removes blank lines
	cleanText = ' '.join(chunk for chunk in chunks if chunk)

	print(cleanText)
	f.close()

def deleteFile():
	
	#File used for holding the parsed email is deleted
	os.remove('hold.html')


try:
	#Get password
	password = getpass.getpass()
	#Creates IMAP object, passes in provider and SSL encryption
	imapObj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
	imapObj.login('drew.m.johnson2@gmail.com', password)

except Exception:
	print("Password incorrect")
	sys.exit()


imapObj.select_folder('INBOX', readonly=False)  #Selects folder to check for mail.
						#'readonly' set to false so emails
						#will be marked as read after fetching.

UIDs = imapObj.search(['UNSEEN'])		#Fetches unread emails	

if len(UIDs) == 0:
	print("No new mail.")
	sys.exit()

print('-----------------------------------------------------------------')
for i in UIDs:
	try:	
		rawMessages = imapObj.fetch(i, ['BODY[]', 'FLAGS'])
		
		#Selects current email UID
		message = pyzmail.PyzMessage.factory(rawMessages[i][b'BODY[]'])
		
		print('Subject: ')
		print(message.get_subject())		#Retrieves message subject
	
		print()
		print('From: ')
		sender = message.get_addresses('from')  #Retrieves sender
		
		for y in sender:
			print(y)

		print()
		print('Body: ')
		message.text_part != None

		#Get plain text from body
		
		createFile(message.text_part.get_payload().decode(message.text_part.charset))
		printFile()
		deleteFile()
		print()
			
		print('----------------------------------------------------------------')
	
	except Exception as err:
		print('Cannot display email', err)			
		print('----------------------------------------------------------------')
imapObj.logout()



