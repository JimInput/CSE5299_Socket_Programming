# I started with the basic lecture slide code for UDP

from socket import *
from TCP_basic_client import send_request, decode_response

def main():
    serverName = 'localhost'    # hosting server on same machine
    serverPort = 12000          # arbitrary unassigned port number
    MAX_BYTES = 60000           # UDP is limited to 2^16 bytes so we have to limit the max number of bytes

    clientSocket = socket(AF_INET, SOCK_DGRAM) # create UDP socket

    query = input('Input Query: ') # accept pattern from user

    request = send_request(query)   # convert user query to SEND request
    clientSocket.sendto(request.encode(), (serverName, serverPort))     # send request to server

    raw_response, _ = clientSocket.recvfrom(MAX_BYTES)  # receive raw data from server
    _, status, N, words = decode_response(raw_response.decode())     # parse response protocol message into data

    # we need to handle the limited size of UDP datagrams because unlike TCP we can't return all the words in one UDP message
    num_words = len(words.split(","))
    total_words = int(N)

    print(f"Number of words found: {N}")
    if status == "200 OK": # if OK and too many words, we just return the list of words and ... N more matches...
        if total_words > num_words:
            print(f"Words: {words}...and {total_words-num_words} more matches...")
        else:
            print(f"Words: {words}")
    if status == "404 NOT FOUND":
        print(f"No words were found which matched the given pattern.")
    clientSocket.close()

if __name__ == '__main__':
    main()