import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
#BOBPORT = 12345        # The port used by the server
SERVERPORT = 12346
ALICEPORT = 12347


print("Alice is online.")


#Establish socket connection to server

try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.connect((HOST, SERVERPORT))
except:
    print("Failed to connect to server")
    quit()

print("Connected to server.")

while(True):

    print("Waiting for messages...")


    #Receive email bytes from server
    try:
        email = serverSocket.recv(1024)
    except:
        print("Failed to receive data from Server.")
        quit()

    #kBobNb = str(kBobNb, 'utf8')

    print("Received email from Bob.")

    emailStrings = email.split(b'\0')
    subjectLine = emailStrings[0]
    paymentInfo = emailStrings[1]
    emailMessage = emailStrings[2]

    print("Subject line: " + subjectLine.decode("utf8"))

    print("Would you like to open this email? Y/N")

    emailOpenCommand = input()


    refundPayment = False

    paymentInfoString = str(paymentInfo)
    paymentInfoStringComponents = paymentInfoString.split()

    paymentToken = paymentInfoStringComponents[1]

    if(emailOpenCommand == "Y"):
        print("Opening email. Displaying message now:")
        print(emailMessage.decode("utf8"))
        refundPayment = True

    elif(emailOpenCommand == "N"):
        print("Email rejected.")

    if(refundPayment):

        
        refundMessage = bytes("Refund","utf8") + b"\0" + bytes(paymentToken,"utf8")
        

        try:
            serverSocket.sendall(refundMessage)
            print("Sent refund message to server to refund email payment.")
        except:
            print("Failed to send refund message.")
    
    else:
        rejectMessage = bytes("Reject","utf8") + b"\0" + bytes(paymentToken,"utf8")

        #rejectMessageBytes = bytes(rejectMessage, "utf8")

        try:
            serverSocket.sendall(rejectMessage)
            print("Sent message to server confirming rejection of email. Payment will not be refunded.")
        except:
            print("Failed to send rejection message.")
            
   # print("Would you like to continue receiving emails? Y/N")

    #continueText = input()
    #if(continueText == "N"):
    #    quit()


        
    