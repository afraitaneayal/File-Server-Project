import os
import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 4466
ADDR = (IP, PORT)
SIZE = 100000
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"


"""
CMD@Msg
"""

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the File Server".encode(FORMAT))

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]
        print( f"request from client {addr} ", cmd)
    
        if cmd == "HELP":
            send_data = "OK@"
            send_data += "LIST: List all the files from the server.\n"
            send_data += "DOWNLOAD filename: DOWNLOAD a file from the server.\n"
            send_data += "LOGOUT: Disconnect from the server.\n"
            send_data += "HELP: List all the commands."

            conn.send(send_data.encode(FORMAT))

        elif cmd == "LOGOUT":
            break 
        
        elif cmd == "LIST":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"

            if len(files) == 0:
                send_data += "The server is empty."
            else:
                send_data += "\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))

        elif cmd == "DOWNLOAD":
            filename = data[1]
            files = os.listdir(SERVER_DATA_PATH)
            for i in files:
                if filename == i:
                    send_data = "OK"
                    with open(f"{SERVER_DATA_PATH}\\{filename}", "r") as f:
                        text = f.read()
                    send_data = f"DOWNLOADING@{filename}@{text}"
                    conn.send(send_data.encode(FORMAT))
                    print(f"file {filename} sent.")
                    break
                else :
                    send_data = "OK@This file is not in the server."

            if send_data == "OK@This file is not in the server.":
                print("The file is not existing in this server")
                conn.send(send_data.encode(FORMAT))
                    
                


        else : 
            send_data = "OK@"
            send_data += f"The term {cmd} is not recognized as a command. Type HELP to get the list of commands."
            conn.send(send_data.encode(FORMAT))



    print(f"[DISCONNECTED] client {addr} disconnected")

def main():
    print("[STARTING] Server is starting.")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[LISTENING] Server is listening.")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()





if __name__== "__main__":
    main()

