# This is the template code which I modified

from TCP_basic_server import decode_request, find_words, encode_response, get_word_list
import time, _thread as thread           
from socket import *                     
                    
serverPort = 12000                           

serverSocket = socket(AF_INET, SOCK_STREAM)             # make a TCP socket object
serverSocket.bind(('', serverPort))                     # bind it to server port number
serverSocket.listen(5)                                  # allow up to 5 pending connects
serverSocket.settimeout(0.5)                            # A reasonable amount of time to wait to allow for KeyboardInterrupt

WORD_LIST = get_word_list("wordlist.txt")               # split text file into an array of strings.

def now():
    return time.ctime(time.time())                      # current time on the server

def handleClient(connection):                    # in spawned thread: reply
    while True:                                  # read, write a client socket
        request = connection.recv(1024).decode()
        if not request: break
        
        pattern = decode_request(request)                   # extract string pattern from request format.
        matching_words = find_words(WORD_LIST, pattern)     # get all words which match the requested format.
        response = encode_response(matching_words)          # convert word list to protocol esponse
                
        connection.send(response.encode())                  # return protocol response to client
        
    connection.close()

def dispatcher():                                # listen until process killed
    try:
        print("Server ready to receive connections.")
        print('Press CTRL+C to stop server.')
        while True:                                  # wait for next connection,
            try:
                connection, address = serverSocket.accept()   # pass to thread for service
                print('Server connected by', address, end=' ')
                print('at', now())
                thread.start_new_thread(handleClient, (connection,))    # start thread passing in the TCP connection
            except TimeoutError:
                    continue
    except KeyboardInterrupt:
        print("Server Shutting Down...")

dispatcher()
serverSocket.close()
