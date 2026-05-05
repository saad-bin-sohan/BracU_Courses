import socket
import threading

port = 5555
hostname = socket.gethostname()
host_ip = socket.gethostbyname(hostname)
server_socket_addr = (host_ip, port)
buffer = 1000
format = "utf-8"
vowel_list = ['A','E','I','O','U','a','e','i','o','u']

#-------------------------------------------------------------------------

server_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_obj.bind(server_socket_addr)
server_obj.listen()
print("Server is listening")




def client_handling(client_object,client_sock):    

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

                count = 0

                for i in received_message:

                    if i in vowel_list:

                        count += 1

                if count == 0:

                    client_object.send("Not enough vowels".encode(format))

                elif 0<count<=2:

                    client_object.send("Enough vowels I guess".encode(format))

                else:
                    
                    client_object.send("Too many vowels".encode(format))





    client_object.close()


while True:
    client_object, client_sock = server_obj.accept()
    thread = threading.Thread(target=client_handling,args=(client_object,client_sock))
    thread.start()