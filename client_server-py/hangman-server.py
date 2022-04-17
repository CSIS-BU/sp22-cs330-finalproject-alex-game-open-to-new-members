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
QUEUE_LENGTH = 10

# server() Listen on socket and print received message to sys.stdout
def server(server_port):

    # These variables denote the host (localhost) to bind itself to the server and the user passed in port
    HOST = "127.0.0.1" 
    PORT = server_port

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
    
        chosenWord = ''
        guessedLetter = ''
        hangmanSegments = 6
        guessedCharacters = []

        # Word thats in play thats being guessed on
        # Ex. chosenWord: determine currentWord: de_t_r_m_i__e
        currentWord = ''

        #Getting the chosenWord from the client
        chosenWord = input('Please chose the Word to guess. ').upper()

        # Generate the currentWord based on the chosenWord
        # Fill current word with dashes equal to chosenWord length
        currentWord.ljust(chosenWord.count(),'_')


        #Getting the guessed LETTER from the client
        guessedLetter = input( 'Please chose a letter to guess.  ').upper()
        
        # If the guessedLetter matches the character in the Chosen Word 
        # Loop through the chosenWord and find any macth and replace it in the currentWord
        # If macth not found -1 to the segement
        # Add the guessed letter to the guessedCharacter[]
        while True:

            print("GameData: Segments: {seg}, Guessed Chars: {gchar}, currentWord: {cword}".format(seg = hangmanSegments, gchar = guessedCharacters, cword = currentWord))
            try:
                guessedLetter = input( 'Please chose a letter to guess.  ').upper()
            except ValueError as e:
                // Add a loop to a function to keep choosing guessed letters
                guessedLetter = input( 'Please chose a letter to guess.  ').upper()
                
            wrongGuessedLetter = True
            for i in range(0,len(chosenWord)):
                if guessedLetter == chosenWord[i]:
                    chosenWord[i] = guessedLetter
                    wrongGuessedLetter = False
            
            if wrongGuessedLetter:
                hangmanSegments--;

            if hangmanSegments == 0:
                print("Game Over!")
                break;
                     

        






def main():
    """Parse command-line argument and call server function """
    if len(sys.argv) != 2:
        sys.exit("Usage: python server-python.py [Server Port]")
    server_port = int(sys.argv[1])
    server(server_port)

if __name__ == "__main__":
    main()
