# I referenced the socket programming slides heavily when working on this assignment.

# fnmatch code from https://docs.python.org/3/library/fnmatch.html

from socket import *
from fnmatch import fnmatch

def main():
    serverPort = 12000 # Using a unused large port number.

    serverSocket = socket(AF_INET, SOCK_STREAM) # create TCP server socket.
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)

    serverSocket.settimeout(0.5) # A reasonable amount of time to wait (breaking the blocking of .accept() so that the program can stop with KeyboardInterrupt).

    WORD_LIST = get_word_list("wordlist.txt") # split text file into an array of strings.

    print('The server is ready to accept connections.')

    try:
        while True:
            try:
                connectionSocket, addr = serverSocket.accept()
            
                print(f"Connection @ {addr[0]}:{addr[1]} opened.")

                request = connectionSocket.recv(1024).decode()      # get request formatted string.
                pattern = decode_request(request)                   # extract string pattern from request format.
                matching_words = find_words(WORD_LIST, pattern)     # get all words which match the requested format.
                
                connectionSocket.send(encode_response(matching_words).encode()) # format data back into protocol and send to client.

                connectionSocket.close()

                print(f"Connection @ {addr[0]}:{addr[1]} closed.")
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

def encode_response(words): # 3 segments, a status header, (404 Not found or 200 OK), NWORDS, and the text body (word data).
    """Take array of words and format into response message. Formatted as PWMS/1.0 STATUS NL NWORDS: N NL WORD_LIST"""
    N = len(words)
    status_header = f"PMWS/1.0 {"404 NOT FOUND" if N == 0 else "200 OK"}"    
    return f"{status_header}\nNWORDS: {N}\n{','.join(words)}\n"

if __name__=='__main__':
    main()