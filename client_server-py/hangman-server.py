#!/usr/bin/env python
###############################################################################
# server-python.py
# Name: Alex Hoerr
###############################################################################

import sys
import socket
import time
from typing import Counter

SEND_BUFFER_SIZE = 2048
RECV_BUFFER_SIZE = 2048
QUEUE_LENGTH = 4

# Bootstrap to start a new game
def startNewGame(conn_list,sock):
        # A number of players is required to connect to the server, this is determined by queue length
        print("Socket successfully established, waiting for players...")
        while len(conn_list) < QUEUE_LENGTH:
            connection, address = sock.accept()
            conn_list += [connection]
            print("Connection from {ip} on port {port}".format(ip=address[0], port=address[1]))
            currPlayerMsg = "*Currently {cnlen}/{ql} players. ".format(cnlen=len(conn_list),ql=QUEUE_LENGTH)
            broadcastMsgPacket(conn_list,currPlayerMsg.encode('utf-8'))
            print(currPlayerMsg[1:-1])
        
        # Sends a message to users that the word guesser is choosing a new word (polish)
        sgMsg = '{ql} players. Waiting for word guesser to guess word '.format(ql=QUEUE_LENGTH)
        broadcastMsgPacket(conn_list,sgMsg.encode('utf-8'))
        print(sgMsg[:-1])

        return ('','',6,[],0)

# Getting the chosenWord from the first player in the connection list (Word Guesser)
def inputChooseWord(conn_list):
        chosenWord = ''
        while chosenWord == '':
            sendMsgPacket(conn_list[0],b'#Please chose the Word to guess: ')
            chosenWord = recvStringPacket(conn_list[0]).upper()
            if chosenWord.isalpha() == False or len(chosenWord) == 0:
                chosenWord = ''
        return chosenWord

# Recieves packets from clients
def recvPacket(connection):
    return connection.recv(RECV_BUFFER_SIZE)

# Recieves the packets and converts the message to string form
def recvStringPacket(connection):
    return recvPacket(connection).decode("utf-8",errors='ignore')

# Sends Packets to the client
def sendMsgPacket(connection,msg):
    sendmsg = connection.sendall(msg)
    time.sleep(0.1)

# Sends the message packet to all clients
def broadcastMsgPacket(conn_list,msg):
    for conn in conn_list:
        sendMsgPacket(conn, msg)

# Sends the packet containing essential game info data '!' is used as a prefix to let clients know that its essential game data
def sendGamePacket(hangmanSegments, guessedCharacters, currentWord,playerNum, conn_list):
    msg = "!|segments:{seg}|guessedChars:{gchar}|currentWord:{cword}|playerNum:{pnum}|!\n".format(seg = hangmanSegments, gchar = guessedCharacters, cword = ''.join(currentWord), pnum = playerNum+1)
    broadcastMsgPacket(conn_list,msg.encode('utf-8'))
    print(msg)

# Chooses the next player in the queue to send the message to
def selectNextPlayer(playerNum):
    playerNum = (playerNum + 1) % (QUEUE_LENGTH - 1)
    return playerNum

# Main bootstrap, server manages starting the game, connecting to all clients, and running all server side operations of the game
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

        # Starts a new game which will first wait for all the clients to connect
        chosenWord, guessedLetter, hangmanSegments, guessedCharacters,playerNum = startNewGame(conn_list,sock)
        
        # The first client to connect will be asked to choose a word for the game
        chosenWord = inputChooseWord(conn_list)


        # Word thats in play thats being guessed on
        # Ex. chosenWord: determine currentWord: de_t_r_m_i__e
        currentWord = ['_' for i in range(len(chosenWord))] 


        # Getting the guessed LETTER from the client
        # If the guessedLetter matches the character in the Chosen Word 
        # Loop through the chosenWord and find any macth and replace it in the currentWord
        # If match not found -1 to the segement
        # Add the guessed letter to the guessedCharacter[]
        while True:
            sendGamePacket(hangmanSegments, guessedCharacters, currentWord, playerNum, conn_list)
            guessedLetter = ''
            while guessedLetter == '':
                try:
                    # A '#' symbol is added to these packets to let the client know it needs to respond to these messages
                    sendMsgPacket(conn_list[playerNum+1],b'#Please chose a letter to guess: ')
                    guessedLetter = recvStringPacket(conn_list[playerNum+1]).upper()
                    if(guessedLetter.isalpha() == True and len(guessedLetter) == 1):
                        check = guessedCharacters.index(guessedLetter)
                    guessedLetter = ''
                # Thrown if the character isnt in the string and can be added to the list
                except ValueError as e:
                    guessedCharacters.append(guessedLetter)
                    
            
            wrongGuessedLetter = True
            for i in range(0,len(chosenWord)):
                # If any letter in the guessed letter matches the chosen word, it then is added to the current guess word
                # ex. H____ -> H_ll_
                if guessedLetter == chosenWord[i]:
                    currentWord[i] = guessedLetter
                    wrongGuessedLetter = False
            
            if wrongGuessedLetter:
                hangmanSegments -= 1

            # Pieces of code decide the win condition of both the chooser and Guessers
            # Guessers win if all letters of the chosen word are figured out, chooers wins if full hangman is drawn
            if chosenWord == ''.join(currentWord):
                gameWinMsg = '*Guessers Win! Word was {cw}'.format(cw=chosenWord)
                sendGamePacket(hangmanSegments, guessedCharacters, chosenWord, playerNum, conn_list)
                broadcastMsgPacket(conn_list, gameWinMsg.encode('utf-8'))
                print('Guessers Win!')
                conn_list.append(conn_list.pop(0))
                chosenWord, guessedLetter, hangmanSegments, guessedCharacters, playerNum = startNewGame(conn_list,sock)
                chosenWord = inputChooseWord(conn_list)
                currentWord = ['_' for i in range(len(chosenWord))]
                continue

            if hangmanSegments == 0:
                gameOverMsg = '*Chooser Wins! Word was {cw}'.format(cw=chosenWord)
                sendGamePacket(hangmanSegments, guessedCharacters, chosenWord, playerNum, conn_list)
                broadcastMsgPacket(conn_list, gameOverMsg.encode('utf-8'))
                print("Game Over!")
                print("Word was: ",chosenWord)
                conn_list.append(conn_list.pop(0))
                chosenWord, guessedLetter, hangmanSegments, guessedCharacters, playerNum = startNewGame(conn_list,sock)
                chosenWord = inputChooseWord(conn_list)
                currentWord = ['_' for i in range(len(chosenWord))]
                continue

            # Moves to the next guesser but skips the next chooser
            playerNum = selectNextPlayer(playerNum)

def main():
    """Parse command-line argument and call server function """
    if len(sys.argv) != 2:
        sys.exit("Usage: python server-python.py [Server Port]")
    server_port = int(sys.argv[1])
    server(server_port)

if __name__ == "__main__":
    main()
