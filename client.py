import os
import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4466
ADDR = (IP, PORT)
SIZE = 100000
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"
CLIENT_DATA_PATH = "client_data"


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]
        msg = data[1]
        print( "response from server: ")


        if cmd == "OK":
            print(f"{msg}")

        elif cmd == "DOWNLOADING":
            name = data[1]
            text = data[2]
            filepath = os.path.join(CLIENT_DATA_PATH, name)
            with open(filepath, "w") as f:
                f.write(text)
            print(f"file {name} downloaded")

        
        
        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "HELP":
            client.send(cmd.encode(FORMAT))
        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break
        elif cmd == "LIST":
            client.send(cmd.encode(FORMAT))

        elif cmd == "DOWNLOAD":
            filename = data[1]
            fullcmd = f"{cmd}@{filename}"
            client.send(fullcmd.encode(FORMAT))

        else :
            client.send(cmd.encode(FORMAT))
            


            

    print("Disconnected from the server.")
    client.close()

if __name__ == "__main__":
    main()