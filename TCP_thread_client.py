from socket import *

# THIS FILE IS NAMED THREAD-CLIENT BUT IT DOESN'T USE THREADS

def main():
    serverName = 'localhost'
    serverPort = 12000
    MAX_BYTES = 700000 # the given text file is 651 KB so 700 KB is reasonable as an upper bound for the size of the buffer needed.

    clientSocket = socket(AF_INET, SOCK_STREAM) # create and connect client socket to server socket.
    clientSocket.connect((serverName, serverPort))
    while True: # query loop to continue querying user until they choose to quit
        query = input('Input Query: ') # accept pattern from user
        if query == "quit":
            break

        clientSocket.send(send_request(query).encode())     # convert user pattern to application protocol send request

        response = clientSocket.recv(MAX_BYTES).decode()    # receive all bytes from server
        _, status, N, words = decode_response(response)     # parse response protocol message into data

        print(f"Number of words found: {N}")
        if status == "200 OK":
            print(f"Words: {words}")
        if status == "404 NOT FOUND":
            print(f"No words were found which matched the given pattern.")
    clientSocket.close()

def send_request(query):
    """Takes a pattern query and formats it into a request protocol message."""
    return f"SEND PMWS/1.0\n{query}\n" # 2 segments, request header and the body (with query data)

def decode_response(resp):
    """Takes a response protocol format and converts it into the respective data fields, protocol_name, status, N_words, and word_list."""
    segments = resp.split("\n")
    protocol = segments[0][:8]
    status = segments[0][9:]
    N = segments[1][8:]
    words = segments[2]
    return protocol, status, N, words



if __name__ == '__main__':
    main()