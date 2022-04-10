import sys 
import socket 
 
RECV_BUFFER_SIZE = 2048 
QUEUE_LENGTH = 10 
 
def server(server_port): 
    """TODO: Listen on socket and print received message to sys.stdout""" 
    # create an INET, STREAMing socket 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket: 
        # bind the socket to the host and its port 
        serversocket.bind(('', server_port)) 
        # prepare for connection 
        serversocket.listen(QUEUE_LENGTH) 
 
        while True: 
            # accept connections from outside 
            (clientsocket, address) = serversocket.accept() 
 
            with clientsocket: 
                while True: 
                    # receive data and print it out 
                    data = clientsocket.recv(RECV_BUFFER_SIZE) 
                    if not data: break 
                    sys.stdout.buffer.write(data) 
                sys.stdout.flush() 
    pass 
 
 
def main(): 
    """Parse command-line argument and call server function """ 
    if len(sys.argv) != 2: 
        sys.exit("Usage: python server-python.py [Server Port]") 
    server_port = int(sys.argv[1]) 
    server(server_port) 
 
if __name__ == "__main__": 
    main() 