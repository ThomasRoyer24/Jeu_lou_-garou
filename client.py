import socket
import threading

class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

        try:
            while True:
                message = input()
                self.client.send(message.encode('utf-8'))
        except KeyboardInterrupt:
            print("Déconnexion du client.")


    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(message)
            except Exception as e:
                print(f"Error receiving message from server: {e}")
                break

def main():
    server_ip = open("master_ip.txt", "r").read().strip()
    client = Client(server_ip, 8080)

if __name__ == "__main__":
    main()