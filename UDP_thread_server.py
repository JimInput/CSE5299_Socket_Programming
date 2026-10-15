"""
Server side: open a socket on a port, listen for a message from a client,
and send an echo reply; echoes lines until eof when client closes socket;
spawns a thread to handle each client connection; threads share global
memory space with main thread; this is more portable than fork: threads
work on standard Windows systems, but process forks do not;
"""

from UDP_basic_server import decode_request, find_words, encode_response, get_word_list
import time, _thread as thread           # or use threading.Thread().start()
from socket import *                     # get socket constructor and constants
myHost = "localhost"                              # server machine, '' means local host
myPort = 12000                           # listen on a non-reserved port number

sockobj = socket(AF_INET, SOCK_DGRAM)           # make a TCP socket object
sockobj.bind((myHost, myPort))                   # bind it to server port number
sockobj.settimeout(0.5)             ### set a reasonable timeout ### <--- ADDED

queue_lock = thread.allocate_lock()
dgram_queue = []
N_THREADS = 4

WORD_LIST = get_word_list("wordlist.txt") ### get word list ### <--- ADDED

def now():
    return time.ctime(time.time())               # current time on the server

def handleClient(sock, thread_idx):      # in spawned thread: reply
    while True: 
        with queue_lock:
            if len(dgram_queue) == 0:
                time.sleep(0.1) # Sleep a reasonable amount of time
                continue
            message, clientAddress = dgram_queue.pop()    # grab dgram to respond to from queue
            print(f"Thread {thread_idx} received DGRAM from {clientAddress[0]}:{clientAddress[1]}.")
        ### THIS IS WHAT I MODIFIED (BASICALLY COPYING MY CODE FROM basic_server.py) ###
        pattern = decode_request(message.decode())                   # extract string pattern from request format.
        matching_words = find_words(WORD_LIST, pattern)     # get all words which match the requested format.
        response = encode_response(matching_words, 50)
        sock.sendto(response.encode(), clientAddress) # format data back into protocol and send to client.
        print(f"Thread {thread_idx} sent response DGRAM to {clientAddress[0]}:{clientAddress[1]}.")
        ### THIS IS WHAT I MODIFIED (BASICALLY COPYING MY CODE FROM basic_server.py) ###


def dispatcher():                                # listen until process killed
    ### I ALSO EDITED THIS SECTION, TO ALLOW FOR KEYBOARD INTERRUPT ###

    # Start by spinning up 4 independent threads to respond to users.
    for i in range(N_THREADS):
        thread.start_new_thread(handleClient, (sockobj, i))
    try:
        print("Server ready to receive connections.")
        print('Press CTRL+C to stop server.')
        while True:                                  # wait for next connection,
            try:
                message, clientAddress = sockobj.recvfrom(1024)
                print(f"Server recieved DGRAM from {clientAddress[0]}:{clientAddress[1]} at {now()}")
                with queue_lock:
                    dgram_queue.append((message, clientAddress))
            except TimeoutError:
                    continue
    except KeyboardInterrupt:
        print("Server Shutting Down...")
    ### I ALSO EDITED THIS SECTION, TO ALLOW FOR KEYBOARD INTERRUPT ###

dispatcher()
sockobj.close()
