import socket
import threading
import json

host = '127.0.0.1' 
port = 55555

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

server.bind((host, port))
server.listen()
print(f"Server running on {host}:{port}")

clients= []
usernames=[]
dict_clients= {}


def broadcast(message,_client):
    for client in clients:
        if client != _client:
            client.send(message)


def handel_messages(client, address):

    client.send("@username".encode("utf-8"))
    username = client.recv(1024).decode('utf-8')
    clients.append(client)
    dict_clients[username]= client
    print(f"{username} is connected with {str(address)}")
    client.send("Connect to server".encode("utf-8"))

    while True :
        try:
          message = client.recv(1024)
          msg_dict= eval(message) 
          sender = msg_dict["username"]
          reciver = msg_dict["des_username"]
          message = msg_dict ["message"]
          connection_des = dict_clients[reciver]
          connection_des.send(message)
        except:   
          index = clients.index(client)
          username = usernames[index]
          broadcast(f"ChatBot: {username} disconnected".encode('utf-8'))
          clients.remove(client)
          usernames.remove(username)
          client.close()
          break
 
def receive_connections():
    
    while True :
        client, address = server.accept()   
        thread = threading.Thread(target= handel_messages , args=(client,)) 
        thread.start()

       
       

receive_connections()        