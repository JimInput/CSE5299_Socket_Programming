from socket import *
from TCP_basic_client import send_request, decode_response

# This file is named thread_client but it doesn't use threads itself. It just allows a user to send multiple queries in one process.

def main():
    serverName = 'localhost'    # hosting server on same machine
    serverPort = 12000          # arbitrary unassigned port number
    MAX_BYTES = 700000          # the given text file is 651 KB so 700 KB is reasonable as an upper bound for the size of the TCP message

    clientSocket = socket(AF_INET, SOCK_STREAM)         # create TCP socket
    clientSocket.connect((serverName, serverPort))      # connect to server socket
    
    while True: # query loop to continue querying user until they choose to quit
        query = input('Input Query: ') # accept pattern from user
        if query == "quit":
            break

        request = send_request(query)           # convert user query to SEND request
        clientSocket.send(request.encode())     # send request to server

        response = clientSocket.recv(MAX_BYTES).decode()    # receive all bytes from server
        _, status, N, words = decode_response(response)     # parse response protocol message into data

        print(f"Number of words found: {N}")    # always print number of words found
        if status == "200 OK":                  # if response is OK print list of words
            print(f"Words: {words}")            
        if status == "404 NOT FOUND":           # if response NOT FOUND print no words found
            print(f"No words were found which matched the given pattern.")
    clientSocket.close()

if __name__ == '__main__':
    main()