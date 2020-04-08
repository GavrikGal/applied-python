import socket
import argparse


class TaskQueueServer:

    def __init__(self, ip, port, path, timeout):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connection.bind((ip, port))

    def run(self):
        self.connection.listen(10)
        while True:
            current_connection, address = self.connection.accept()
            while True:
                data = current_connection.recv(2048)

                if data == b'quit\n':
                    current_connection.shutdown(1)
                    current_connection.close()
                elif data == b'stop\n':
                    current_connection.shutdown(1)
                    current_connection.close()
                elif data:
                    print(data)



def parse_args():
    parser = argparse.ArgumentParser(description='This is a simple task queue server with custom protocol')
    parser.add_argument(
        '-p',
        action="store",
        dest="port",
        type=int,
        default=5555,
        help='Server port')
    parser.add_argument(
        '-i',
        action="store",
        dest="ip",
        type=str,
        default='0.0.0.0',
        help='Server ip adress')
    parser.add_argument(
        '-c',
        action="store",
        dest="path",
        type=str,
        default='./',
        help='Server checkpoints dir')
    parser.add_argument(
        '-t',
        action="store",
        dest="timeout",
        type=int,
        default=300,
        help='Task maximum GET timeout in seconds')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    server = TaskQueueServer(**args.__dict__)
    server.run()
