import socket
import argparse
from queue import Queue


class TaskQueueServer:

    def __init__(self, ip, port, path, timeout):
        self.task_queue_pool = TaskQueuePool()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connection.bind((ip, port))

    def queue(self, name):
        return self.task_queue_pool.get(name)

    def add_task(self, queue, length, data):
        return self.queue(queue).put(Task(length, data))

    def exist_task(self, queue, id):
        if id in self.queue(queue):
            return 'YES'
        else:
            return 'NO'

    def get_task(self, queue):
        return self.queue(queue).get()

    def ask_task(self, queue, id):
        return self.queue(queue).task_done(id)

    def run(self):
        self.connection.listen(10)
        while True:
            current_connection, address = self.connection.accept()
            while True:
                data = current_connection.recv(1000000)
                response = ''
                if not data:
                    break

                data = data.decode("utf-8")
                command, *params = data.split(" ")
                print('command: ' + command)
                print(params)

                if command == 'ADD':
                    response = self.add_task(*params)

                elif command == 'GET':
                    response = self.get_task(*params)

                elif command == 'ACK':
                    response = self.ask_task(*params)

                elif command == 'IN':
                    response = self.exist_task(*params)

                elif command == 'SAVE':
                    break
                else:
                    response = 'ERROR'

                print('response: ' + response)
                current_connection.send(response.encode('utf-8'))
            current_connection.close()


class Task:
    count_of_instance = 0

    def __init__(self, length, data):
        Task.count_of_instance += 1
        self.id = str(Task.count_of_instance)
        print('\tdata: ' + data)
        self.data = data
        self.length = length
        self.at_work = False
        

class TaskQueue:
    def __init__(self, name):
        self.name = name
        self.queue = []
        self.at_work_queue = []
        self.done_task_ids = []

    def __contains__(self, item):
        return item in [task.id for task in self.queue]

    def put(self, task: Task):
        self.queue.append(task)
        return task.id

    def get(self):
        task = None
        for q_task in self.queue:
            if q_task.at_work:
                continue
            else:
                task = q_task
                break
        task.at_work = True
        self.at_work_queue.append(task)
        # Запустить счетчик таймаута выполнения задания
        return task.id + ' ' + task.length + ' ' + task.data
        # self.queue.pop(0)

    def task_done(self, id):
        response = 'NO'
        for task in self.at_work_queue:
            if id == task.id:
                response = 'YES'
                self.queue.remove(task)
                self.at_work_queue.remove(task)
                self.done_task_ids.append(task.id)
                break
        return response

    # def task_complete(self, id):
    #     return id in self.done_task_ids


class TaskQueuePool:
    def __init__(self):
        self._task_queues = {}

    def get(self, name):
        if name not in self._task_queues.keys():
            self._task_queues[name] = TaskQueue(name)
        return self._task_queues[name]


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
