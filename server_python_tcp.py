import socket
import sys
import os

#https://pythonprogramming.net/sockets-tutorial-python-3/



class TCPServer:
    def __init__(self, host, port, buffer_size, default_filename):
        self.buffer_size =  buffer_size
        self.default_filename = default_filename
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

    def connect(self):
        try:
            while True:
                connect, client_address = self.sock.accept()
                self.connection = connect
                self.get_command()
                self.connection.close()
        except KeyboardInterrupt:
            self.sock.close()
            sys.exit()

    def get_command(self):
        try:
            data = self.connection.recv(self.buffer_size)
            self.command = data.decode('utf-8')
            self.run_command()
        except socket.error:
            print("Failed to receive instructions from the client.", file = sys.stderr)
            self.connection.close()
            sys.exit(1)

    def run_command(self):
        file_index = self.command.find('>')
        if file_index == -1:
            self.filename = self.default_filename
            os.system(self.command + ' > ' + self.filename)
        else:
            command_array = self.command.split('>')
            self.filename = command_array[1].replace(' ', '')
            os.system(self.command)
        self.send_file()

    def send_file(self):
        #modiefied from https://www.thepythoncode.com/article/send-receive-files-using-sockets-python

        file_size = os.path.getsize(self.filename)
        SEPARATOR = "<SEPARATOR>"

        try:
            self.connection.send(f"{self.filename}{SEPARATOR}{file_size}".encode())

            with open(self.filename, "rb") as f:
                while True:
                    bytes_read = f.read(self.buffer_size)

                    if not bytes_read:
                        break
                    self.connection.sendall(bytes_read)
            f.close()


        except socket.error:
            print("File transmission failed.", file=sys.stderr)
            sys.exit(1)




def run_sript():
    server_port = int(sys.argv[1])
    Server = TCPServer('localhost', server_port, 512, 'out.txt')
    Server.connect()

if __name__ == '__main__':
    run_sript()

