"""
Server side: open a socket on a port, listen for a message from a client,
and send an echo reply; echoes lines until eof when client closes socket;
spawns a thread to handle each client connection; threads share global
memory space with main thread; this is more portable than fork: threads
work on standard Windows systems, but process forks do not;
"""

from TCP_basic_server import decode_request, find_words, encode_response, get_word_list
import time, _thread as thread           # or use threading.Thread().start()
from socket import *                     # get socket constructor and constants
myHost = "localhost"                              # server machine, '' means local host
myPort = 12000                           # listen on a non-reserved port number

sockobj = socket(AF_INET, SOCK_STREAM)           # make a TCP socket object
sockobj.bind((myHost, myPort))                   # bind it to server port number
sockobj.listen(5)                                # allow up to 5 pending connects
sockobj.settimeout(0.5)             ### set a reasonable timeout ### <--- ADDED

WORD_LIST = get_word_list("wordlist.txt") ### get word list ### <--- ADDED

def now():
    return time.ctime(time.time())               # current time on the server

def handleClient(connection):                    # in spawned thread: reply
    while True:                                  # read, write a client socket
        request = connection.recv(1024).decode()
        if not request: break
        ### THIS IS WHAT I MODIFIED (BASICALLY COPYING MY CODE FROM basic_server.py) ###
        pattern = decode_request(request)                   # extract string pattern from request format.
        matching_words = find_words(WORD_LIST, pattern)     # get all words which match the requested format.
                
        connection.send(encode_response(matching_words).encode()) # format data back into protocol and send to client.
        ### THIS IS WHAT I MODIFIED (BASICALLY COPYING MY CODE FROM basic_server.py) ###
    connection.close()

def dispatcher():                                # listen until process killed
    ### I ALSO EDITED THIS SECTION, TO ALLOW FOR KEYBOARD INTERRUPT ###
    try:
        print("Server ready to receive connections.")
        print('Press CTRL+C to stop server.')
        while True:                                  # wait for next connection,
            try:
                connection, address = sockobj.accept()   # pass to thread for service
                print('Server connected by', address, end=' ')
                print('at', now())
                thread.start_new_thread(handleClient, (connection,))
            except TimeoutError:
                    continue
    except KeyboardInterrupt:
        print("Server Shutting Down...")
    ### I ALSO EDITED THIS SECTION, TO ALLOW FOR KEYBOARD INTERRUPT ###

dispatcher()
sockobj.close()
