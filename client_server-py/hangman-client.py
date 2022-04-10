import sys 
import socket 
 
SEND_BUFFER_SIZE = 2048 
 
def client(server_ip, server_port): 
    """TODO: Open socket and send message from sys.stdin""" 
    # create an INET, STREAMing socket 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
        # now connect to server 
        s.connect((server_ip, server_port)) 
         
        while True: 
            content = sys.stdin.buffer.read(SEND_BUFFER_SIZE) 
            if not content: break 
            sent = s.sendall(content) 
            if sent == 0: 
                raise RuntimeError("socket connection broken") 
    pass 
 
 
def main(): 
    """Parse command-line arguments and call client function """ 
    if len(sys.argv) != 3: 
        sys.exit("Usage: python3 client-python.py [Server IP] [Server Port] < [message]") 
    server_ip = sys.argv[1] 
    server_port = int(sys.argv[2]) 
    client(server_ip, server_port) 
 
if __name__ == "__main__": 
    main() 