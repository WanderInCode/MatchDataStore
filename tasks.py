import logging
import aiohttp

from task_exception import TaskException


class AbstractTask:

    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S')
        self._logger = logging.getLogger()

    def set_queue(self, queue):
        raise NotImplemented

    async def run(self):
        raise NotImplemented


class InitTask(AbstractTask):

    def __init__(self, url, fn):
        AbstractTask.__init__(self)
        self.url = url
        self.handle_response = fn

    def set_queue(self, queue):
        self.queue = queue

    async def run(self):
        async with aiohttp.request('GET', url) as resp:
            try:
                resp_data = await resp.json()
                tasks = self.handle_response(resp_data)
                async for task in tasks:
                    await self.queue.put(tasks)
            except TaskException as e:
                self._logger.error(e.message)
                await self.queue.put(None)
            except Exception as e:
                self._logger.error(e.message)
                await self.queue.put(None)


class AcquisitionTask(AbstractTask):

    def __init__(self, url):
        AbstractTask.__init__(self)
        self.url = url

    def set_queue(self, queue):
        self.queue = queue

    async def run(self):
        async with aiohttp.request('GET', url) as resp:
            try:
                resp_data = await resp.json()
                # TODO
                pass
            except TaskException as e:
                self._logger.error(e.message)
                await self.queue.put(None)


class StoreTask(AbstractTask):

    store_list = []

    def __init__(self, engine):
        self.engine = engine
        pass
