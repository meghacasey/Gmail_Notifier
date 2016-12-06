import RPi.GPIO as GPIO
import imaplib,email
from os import sys
import time
import getpass

#Initialise GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)       #Activate two pins as ‘input’ for buttons
GPIO.setup(11,GPIO.OUT)       #Resetter Button

#Ask username and password from user
username = raw_input(“Enter your Gmail username :”)
passwrd = getpass.getpass(“Enter your password : ”)

m = imaplib.IMAP4_SSL(“imap.gmail.com”)

#Login with username and password
try:
 m.login(username,passwrd)
 print “Login Successful”

except imaplib.IMAP4.error:
 print “Login Failed”
 m.logout()
 sys.exit()


res,list1=m.select(“INBOX”)
res, items1 = m.search(None, “ALL”)
item1 = items1[0].split()
n=len(item1)

print “Checking Mail …… ”


while True:                                 #Constantly checks whether a new mail arrives
  res,list=m.select(“INBOX”)
  resp, items = m.search(None, “ALL”)
  item = items[0].split()
  n_new=len(item)
  reset=0
  if n_new>n:
      print “\n”
      print “New Mail”
      print “———–”
      resp, data = m.fetch(n_new, “(RFC822)”)
      msg = email.message_from_string(data[0][1])
      typ, data = m.store(n_new,’-FLAGS’,’\Seen’)
 
      for header in [ 'subject’, 'from’ ]:
                  print ’%-8s: %s’ % (header.upper(), msg[header])
      print “\n”
      print “Press the Blue Button to Display the Message…….”
      print “Press the Red Button to reset the Message…….”

      while reset!=1:
         GPIO.output(13,GPIO.HIGH)
         GPIO.output(15,GPIO.HIGH)
         time.sleep(0.2)
         GPIO.output(13,GPIO.LOW)
         GPIO.output(15,GPIO.LOW)
         time.sleep(0.2)
         inputval_blue=GPIO.input(12)
         inputval_red=GPIO.input(11)

         if inputval_blue==True:
              print “\n”
              print “*************”
              for header in [ 'subject’, 'from’ ]:
                  print ’%-8s: %s’ % (header.upper(), msg[header])
              print “CONTENT : ”
              for part in msg.walk():
                 if part.get_content_type() == 'text/plain’:
                    print part.get_payload()
              reset=1
         if inputval_red==True:
              reset=1
              print “\nMessage Resetted”

      n=n_new
  time.sleep(0.01)

