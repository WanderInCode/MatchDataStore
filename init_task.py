import logging

import abstract_object
import aiohttp
from task_exception import TaskException


class InitTask(abstract_object.AbstractTask):

    def __init__(self, url, fn):
        self.url = url
        self.handle_response = fn
        logging.basicConfig(
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S')
        self._logger = logging.getLogger()

    def set_queue(self, queue):
        self.queue = queue

    async def run(self):
        async with aiohttp.request('GET', url) as resp:
            try:
                await resp_data = resp.json()
                tasks = self.handle_response(resp_data)
                async for task in tasks:
                    await self.queue.put(tasks)
            except TaskException as e:
                self._logger.error(e.message)
                await self.queue.put(None)
            except Exception as e:
                self._logger.error(e.message)
                await self.queue.put(None)
