###############################################################################
# client-python.py
# Name: Alex Hoerr, Simfara
###############################################################################

import sys
import socket
import random
import string
import curses

def renderData():
    pass

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
            #Preparing to initialize screen...
            screen = curses.initscr()
            # Wipe the screen buffer and set the cursor to 0,0
            screen.clear()
            screen.nodelay(False)
            curses.noecho()
            screen.keypad(True)        
            # Update the buffer, adding text
            screen.addstr(0,0,'Lets begin the game of hangman')
            displaySegments(6)
            screen.refresh()
            while True:
                # Changes go in to the screen buffer and only get displayed after calling `refresh()` to update
                data = (sock.recv(RECV_BUFFER_SIZE))
                strData = data.decode('utf-8')
                parsedData = strData.split('|')
                
                if parsedData[0] == '!':
                    screen.clear()
                    screen.addstr(0,0,'Lets begin the game of hangman')
                    #print("parsedData:",parsedData)
                    # Parse segments
                    hangmanSegments = int(parsedData[1][-1])
                    #print("segments:",hangmanSegments)
                    #print(displaySegments(hangmanSegments))
                    screen.addstr(1,0,displaySegments(hangmanSegments))
                    
                    # Parse guessedCharacters
                    guessedCharacters = []
                    gCharString = parsedData[2][parsedData[2].find(':')+1:]
                    gCharList = list(gCharString)
                    for index in range(len(gCharList)):
                        if gCharList[index].isalpha() == True:
                            guessedCharacters.append(gCharList[index])
                    #print('guessedCharacters:',guessedCharacters)
                    # Create a formatted guess Characters Input

                    # Parse currentWord
                    currentWord = parsedData[3][parsedData[3].find(':')+1:]
                    #print('currentWord: ', currentWord)
                    screen.addstr(11,0, 'Current Guess: '+currentWord)
                   
                    # Parse playerNum
                    playerNum = parsedData[4][-1]
                    #print('playerNum:',playerNum)
                    screen.addstr(12,0, 'Player '+playerNum+'s turn.')
                    
                    screen.refresh()
                
                else:
                    screen.addstr(13,0,'                                                                  ')
                    if data.decode('utf8')[0] == '#':
                        screen.addstr(13,0,data.decode('utf-8')[1:])
                    else:
                        screen.addstr(13,0,data.decode('utf-8'))
                    screen.refresh()
                    #sys.stdout.buffer.raw.write(data)

                if(data.decode('utf8')[0] == '#'):
                    #msg = sys.stdin.buffer.raw.read(SEND_BUFFER_SIZE)
                    msg = []
                    while True:
                        c = screen.getch()
                        if c == curses.KEY_ENTER or c == 10 or c == 13:
                            if len(msg) == 0:
                                continue
                            break
                        if c == 8 or c == 127 or c == curses.KEY_BACKSPACE:
                            if len(msg) > 0:
                                msg = msg[:-1]
                                screen.addstr("\b \b")
                        else:
                            msg.append(chr(c))
                            msgStream = "".join(msg)
                            screen.addstr(13,34,msgStream)
                        screen.refresh()
                        # TODO: ADD python escape sequence using ctrl+C (simfara)

                    sendmsg = sock.sendall(''.join(msg).encode('utf-8'))
                
                #screen.clear()
                #screen.refresh()  
                #curses.endwin()
            curses.endwin()
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
