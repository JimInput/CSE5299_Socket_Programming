# I started with the basic lecture slide code for TCP
# I named my protocol Pattern Matching Word Search (PMWS/1.0)

from socket import *

def main():
    serverName = 'localhost'    # hosting server on same machine
    serverPort = 12000          # arbitrary unassigned port number
    MAX_BYTES = 700000          # the given text file is 651 KB so 700 KB is reasonable as an upper bound for the size of the TCP message

    clientSocket = socket(AF_INET, SOCK_STREAM)     # create TCP socket
    clientSocket.connect((serverName, serverPort))  # connect to server socket

    query = input('Input Query: ') # accept user input pattern
    
    request = send_request(query)           # convert user query to SEND request
    clientSocket.send(request.encode())     # send request to server

    response = clientSocket.recv(MAX_BYTES).decode()    # receive the response protocol message
    _, status, N, words = decode_response(response)     # parse response protocol message

    print(f"Number of words found: {N}")    # always print number of words found
    if status == "200 OK":                  # if response is OK print list of words
        print(f"Words: {words}")            
    if status == "404 NOT FOUND":           # if response NOT FOUND print no words found
        print(f"No words were found which matched the given pattern.")
    clientSocket.close()    # close socket

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
    return protocol, status, N, words # just parsing the response formatted message



if __name__ == '__main__':
    main()