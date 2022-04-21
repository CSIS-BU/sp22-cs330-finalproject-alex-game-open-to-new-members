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
QUEUE_LENGTH = 4

def revcPacket(connection):
    return connection.recv(RECV_BUFFER_SIZE)

def sendPacket(hangmanSegments, guessedCharacters, currentWord):
    print("Segments:{seg},Guessed Chars:{gchar},currentWord:{cword}".format(seg = hangmanSegments, gchar = guessedCharacters, cword = ''.join(currentWord)))

# server() Listen on socket and print received message to sys.stdout
def server(server_port):

    # These variables denote the host (localhost) to bind itself to the server and the user passed in port
    HOST = "127.0.0.1" 
    PORT = server_port
    conn_list = []

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
        while len(conn_list) < 4:
            connection, address = sock.accept()
            conn_list += [connection]
            print("Connection from {ip} on port {port}".format(ip=address[0], port=address[1]))
            print("Currently {cnlen}/{ql} players.".format(cnlen=len(conn_list)))
        ###
        print('{QUEUE_LENGTH} players. Ready to start the game!')

        chosenWord = ''
        guessedLetter = ''
        hangmanSegments = 6
        guessedCharacters = []



        #Getting the chosenWord from the client
        chosenWord = input('Please chose the Word to guess. ').upper()

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
            sendPacket(hangmanSegments, guessedCharacters, currentWord)
            guessedLetter = ''
            while guessedLetter == '':
                try:
                    guessedLetter = input( 'Please chose a letter to guess.  ').upper()
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
                sendPacket(hangmanSegments, guessedCharacters, chosenWord)
                break

            if hangmanSegments == 0:
                print("Game Over!")
                sendPacket(hangmanSegments, guessedCharacters, chosenWord)
                break;
                     

        






def main():
    """Parse command-line argument and call server function """
    if len(sys.argv) != 2:
        sys.exit("Usage: python server-python.py [Server Port]")
    server_port = int(sys.argv[1])
    server(server_port)

if __name__ == "__main__":
    main()
