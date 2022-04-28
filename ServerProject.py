import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
BOBPORT = 12345        # The port used by the server
SERVERPORT = 12346
#ALICEPORT = 12347

print("Server is online.")

#Establish socket connection to Alice

try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((HOST, SERVERPORT))
    serverSocket.listen()
    aliceConn,aliceAddr = serverSocket.accept()
except:
    print("Failed to connect to Alice")
    quit()

print("Connected to Alice.")

try:
    bobSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bobSocket.bind((HOST, BOBPORT))
    bobSocket.listen()
    bobConn,bobAddr = bobSocket.accept()
except:
    print("Failed to connect to Bob")
    quit()


print("Connected to Bob.")

messagesReceived = {

}

paymentTokensReceived = []

paymentTokensRefunded = []

while True:
    print("Waiting for messages...")


    #Receive email bytes from server
    #try:
    email = bobConn.recv(1024)
    #except:
    #    print("Failed to receive data from Bob.")
    #    quit()


    emailStrings = email.split(b"\0")

    subjectLine = emailStrings[0]
    paymentInfo = emailStrings[1]
    emailMessage = emailStrings[2]

    #print(paymentInfo)

    paymentInfoString = paymentInfo.decode("utf8")

    #print(paymentInfoString)

    paymentInfoComponents = paymentInfoString.split()

    print("Payment data shown below:")
    print(paymentInfoComponents[1])

    if(paymentInfoComponents[0] == "PaymentData"):

        #paymentsReceived.append(paymentInfoComponents[1])

        messagesReceived[paymentInfoComponents[1]] = email #Every email that is paid for is logged, using the payment token as the key.

        paymentTokensReceived.append(paymentInfoComponents[1])

        try:
            aliceConn.sendall(email)
        except:
            print("Failed to forward email to Alice.")
            quit()

        try:
            aliceResponseEmail = aliceConn.recv(1024)
        except:
            print("Failed to receive response from Alice.")
            quit()

        aliceResponseEmailData = aliceResponseEmail.split(b"\0")

        if(aliceResponseEmailData[0].decode("utf8") == "Refund"):

            refundedPaymentString = aliceResponseEmailData[1].decode("utf8")
            paymentTokensRefunded.append(refundedPaymentString) #Log that the payment was refunded.

            refundMessage = bytes("Refunding ","utf8") + b"\0" + bytes(refundedPaymentString,"utf8")

            try:
                bobConn.sendall(refundMessage)
            except:
                print("Failed to send refund message to Bob.")


        elif(aliceResponseEmailData[0].decode("utf8") == "Reject"):

            #rejectMessage = "Message rejected. The following payment will not be refunded:" + "\0" + str(aliceResponseEmail[1])

            rejectedPaymentString = aliceResponseEmailData[1].decode("utf8")

            #rejectMessageText = "Message rejected. Payment " + str(aliceResponseEmailData[1]) + " will not be refunded."
            rejectMessage = bytes("Rejected ","utf8") + b"\0" + bytes(rejectedPaymentString,"utf8")

            try:
                bobConn.sendall(rejectMessage)
            except:
                print("Failed to send rejection message to Bob.")


    else:
        print("No payment was received!")
        failureToPayString = "Error: your message did not include payment data."

        failureToPayStringBytes = bytes(failureToPayString,"utf8")

        bobConn.sendall(failureToPayStringBytes)



