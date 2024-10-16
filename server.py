import socket
import threading

# Liste pour garder la trace de tous les clients connectés
clients = []

# Fonction pour gérer chaque client
def handle_client(client_socket, addr):
    print(f"Nouvelle connexion : {addr}")
    while True:
        try:
            # Recevoir les messages du client
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"{addr} dit : {message}")
                broadcast(message, client_socket)
        except:
            # Si une erreur survient, on ferme la connexion
            print(f"Connexion perdue avec {addr}")
            clients.remove(client_socket)
            client_socket.close()
            break

# Fonction pour envoyer un message à tous les clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

# Fonction principale du serveur
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5555))  # Adresse et port du serveur
    server.listen(5)
    print("Serveur démarré et en attente de connexions...")

    while True:
        # Accepter de nouvelles connexions
        client_socket, addr = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
