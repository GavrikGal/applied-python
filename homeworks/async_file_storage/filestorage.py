import aiohttp
import asyncio
import yaml
from aiohttp import web
import logging
import os


logging.basicConfig(level=logging.INFO)


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

    async def get_file(self, file_name) -> 'file_data':
        data = await self.find_local(file_name)
        if data is not None and data != self.FILE_NOT_FOUND:
            return data
        else:
            results = await self.find_remote(file_name)
            if results is not None:
                for result in results:
                    if result is not None and result != self.FILE_NOT_FOUND:
                        return result
            else:
                return self.FILE_NOT_FOUND

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
