# I referenced the UDP socket programming lecture slides.

# fnmatch code from https://docs.python.org/3/library/fnmatch.html

from socket import *
from fnmatch import fnmatch

def main():
    serverPort = 12000 # Using a unused large port number.

    serverSocket = socket(AF_INET, SOCK_DGRAM) # create UDP server socket.
    serverSocket.bind(('', serverPort))

    serverSocket.settimeout(0.5) # A reasonable amount of time to wait (breaking the blocking of .recvfrom() so that the program can stop with KeyboardInterrupt).

    WORD_LIST = get_word_list("wordlist.txt") # split text file into an array of strings.

    print('The server is ready to accept connections.')
    print('Press CTRL+C to stop server.')

    try:
        while True:
            try:
                message, clientAddress = serverSocket.recvfrom(1024)
            
                print(f"Datagram from {clientAddress[0]}:{clientAddress[1]} received.")

                request = message.decode()      # get request formatted string.
                pattern = decode_request(request)                   # extract string pattern from request format.
                matching_words = find_words(WORD_LIST, pattern)     # get all words which match the requested format.
                # We limit the number of matching_words to 50 since datagrams are limited in size.
                response = encode_response(matching_words, 50)
                serverSocket.sendto(response.encode(), clientAddress) # format data back into protocol and send to client.

                print(f"Datagram sent to {clientAddress[0]}:{clientAddress[1]}")
            except TimeoutError:
                continue

    except KeyboardInterrupt:
        print("Server Shutting Down...")

    serverSocket.close()

def get_word_list(filename):
    with open(filename, 'r') as f: 
        return f.read().splitlines() # split text file into an array of strings.

def find_words(WORD_LIST, pattern): 
    """Uses regex pattern matching to pattern match with all of the words in WORD_LIST."""
    return [word for word in WORD_LIST if fnmatch(word, f"*{pattern}*")] 

def decode_request(req):
    """Parses a request formatted as PWMS/1.0 NL pattern NL"""
    segments = req.split("\n")
    return segments[1] # The segment containing the query

def encode_response(words, max_words=None): # 3 segments, a status header, (404 Not found or 200 OK), NWORDS, and the text body (word data).
    """Take array of words and format into response message. Formatted as PWMS/1.0 STATUS NL NWORDS: N NL WORD_LIST"""
    N = len(words)
    status_header = f"PMWS/1.0 {"404 NOT FOUND" if N == 0 else "200 OK"}"    
    if max_words: # I modify this section for UDP to limit the number of words
        return f"{status_header}\nNWORDS: {N}\n{','.join(words[:min(N, max_words)])}\n"
    else:
        return f"{status_header}\nNWORDS: {N}\n{','.join(words)}\n"

if __name__=='__main__':
    main()