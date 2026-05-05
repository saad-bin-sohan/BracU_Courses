import socket 

port = 5555
hostname = socket.gethostname()
host_ip = socket.gethostbyname(hostname)
server_socket_addr = (host_ip, port)
buffer = 1000
format = "utf-8"

server_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_obj.bind(server_socket_addr)
server_obj.listen()
print("Server is listening")

#---------------------------------------------------------------------------------------------

while True:

    client_object, client_sock = server_obj.accept()
    print("Connected to:", client_sock)
    connected = True

    while connected:

        received_message_length = client_object.recv(buffer).decode(format)

        if received_message_length:

            received_message_length = int(received_message_length)
            received_message = client_object.recv(received_message_length).decode(format)

            if received_message == "Disconnect":

                client_object.send("Goodbye. Nice to Serve you".encode(format))
                print("Terminating the connection with:", client_sock)
                connected = False

            else:
                
                print(received_message)
                client_object.send("Message Received Client!".encode(format))

    client_object.close()
