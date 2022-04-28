import socket
import random

HOST = '127.0.0.1'  # The server's hostname or IP address
BOBPORT = 12345        # The port used by the server
SERVERPORT = 12346



print("Bob is online.")

#Establish socket connection to server

try:
    bobSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bobSocket.connect((HOST, BOBPORT))
except:
    print("Failed to connect to server")
    quit()



paymentTokensCreated = []
paymentTokensRefunded = []

while(True):

    generatingRandomPaymentToken = True

    randomPaymentToken = random.randint(-999999,999999)


    #We make sure we don't generate duplicate payment tokens.
    while(generatingRandomPaymentToken):
        if(randomPaymentToken not in paymentTokensCreated):
            paymentTokensCreated.append(randomPaymentToken)
            print 
            generatingRandomPaymentToken = False
        else:
            randomPaymentToken = random.randint(-999999,999999)

    randomPaymentTokenString = "PaymentData " + str(randomPaymentToken)

    print("Generated random payment token of " + randomPaymentTokenString)

    print("Please input subject line for email.")

    subjectLineString = input()

    print("Please input message text for email.")

    messageString = input()


    print("Message consists of subject " + subjectLineString + ", with content " + messageString + ", and payment token " + randomPaymentTokenString)

   



    subjectLine = bytes(subjectLineString,"utf8")
    paymentInfo = bytes(randomPaymentTokenString,"utf8")
    emailMessageContent = bytes(messageString,"utf8")

    emailMessageBytes = subjectLine + b"\0" + paymentInfo + b"\0" + emailMessageContent


    print("Sending message to server.")

    try:
        bobSocket.sendall(emailMessageBytes)
    except:
        print("Failed to send email to server.")

    #Receive email bytes from server
    try:
        aliceResponseEmail = bobSocket.recv(1024)
    except:
        print("Failed to receive response message from Server.")
        quit()


    aliceResponseEmailData = aliceResponseEmail.split(b"\0")

    aliceResponseEmailDataString = aliceResponseEmail.decode("utf8")

    aliceResponseEmailComponents = aliceResponseEmailDataString.split()


    if(aliceResponseEmailComponents[0] == "Refunding"):

        refundedPaymentString = aliceResponseEmailData[1].decode("utf8")
        paymentTokensRefunded.append(refundedPaymentString) #Log that the payment was refunded.

        print("Payment " + refundedPaymentString + " was refunded!")

    elif(aliceResponseEmailComponents[0] == "Rejected"):

        rejectedPaymentString = aliceResponseEmailData[1].decode("utf8")

        print("Payment " + rejectedPaymentString + " was not refunded.")

    else:
        print("Failed to pay properly!")


    