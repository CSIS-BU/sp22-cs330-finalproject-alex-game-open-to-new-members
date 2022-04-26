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
QUEUE_LENGTH = 3

# Loops until a connection is accepted
# Wait for four people to connect to start the game
def startNewGame(conn_list,sock):
        print("Socket successfully established, waiting for players...")
        while len(conn_list) < QUEUE_LENGTH:
            connection, address = sock.accept()
            conn_list += [connection]
            print("Connection from {ip} on port {port}".format(ip=address[0], port=address[1]))
            currPlayerMsg = "Currently {cnlen}/{ql} players.\n".format(cnlen=len(conn_list),ql=QUEUE_LENGTH)
            broadcastMsgPacket(conn_list,currPlayerMsg.encode('utf-8'))
            print(currPlayerMsg[:-1])
        

        sgMsg = '{ql} players. Ready to start the game!\n'.format(ql=QUEUE_LENGTH)
        broadcastMsgPacket(conn_list,sgMsg.encode('utf-8'))
        print(sgMsg[:-1])

        return ('','',6,[],0)

def inputChooseWord(conn_list):
        #Getting the chosenWord from the first player in the connection list
        # (Remove later)chosenWord = input('Please chose the Word to guess. ').upper()
        sendMsgPacket(conn_list[0],b'Please chose the Word to guess: ')
        return recvStringPacket(conn_list[0]).upper()

def recvPacket(connection):
    return connection.recv(RECV_BUFFER_SIZE)

def recvStringPacket(connection):
    return recvPacket(connection).decode("utf-8",errors='ignore')[:-1]

def sendMsgPacket(connection,msg):
    sendmsg = connection.sendall(msg)

def broadcastMsgPacket(conn_list,msg):
    for conn in conn_list:
        sendMsgPacket(conn, msg)

def sendGamePacket(hangmanSegments, guessedCharacters, currentWord,playerNum, conn_list):
    msg = "!|segments:{seg}|guessedChars:{gchar}|currentWord:{cword}|playerNum:{pnum}|!\n".format(seg = hangmanSegments, gchar = guessedCharacters, cword = ''.join(currentWord), pnum = playerNum+1)
    broadcastMsgPacket(conn_list,msg.encode('utf-8'))
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


        chosenWord, guessedLetter, hangmanSegments, guessedCharacters,playerNum = startNewGame(conn_list,sock)
        
        chosenWord = inputChooseWord(conn_list)
        # Word thats in play thats being guessed on
        # Ex. chosenWord: determine currentWord: de_t_r_m_i__e
        currentWord = ['_' for i in range(len(chosenWord))] 


        #Getting the guessed LETTER from the client
        # If the guessedLetter matches the character in the Chosen Word 
        # Loop through the chosenWord and find any macth and replace it in the currentWord
        # If macth not found -1 to the segement
        # Add the guessed letter to the guessedCharacter[]
        while True:
            sendGamePacket(hangmanSegments, guessedCharacters, currentWord, playerNum, conn_list)
            guessedLetter = ''
            while guessedLetter == '':
                try:
                    # guessedLetter = input( 'Please chose a letter to guess.  ').upper()
                    sendMsgPacket(conn_list[playerNum+1],b'Please chose a letter to guess: ')
                    guessedLetter = recvStringPacket(conn_list[playerNum+1]).upper()
                    if(guessedLetter.isalpha() == True or len(guessedLetter) == 1):
                        check = guessedCharacters.index(guessedLetter)
                        sendMsgPacket(conn_list[playerNum+1],b'Character already chosen\n')
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
                gameWinMsg = 'Guessers Win!\nWord was {cw}\n'.format(cw=chosenWord)
                broadcastMsgPacket(conn_list, gameWinMsg.encode('utf-8'))
                print('Guessers Win!')
                conn_list.append(conn_list.pop(0))
                chosenWord, guessedLetter, hangmanSegments, guessedCharacters, playerNum = startNewGame(conn_list,sock)
                chosenWord = inputChooseWord(conn_list)
                currentWord = ['_' for i in range(len(chosenWord))]
                continue

            if hangmanSegments == 0:
                gameOverMsg = 'Chooser Wins!\nWord was {cw}\n'.format(cw=chosenWord)
                broadcastMsgPacket(conn_list, gameOverMsg.encode('utf-8'))
                print("Game Over!")
                print("Word was: ",chosenWord)
                conn_list.append(conn_list.pop(0))
                chosenWord, guessedLetter, hangmanSegments, guessedCharacters, playerNum = startNewGame(conn_list,sock)
                chosenWord = inputChooseWord(conn_list)
                currentWord = ['_' for i in range(len(chosenWord))]
                continue

            playerNum = selectNextPlayer(playerNum)

def main():
    """Parse command-line argument and call server function """
    if len(sys.argv) != 2:
        sys.exit("Usage: python server-python.py [Server Port]")
    server_port = int(sys.argv[1])
    server(server_port)

if __name__ == "__main__":
    main()
