import socket

format = "utf-8"
port = 5555
buffer = 1000
hostname = socket.gethostname()
host_ip = socket.gethostbyname(hostname)
server_socket_addr = (host_ip,port)
client_obj = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_obj.connect(server_socket_addr)

#-----------------------------------------------------------------------

def send_message(message):

    message = message.encode(format)
    message_length = len(message)
    message_length = str(message_length).encode(format)
    message_length += b" "*(buffer - len(message_length))
    client_obj.send(message_length)
    client_obj.send(message)
    print(client_obj.recv(2048).decode(format))

while True:

    message = input("How many hours worked?: ")

    if message == "Disconnect":
    
        send_message(message)
        break
    
    else:
    
        send_message(message)