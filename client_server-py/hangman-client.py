###############################################################################
# client-python.py
# Name: Alex Hoerr
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

    hangmanSegments = 0
    guessedCharacters = []
    currentWord = ''
    playerNum = 0

    # Opens a socket and sets the socket mode to IPV4 and TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        # Connects to the server using the ip and port the user specified
        sock.connect((server_ip, server_port))

        # WHile a connection is open send all of the data rom the input stream to the server in chunks the size of SEND_BUFFER_SIZE
        with open(0,'rb'):
            while True:
                data = sock.recv(RECV_BUFFER_SIZE)
                sys.stdout.buffer.raw.write(data)
                strData = data.decode('utf-8')
                parsedData = strData.split(',')
                if parsedData[0] == '!':
                    print("parsedData:",parsedData)
                    # Parse segments
                    #start = s.find("segments:") + len("segments:")
                    #end = s.find("|UGA")
                    #substring = s[start:end]
                    #hangmanSegments = int(substring)
                    #print("segments:",)

                if(data.decode('utf8') == 'Please chose a letter to guess: ' or data.decode('utf8') == 'Please chose the Word to guess: '):
                    msg = sys.stdin.buffer.raw.read(SEND_BUFFER_SIZE)
                    sendmsg = sock.sendall(msg)
            sys.stdout.flush()

def displaySegments(hangmanSegments):
    states = [  # 0: last state (GAME OVER!)
                """
                    +------+
                   |      |
                   |      O
                   |     /|\ 
                   |     / \ 
                   |     
                   +------
                """,
                # 1: head, body, both arms & 1 leg
                """
                   +------+
                   |      |
                   |      O
                   |     /|\ 
                   |     /
                   |     
                   +------
                """,
                # 2: head, body, & both arms
                """
                   +------+
                   |      |
                   |      O
                   |     /|\ 
                   |      
                   |     
                   +------
                """,
                # 3: head, body & 1 arm
                """
                   +------+
                   |      |
                   |      O
                   |     /|
                   |      
                   |     
                   +------
                """,
                # 4: head & body
                """
                   +------+
                   |      |
                   |      O
                   |      |
                   |      
                   |     
                   +------
                """,
                # 5: head
                """
                   +------+
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   +------
                """,
                # 6: initial state (empty)
                """
                   +------+
                   |      |
                   |      
                   |    
                   |      
                   |     
                   +------
                """
    ]
    return states[hangmanSegments]
def main():
    """Parse command-line arguments and call client function """
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 client-python.py [Server IP] [Server Port] < [message]")
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    client(server_ip, server_port)

if __name__ == "__main__":
    main()
