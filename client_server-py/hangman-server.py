#!/usr/bin/env python
###############################################################################
# server-python.py
# Name: Alex Hoerr
###############################################################################

import sys
import socket
from typing import Counter

SEND_BUFFER_SIZE = 2048
RECV_BUFFER_SIZE = 2048
QUEUE_LENGTH = 2

def recvPacket(connection):
    return connection.recv(RECV_BUFFER_SIZE)

def recvStringPacket(connection):
    return recvPacket(connection).decode("utf-8",errors='ignore')[:-1]

def sendMsgPacket(connection,msg):
    sendmsg = connection.sendall(msg)

def sendGamePacket(hangmanSegments, guessedCharacters, currentWord, conn_list):
    msg = "[segments:{seg},guessedChars:{gchar},currentWord:{cword},playerNum:{pnum}]\n".format(seg = hangmanSegments, gchar = guessedCharacters, cword = ''.join(currentWord), pnum = playerNum)
    for conn in conn_list:
        sendMsgPacket(conn, msg.encode("utf-8"))
    # Kept for debugging
    print(msg)

def selectNextPlayer(playerNum):
    playerNum = (playerNum + 1) % (QUEUE_LENGTH - 1)
    return playerNum

# server() Listen on socket and print received message to sys.stdout
def server(server_port):

    # These variables denote the host (localhost) to bind itself to the server and the user passed in port
    HOST = "127.0.0.1" 
    PORT = server_port
    conn_list = []
    playerNum = 0

    # Opens a socket and sets the socket mode to IPV4 and TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        # Binds the socket to the server
        sock.bind((HOST,PORT))

        # Listens for new clients with a client queue defined by QUEUE_LENGTH
        sock.listen(QUEUE_LENGTH)

        # Loops until a connection is accepted
        # When a new connection is accpeted it loops through and recieves all the chunks of data the client sends to the server and then closes the connection
        '''       
        while True:
            connection, address = sock.accept()
            with connection:
                while True:
                    data = connection.recv(RECV_BUFFER_SIZE)
                    sys.stdout.buffer.raw.write(data)

                    msg = sys.stdin.buffer.raw.read(SEND_BUFFER_SIZE)
                    sendmsg = connection.sendall(msg)
                sys.stdout.flush()
        '''

        '''
        connection, address = sock.accept()
        conn_list += [connection]
        '''
    

        # Wait for four people to connect to start the game
        # Define fn for
        print("Socket successfully established, waiting for players...")
        while len(conn_list) < QUEUE_LENGTH:
            connection, address = sock.accept()
            conn_list += [connection]
            print("Connection from {ip} on port {port}".format(ip=address[0], port=address[1]))
            print("Currently {cnlen}/{ql} players.".format(cnlen=len(conn_list),ql=QUEUE_LENGTH))
        ###
        print('{ql} players. Ready to start the game!'.format(ql=QUEUE_LENGTH))

        chosenWord = ''
        guessedLetter = ''
        hangmanSegments = 6
        guessedCharacters = []



        #Getting the chosenWord from the first player in the connection list
        # (Remove later)chosenWord = input('Please chose the Word to guess. ').upper()
        sendMsgPacket(conn_list[0],b'Please chose the Word to guess:\n')
        chosenWord = recvStringPacket(conn_list[0]).upper()
        print(chosenWord)
        if(chosenWord != 'HELLO'):
            print("Error WOrd is:",chosenWord)
            print("Correct word :","HELLO")
        # Word thats in play thats being guessed on
        # Ex. chosenWord: determine currentWord: de_t_r_m_i__e
        currentWord = ['_' for i in range(len(chosenWord))] 


        #Getting the guessed LETTER from the client
        #guessedLetter = input( 'Please chose a letter to guess.  ').upper()
        

        # If the guessedLetter matches the character in the Chosen Word 
        # Loop through the chosenWord and find any macth and replace it in the currentWord
        # If macth not found -1 to the segement
        # Add the guessed letter to the guessedCharacter[]
        while True:
            playerNum = selectNextPlayer(playerNum)
            sendGamePacket(hangmanSegments, guessedCharacters, currentWord,conn_list)
            guessedLetter = ''
            while guessedLetter == '':
                try:
                    # guessedLetter = input( 'Please chose a letter to guess.  ').upper()
                    sendMsgPacket(conn_list[playerNum+1],b'Please chose a letter to guess\n')
                    guessedLetter = recvStringPacket(conn_list[playerNum+1]).upper()
                    if(guessedLetter != ''):
                        check = guessedCharacters.index(guessedLetter)
                        print('Character already chosen ')
                    guessedLetter = ''
                except ValueError as e:
                    guessedCharacters.append(guessedLetter)
                    # Add a loop to a function to keep choosing guessed letters
                    # print("value chosen, : ", guess)
                    
                
            wrongGuessedLetter = True
            for i in range(0,len(chosenWord)):
                if guessedLetter == chosenWord[i]:
                    currentWord[i] = guessedLetter
                    wrongGuessedLetter = False
            
            if wrongGuessedLetter:
                hangmanSegments -= 1

            if chosenWord == ''.join(currentWord):
                print('Guessers Win!')
                #sendGamePacket(hangmanSegments, guessedCharacters, chosenWord)
                break

            if hangmanSegments == 0:
                print("Game Over!")
                print("Word was: ",chosenWord)
                #sendGamePacket(hangmanSegments, guessedCharacters, chosenWord)
                break;
                     

        






def main():
    """Parse command-line argument and call server function """
    if len(sys.argv) != 2:
        sys.exit("Usage: python server-python.py [Server Port]")
    server_port = int(sys.argv[1])
    server(server_port)

if __name__ == "__main__":
    main()
