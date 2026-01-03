from customtkinter import *
from PIL import Image
from socket import *
import threading

IP = "0.0.0.0"
PORT = 8080
USERNAME = "user"

window = CTk()
window.geometry("400x400")
window.title("LogiTalk")

modal = CTkToplevel(window)
modal.geometry("400x200")
modal.title("entry...")
modal.focus()
modal.grab_set()

ip_entry = CTkEntry(modal, placeholder_text="ip:port")
username_entry = CTkEntry(modal, placeholder_text="username")

client = socket(AF_INET, SOCK_STREAM)

def receive_message(username, message, from_self: bool = False):
    anchor = "e" if from_self else "w"
    bg_color = "#4a90e2" if from_self else "#5b42db"
    justify = "right" if from_self else "left"
    msgFrame = CTkFrame(chatFrame, fg_color=bg_color, corner_radius=10)
    usernameLabel = CTkLabel(msgFrame, text=username, anchor=anchor, wraplength=180, justify = justify)
    messageLabel = CTkLabel(msgFrame, text=message, anchor=anchor, wraplength=180, justify = justify)
    usernameLabel.pack(anchor=anchor)
    messageLabel.pack(anchor=anchor)
    msgFrame.pack(anchor=anchor, pady=10, padx=10, ipadx=10, ipady=10)

def listen_server():
    while True:
        try:
            data = client.recv(1024).decode()
            if data:
                username, message = data.split(":", 1)
                window.after(0, receive_message, username, message)
        except:
            break

def submit_handler():
    global IP, PORT, USERNAME

    data = ip_entry.get()
    IP, PORT = data.split(":")
    PORT = int(PORT)
    USERNAME = username_entry.get()

    client.connect((IP, PORT))
    client.send(f"{USERNAME}:Connected!".encode())

    threading.Thread(target=listen_server, daemon=True).start()
    modal.destroy()

submit_button = CTkButton(modal, text="submit", command=submit_handler)
ip_entry.pack(pady=5)
username_entry.pack(pady=5)
submit_button.pack(pady=10)

chatFrame = CTkScrollableFrame(window, height=275, label_text="LogiTalk")
chatFrame.pack(fill="both", expand=True)

inputFrame = CTkFrame(window)
inputFrame.pack(fill="x", pady=5)

sendEntry = CTkEntry(inputFrame, width=300)
sendEntry.grid(row=0, column=0, padx=5)

def send_message():
    text = sendEntry.get()
    if not text:
        return
    sendEntry.delete(0, END)
    receive_message(USERNAME, text, True)
    client.send(f"{USERNAME}:{text}".encode())

sendButton = CTkButton(inputFrame, text=">", width=50, command=send_message)
sendButton.grid(row=0, column=1)

window.mainloop()
