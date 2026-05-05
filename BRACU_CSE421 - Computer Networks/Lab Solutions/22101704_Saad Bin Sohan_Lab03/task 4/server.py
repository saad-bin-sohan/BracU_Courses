import socket 

port = 5555
hostname = socket.gethostname()
host_ip = socket.gethostbyname(hostname)
server_socket_addr = (host_ip, port)
buffer = 1000
format = "utf-8"
vowel_list = ['A','E','I','O','U','a','e','i','o','u']

#------------------------------------------------------------------

server_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_obj.bind(server_socket_addr)
server_obj.listen()
print("Server is listening")

while True:    

    client_object, client_sock = server_obj.accept()
    print("Connected to:", client_sock)
    connected = True

    while connected:

        received_message_length = client_object.recv(buffer).decode(format)

        if received_message_length:

            received_message_length = int(received_message_length)
            received_message = client_object.recv(received_message_length).decode(format)
            print(received_message)

            if received_message == "Disconnect":

                client_object.send("Goodbye. Nice to Serve you".encode(format))
                print("Terminating the connection with:", client_sock)
                connected = False

            else:

                salary = 0
                hour = int(received_message)

                if hour <= 40:

                    salary += (200 * hour)

                else:
                    
                    salary += 8000 + (300*hour)

                salary = str(salary)
                client_object.send(salary.encode(format))

                   



    client_object.close()
