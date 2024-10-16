import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
import random

# Fonction pour recevoir les messages
def receive_messages(client_socket, text_area):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                text_area.config(state=tk.NORMAL)
                text_area.insert(tk.END, message + "\n", "message")
                text_area.yview(tk.END)
                text_area.config(state=tk.DISABLED)
        except ConnectionResetError:
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END, "Connexion perdue avec le serveur.\n", "error")
            text_area.yview(tk.END)
            text_area.config(state=tk.DISABLED)
            break

# Fonction pour envoyer des messages
def send_message(client_socket, input_field, username, text_area):
    message = input_field.get()
    input_field.delete(0, tk.END)
    if message:
        try:
            full_message = f"{username}: {message}"
            client_socket.send(full_message.encode('utf-8'))
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END, f"Vous: {message}\n", "self")
            text_area.yview(tk.END)
            text_area.config(state=tk.DISABLED)
        except BrokenPipeError:
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END, "Erreur : Impossible d'envoyer le message.\n", "error")
            text_area.yview(tk.END)
            text_area.config(state=tk.DISABLED)

# Fonction pour créer la fenêtre de chat
def create_chat_window(client_socket, username):
    # Configuration de la fenêtre principale
    root = tk.Tk()
    root.title(f"Chat - {username}")

    # Zone de texte pour afficher les messages
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Champ de texte pour entrer les messages
    input_field = tk.Entry(root)
    input_field.pack(padx=10, pady=10, fill=tk.X)

    # Bouton pour envoyer les messages
    send_button = tk.Button(root, text="Envoyer", command=lambda: send_message(client_socket, input_field, username, text_area))
    send_button.pack(pady=5)

    # Thread pour recevoir les messages
    thread = threading.Thread(target=receive_messages, args=(client_socket, text_area), daemon=True)
    thread.start()

    # Gestion de la touche "Enter" pour envoyer des messages
    input_field.bind("<Return>", lambda event: send_message(client_socket, input_field, username, text_area))

    # Personnalisation des couleurs
    random_color = random.choice(["blue", "green", "purple", "orange"])
    text_area.tag_config("self", foreground=random_color)
    text_area.tag_config("error", foreground="red")

    # Lancement de la boucle principale de l'interface graphique
    root.mainloop()

# Fenêtre d'entrée du nom d'utilisateur
def get_username():
    def on_submit():
        username = username_entry.get()
        if username:
            username_window.destroy()
            start_client(username)
        else:
            messagebox.showerror("Erreur", "Le nom d'utilisateur ne peut pas être vide.")
    
    username_window = tk.Tk()
    username_window.title("Entrer un nom d'utilisateur")

    tk.Label(username_window, text="Entrez votre nom d'utilisateur :").pack(pady=10)
    username_entry = tk.Entry(username_window)
    username_entry.pack(padx=10, pady=10)

    submit_button = tk.Button(username_window, text="Commencer", command=on_submit)
    submit_button.pack(pady=10)

    username_window.mainloop()

# Initialisation du client et gestion des erreurs de connexion
def start_client(username):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('localhost', 5555))  # Connectez-vous à l'adresse du serveur
        create_chat_window(client, username)
    except ConnectionRefusedError:
        messagebox.showerror("Erreur", "Impossible de se connecter au serveur.")

if __name__ == "__main__":
    get_username()
