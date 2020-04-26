import socket
import sys
import struct
import os

def validate(addr):
    try:
        socket.gethostbyname(addr)
        return True
    except:
        return False


class TCPClient:
    def __init__(self, host, port, buffer_size):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(1)

    def connect(self):
        try:
            self.sock.connect((self.host, self.port))
            return True
        except socket.error:
            print("Could not connect to server.", file=sys.stderr)
            sys.exit(1)
        #self.get_send_command()

    def get_command(self):
        print("Enter command:", end=" ")
        command = input()
        return command

    def send_command(self, command):
        try:
            self.sock.send(bytes(command, "utf-8"))
            return True
        except socket.error:
            print("Failed to send command. Terminating.", file=sys.stderr)
            self.sock.close()
            print("socket.error")
            return False
            #sys.exit(1)
        #self.receive_file()

    def receive_file(self):
        SEPARATOR = "<SEPARATOR>"

        try:
            received = self.sock.recv(self.buffer_size).decode()
            filename, filesize = received.split(SEPARATOR)

            filename = os.path.basename(filename)
            filesize = int(filesize)

            if os.path.exists(filename):
                os.remove(filename)

            with open(filename, 'a') as f:
                while True:
                    bytes_read = self.sock.recv(self.buffer_size)
                    if not bytes_read:
                        break

                    f.write(bytes_read.decode())
            f.close()

            if filesize == os.path.getsize(filename):
                print("File %s saved." % filename)

            # print("File %s saved." % filename)
        except socket.error:
            print("Did not receive response.", file=sys.stderr)
            self.sock.close()
            return 'case 4'
            #sys.exit()

        finally:
            self.sock.close()

def run_script():

    print("Enter server name or IP address:", end=" ")
    server_name = input()

    print("Enter port:", end=" ")
    port = int(input())

    if port < 0 or port > 65535:
        print("Invalid port number.", file=sys.stderr)
        sys.exit()

    if not validate(server_name):
        print("Could not connect to server.", file=sys.stderr)
        sys.exit()

    client = TCPClient(server_name, port, 512)
    connection = client.connect()
    if connection:
        command = client.get_command()
        client.send_command(command)

        client.receive_file()


if __name__ == '__main__':
    run_script()

