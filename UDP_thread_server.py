from TCP_basic_server import decode_request, find_words, get_word_list
from UDP_basic_server import encode_response
import time, _thread as thread        
from socket import *                  
                 
serverPort = 12000                           

serverSocket = socket(AF_INET, SOCK_DGRAM)               # make a UDP socket object
serverSocket.bind(('', serverPort))                      # bind it to server port number
serverSocket.settimeout(0.5)                             # A reasonable amount of time to wait for KeyboardInterrupt

queue_lock = thread.allocate_lock() # mutex lock to handle race condition
dgram_queue = []    # queue that updates as datagram requests come in
N_THREADS = 4   # max number of threads

WORD_LIST = get_word_list("wordlist.txt") # split text file into an array of strings.

def now():
    return time.ctime(time.time())               # current time on the server

def handleClient(thread_idx): # a thread checks the queue, and as the queue fills up responds to each request
    while True: 
        with queue_lock:
            if len(dgram_queue) == 0:   # if the queue is empty sleep to not use 100% of CPU
                time.sleep(0.1) # Sleep a reasonable amount of time
                continue
            if dgram_queue[-1] == 'DONE':
                break
            message, clientAddress = dgram_queue.pop()    # grab dgram to respond to from queue
        
        print(f"Thread {thread_idx} received DGRAM from {clientAddress[0]}:{clientAddress[1]}.")

        request = message.decode()
        pattern = decode_request(request)                   # extract string pattern from request format.
        matching_words = find_words(WORD_LIST, pattern)     # get all words which match the requested format.
        response = encode_response(matching_words, 50)      # encode response, getting back up to 50 words.
        serverSocket.sendto(response.encode(), clientAddress)       # send response back to client
        print(f"Thread {thread_idx} sent response DGRAM to {clientAddress[0]}:{clientAddress[1]}.")


def dispatcher():
    # Start by spinning up 4 independent threads to respond to users.
    for i in range(N_THREADS):
        thread.start_new_thread(handleClient, (i,)) # each thread gets an index (for printing purposes)
    try:
        print("Server ready to receive connections.")
        print('Press CTRL+C to stop server.')
        while True:
            try:
                message, clientAddress = serverSocket.recvfrom(1024) # wait for a request datagram
                print(f"Server recieved DGRAM from {clientAddress[0]}:{clientAddress[1]} at {now()}")
                with queue_lock: # add request to queue, and next available thread will handle it
                    dgram_queue.append((message, clientAddress))
            except TimeoutError:
                    continue
    except KeyboardInterrupt:
        print("Server Shutting Down...")

dispatcher()
dgram_queue.append("DONE")
serverSocket.close()
