import socket
import argparse
import pickle
from threading import Thread
import time
import os


DUMP_FILE_NAME = 'dump.tmp'


class TaskQueueServer:

    def __init__(self, ip, port, path, timeout):
        self.task_queue_pool = None
        try:
            if os.path.isfile(DUMP_FILE_NAME):
                with open(DUMP_FILE_NAME, 'br') as file:
                    dump = pickle.load(file)
                    self.task_queue_pool = dump
        except OSError:
            print('LOAD DUMP ERROR')
        if not self.task_queue_pool:
            self.task_queue_pool = TaskQueuePool()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connection.bind((ip, port))

    def queue_by_name(self, name):
        return self.task_queue_pool.get(name)

    def add_task(self, queue, length, data):
        return self.queue_by_name(queue).put(Task(length, data))

    def exist_task(self, queue, id):
        if id in self.queue_by_name(queue):
            return 'YES'
        else:
            return 'NO'

    def get_task(self, queue):
        return self.queue_by_name(queue).get()

    def ask_task(self, queue, id):
        return self.queue_by_name(queue).task_done(id)

    def clear_queues(self):
        self.task_queue_pool = None
        if os.path.isfile(DUMP_FILE_NAME):
            os.remove(DUMP_FILE_NAME)
        return 'CLEAR OK'

    def save_queues(self):
        try:
            with open(DUMP_FILE_NAME, 'bw') as file:
                pickle.dump(self.task_queue_pool, file)
                return 'OK'
        except OSError:
            return 'ERROR'

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

                if command == 'ADD':
                    response = self.add_task(*params)

                elif command == 'GET':
                    response = self.get_task(*params)

                elif command == 'ACK':
                    response = self.ask_task(*params)

                elif command == 'IN':
                    response = self.exist_task(*params)

                elif command == 'SAVE':
                    response = self.save_queues()

                elif command == 'CLEAR':
                    response = self.clear_queues()
                else:
                    response = 'ERROR'

                current_connection.send(response.encode('utf-8'))
            current_connection.close()


class Task:
    count_of_instance = 0

    def __init__(self, length, data):
        Task.count_of_instance += 1
        self.id = str(Task.count_of_instance)
        self.data = data
        self.length = length
        self.at_work = False


class TaskQueue:
    def __init__(self, name):
        self.name = name
        self.queue = []
        self.at_work_queue = []

    def __contains__(self, item):
        return item in [task.id for task in self.queue]

    @staticmethod
    def task_timer(queue, task):
        time.sleep(0.01*60)
        if task is None:
            pass
        else:
            task.at_work = False
            queue.at_work_queue.remove(task)

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
        if task is None:
            return 'QUEUE IS EMPTY'
        task.at_work = True
        self.at_work_queue.append(task)
        self.run_timer(task)    # Запустить счетчик таймаута выполнения задания
        return task.id + ' ' + task.length + ' ' + task.data

    def run_timer(self, task):
        thread = Thread(target=self.task_timer, args=(self, task))
        thread.start()

    def task_done(self, id):
        response = 'NO'
        for task in self.at_work_queue:
            if id == task.id:
                response = 'YES'
                self.queue.remove(task)
                self.at_work_queue.remove(task)
                break
        return response

    def task_at_work(self, task_id):
        return task_id in [task.id for task in self.at_work_queue]


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
