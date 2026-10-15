from socket import *

# THIS FILE IS NAMED THREAD-CLIENT BUT IT DOESN'T USE THREADS

def main():
    serverName = 'localhost'
    serverPort = 12000
    MAX_BYTES = 700000 # the given text file is 651 KB so 700 KB is reasonable as an upper bound for the size of the buffer needed.

    clientSocket = socket(AF_INET, SOCK_DGRAM) # create and connect client socket to server socket.
    
    while True: # query loop to continue querying user until they choose to quit
        query = input('Input Query: ') # accept pattern from user
        if query == "quit":
            break

        clientSocket.sendto(send_request(query).encode(), (serverName, serverPort))     # convert user pattern to application protocol send request

        raw_response, _ = clientSocket.recvfrom(MAX_BYTES)  # receive all bytes from server
        _, status, N, words = decode_response(raw_response.decode())     # parse response protocol message into data
        num_words = len(words.split(","))
        total_words = int(N)

        print(f"Number of words found: {N}")
        if status == "200 OK":
            if total_words > num_words:
                print(f"Words: {words}...and {total_words-num_words} more matches...")
            else:
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