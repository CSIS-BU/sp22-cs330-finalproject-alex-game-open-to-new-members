
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <strings.h>
#include <stdlib.h>
#include <unistd.h>

#include <string>
#include <iostream>

#define MAX_PENDING 5
#define MAX_SIZE 2048
int
main(int argc, char** argv)
{
 struct sockaddr_in sin;
 char buf[MAX_SIZE];
 int buf_len;
 socklen_t addr_len;
 int s, new_s;
 char *port;
 if(argc==2) {
 port = argv[1];
 }
 else {
 fprintf(stderr, "usage: %s port\n", argv[0]);
 exit(1);
 }
 /* build address data structure */
 bzero((char *)&sin, sizeof(sin));
 sin.sin_family = AF_INET;
 sin.sin_addr.s_addr = INADDR_ANY;
 sin.sin_port = htons(atoi(port));
 /* setup passive open */
 if ((s = socket(PF_INET, SOCK_STREAM, 0)) < 0) {
 perror("simplex-talk: socket");
 exit(1);
 }
 if ((bind(s, (struct sockaddr *)&sin, sizeof(sin))) < 0) {
 perror("simplex-talk: bind");
 exit(1);
 }
 listen(s, MAX_PENDING);
 /* wait for connection, then receive and print text */
 while(1) {
 if ((new_s = accept(s, (struct sockaddr *)&sin, &addr_len)) < 0) {
 fprintf(stderr, "error: %s accept\n", argv[0]);
 exit(1);
 }
 while ( (buf_len = recv(new_s, buf, sizeof(buf), 0)) ) {
 fwrite(buf, 1, buf_len, stdout);
 }
 fflush(stdout);
 close(new_s);
 }
 close(s);
 return 0;
}