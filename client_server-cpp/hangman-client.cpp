
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>
#include <stdlib.h>
#include <strings.h>

#define MAX_SIZE 2048

#include <string>
#include <iostream>

using namespace std;
int main(int argc, char *argv[])
{
    FILE *fp;
    struct hostent *hp;
    struct sockaddr_in sin;
    char *host, *port;
    char buf[MAX_SIZE];
    int s;
    int len;
    if (argc == 3)
    {
        host = argv[1];
        port = argv[2];
    }
    else
    {
        fprintf(stderr, "usage: %s host port\n", argv[0]);
        exit(1);
    }
    /* translate host name into peer's IP address */
    hp = gethostbyname(host);
    if (!hp)
    {
        fprintf(stderr, "%s: unknown host\n", host);
        exit(1);
    }
    /* build address data structure */
    bzero((char *)&sin, sizeof(sin));
    sin.sin_family = AF_INET;
    bcopy(hp->h_addr, (char *)&sin.sin_addr, hp->h_length);
    sin.sin_port = htons(atoi(port));
    /* active open */
    if ((s = socket(PF_INET, SOCK_STREAM, 0)) < 0)
    {
        perror("simplex-talk: socket");
        exit(1);
    }
    if (connect(s, (struct sockaddr *)&sin, sizeof(sin)) < 0)
    {
        perror("simplex-talk: connect");
        close(s);
        exit(1);
    }
    else {
        printf("Connected to server\n");
    }
    int size;
    string plusBuffer = "";
    while ((cin.get(plusBuffer, MAX_SIZE - 1)))
    {
        std::cout << "Sending message: " << plusBuffer << "\n";
        if (send(s, buf, size, 0) < 0)
        {
            perror("client: send");
        }
    }
    // Done, close the s socket descriptor
    close(s);
}