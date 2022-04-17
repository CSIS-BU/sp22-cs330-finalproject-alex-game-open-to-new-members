###############################################################################
# hangman-client-python.py
###############################################################################

import sys
import socket
import random
import string

# Size of chunks the client sends messages to the server with
RECV_BUFFER_SIZE = 2048
SEND_BUFFER_SIZE = 2048
# client(): Open socket and send message from sys.stdin

def client(server_ip, server_port):

    # Opens a socket and sets the socket mode to IPV4 and TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        # Connects to the server using the ip and port the user specified
        sock.connect((server_ip, server_port))

        # WHile a connection is open send all of the data rom the input stream to the server in chunks the size of SEND_BUFFER_SIZE
        with open(0,'rb'):
            while True:
                msg = sys.stdin.buffer.raw.read(SEND_BUFFER_SIZE)
                sendmsg = sock.sendall(msg)
                
                data = sock.recv(RECV_BUFFER_SIZE)
                sys.stdout.buffer.raw.write(data)
            sys.stdout.flush()


def main():
    """Parse command-line arguments and call client function """
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 client-python.py [Server IP] [Server Port] < [message]")
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    client(server_ip, server_port)

# reads in data from the server
def receive(socket):
    value1 = int(socket.recv(1)[0])
    if value1 == 0:
        x, y = socket.recv(2)
        return 0, socket.recv(int(x)), socket.recv(int(y))
    else:
        return 1, socket.recv(value1)
 
# Game will take in and send user input; will also check if the guesses are valid
def playHangman(s):
    while True:
        pkt = receive(s)
        messageFlag = pkt[0]
        if messageFlag != 0:
            message = pkt[1].decode('utf8')
            print(message)
        else:
            chosenWord = pkt[1].decode('utf8')
            incorrectGuesses = pkt[2].decode('utf8')
            

if __name__ == "__main__":
    main()
