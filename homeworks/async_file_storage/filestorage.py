import aiohttp
import asyncio
import yaml
from aiohttp import web
import logging
import os
import threading
import time


logging.basicConfig(level=logging.ERROR)


class Node:
    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = port


class FileStorage:
    FILE_NOT_FOUND = b'Not Found'

    def __init__(self, config_path):
        with open(config_path) as conf:
            self.config = yaml.safe_load(conf)
        self.name = self.config['name']
        self.nodes = [Node(node['name'], node['host'], node['port'])
                      for node
                      in self.config['nodes']]
        self.app = web.Application()
        self.app.router.add_route(path='/{file_name}',
                                  handler=self.main_handler,
                                  method='get')
        self.app.router.add_route(path='/node/{file_name}',
                                  handler=self.node_handler,
                                  method='get')

    def run(self):
        web.run_app(self.app, port=self.config['port'])

    async def node_handler(self, request):
        file_name = request.match_info.get('file_name')
        if file_name:
            if file_name == 'favicon.ico':
                pass
            else:
                data = await self.find_local(file_name)
                if data:
                    return await self.prepare_response(request, data, file_name)
                else:
                    return self.FILE_NOT_FOUND
        else:
            return aiohttp.web.HTTPBadRequest()

    async def main_handler(self, request):
        file_name = request.match_info.get('file_name')
        if file_name:
            if file_name == 'favicon.ico':
                pass
            else:
                data = await self.get_file(file_name)
                if data is not None and data != self.FILE_NOT_FOUND:

                    return await self.prepare_response(request, data, file_name)
                else:
                    return aiohttp.web.HTTPFound('/')
        else:
            return aiohttp.web.HTTPFound('Введите имя файла для поиска')     # Возможно хрень!!

    @staticmethod
    async def prepare_response(request, data, file_name) -> 'response':
        response = web.StreamResponse(headers={'CONTENT-DISCRIPTION': 'attachment; filename="{}"'.format(file_name), })
        response.content_type = 'text/txt'
        await response.prepare(request)
        await response.write(data)
        return response

    def cash_file(self, file_name, data):
        self.save_file(file_name, data)
        if self.config['clear_tmp_file_time']:
            self.delete_after_timeout(file_name, self.config['clear_tmp_file_time'])

    def delete_after_timeout(self, file_name, timeout):
        def delete(file_name):
            time.sleep(timeout)
            try:
                os.remove(self.config['path'] + file_name)
            except Exception as err:
                print(str(err))
        thread = threading.Thread(target=delete, args=(file_name,))
        thread.start()

    def save_file(self, file_name, data):
        def save(file_name, data):
            try:
                with open(self.config['path'] + file_name, 'wb') as file:
                    file.write(data)
            except Exception as err:
                print(str(err))
        thread = threading.Thread(target=save, args=(file_name, data))
        thread.start()

    async def get_file(self, file_name) -> 'file_data':
        data = await self.find_local(file_name)
        remote_result = self.FILE_NOT_FOUND
        if data is not None and data != self.FILE_NOT_FOUND:
            return data
        else:
            results = await self.find_remote(file_name)
            if results is not None:
                for result in results:
                    if result is not None and result != self.FILE_NOT_FOUND:
                        remote_result = result
            else:
                return self.FILE_NOT_FOUND
        if remote_result is not None and remote_result != self.FILE_NOT_FOUND:
            if self.config['save_file']:
                self.cash_file(file_name, remote_result)
        return remote_result

    async def find_remote(self, file_name):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for node in self.nodes:
                task = asyncio.create_task(
                    self.fetch_content('http://{}:{}/node/{}'.format(node.host, node.port, file_name), session))
                tasks.append(task)
            return await asyncio.gather(*tasks)

    @staticmethod
    async def fetch_content(url, session):
        async with session.get(url, allow_redirects=True) as response:
            return await response.read()

    async def find_local(self, file_name) -> 'file_data':
        try:
            if os.path.exists(self.config['path'] + file_name):
                with open(self.config['path'] + file_name, 'rb') as f:
                    return f.read()
            else:
                return self.FILE_NOT_FOUND
        except Exception as err:
            logging.exception(str(err))
