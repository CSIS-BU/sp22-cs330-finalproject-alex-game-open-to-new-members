default: cpp

all: cpp

CC=g++

cpp: hangman-client hangman-server


hangman-client: hangman-client.cpp
	$(CC) hangman-client.cpp -o hangman-client

hangman-server: hangman-server.cpp
	$(CC) hangman-server.cpp -o hangman-server

client-c-sol: client-c-sol.c
	$(CC) client-c-sol.c -o client-c
server-c-sol: server-c-sol.c
	$(CC) server-c-sol.c -o server-c

clean:
	rm -f hangman-server hangman-client  *.o
