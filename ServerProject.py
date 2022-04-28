import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
BOBPORT = 12345        # The port used by the server
SERVERPORT = 12346
ALICEPORT = 12347

print("Server is online.")

#Establish socket connection to Alice

try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((HOST, SERVERPORT))
    serverSocket.listen()
    conn,addr = serverSocket.accept()
except:
    print("Failed to connect to Alice")
    quit()



try:
    bobSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bobSocket.bind((HOST, BOBPORT))
    bobSocket.listen()
    conn,addr = serverSocket.accept()
except:
    print("Failed to connect to Bob")
    quit()

messagesReceived = {

}

paymentTokensReceived = []

paymentTokensRefunded = []

while True:
    print("Waiting for messages...")


    #Receive email bytes from server
    try:
        email = bobSocket.recv(1024)
    except:
        print("Failed to receive data from Bob.")
        quit()


    emailStrings = email.split(b"\0")

    subjectLine = emailStrings[0]
    paymentInfo = emailStrings[1]
    emailMessage = emailStrings[2]

    paymentInfoString = str(paymentInfo)

    paymentInfoComponents = paymentInfoString.split()

    if(paymentInfoString[0] == "PaymentData"):

        #paymentsReceived.append(paymentInfoComponents[1])

        messagesReceived[paymentInfoComponents[1]] = email #Every email that is paid for is logged, using the payment token as the key.

        paymentTokensReceived.append(paymentInfoString[1])

        try:
            serverSocket.sendall(email)
        except:
            print("Failed to forward email to Alice.")
            quit()

        try:
            aliceResponseEmail = serverSocket.recv(1024)
        except:
            print("Failed to receive response from Alice.")
            quit()

        aliceResponseEmailData = aliceResponseEmail.split(b"\0")

        if(str(aliceResponseEmailData[0]) == "Refund"):

            refundedPaymentString = str(aliceResponseEmailData[1])
            paymentTokensRefunded.append(refundedPaymentString) #Log that the payment was refunded.

            refundMessage = bytes("Refunding payment ","utf8") + b"\0" + bytes(refundedPaymentString,"utf8")

            try:
                bobSocket.sendall(refundMessage)
            except:
                print("Failed to send refund message to Bob.")


        elif(str(aliceResponseEmailData[0]) == "Reject"):

            #rejectMessage = "Message rejected. The following payment will not be refunded:" + "\0" + str(aliceResponseEmail[1])

            #rejectMessageText = "Message rejected. Payment " + str(aliceResponseEmailData[1]) + " will not be refunded."
            rejectMessage = bytes("Message rejected. The following payment will not be refunded: ","utf8") + b"\0" + bytes(refundedPaymentString,"utf8")

            try:
                bobSocket.sendall(bytes(rejectMessage),"utf8")
            except:
                print("Failed to send rejection message to Bob.")






