import asyncio
import random

import aiohttp
from sqlalchemy.exc import DBAPIError

import utils
from task_exception import TaskError


class AbstractTask:

    def __init__(self):
        self._logger = utils.logger

    def set_queue(self, queue):
        self._queue = queue

    def get_queue(self):
        return self._queue

    async def enqueue(self):
        if not getattr(self, '_queue', None):
            raise AttributeError('queue is not set!')
        await self._queue.put(self)

    def run(self):
        raise NotImplemented


class InitTask(AbstractTask):

    def __init__(self, url, fn):
        AbstractTask.__init__(self)
        self.url = url
        self.handle_response = fn

    async def run(self):
        self._logger.info('InitTask: {}'.format(self.url))
        await asyncio.sleep(0.5 + random.random() / 2)
        async with aiohttp.request('GET', url) as resp:
            try:
                resp_data = await resp.json()
                tasks = self.handle_response(resp_data)
                async for task in tasks:
                    task.set_queue(self.get_queue())
                    await task.enqueue()
                return len(tasks)
            except TaskError as e:
                self._logger.error(e)
                raise


class AcquisitionTask(AbstractTask):

    def __init__(self, urls, fn):
        AbstractTask.__init__(self)
        self.urls = urls
        self.handle_response = fn

    async def run(self):
        task_length = 0
        async for url in self.urls:
            self._logger.info('AcquisitionTask: {}'.format(url))
            await asyncio.sleep(0.5 + random.random() / 2)
            async with aiohttp.request('GET', url) as resp:
                try:
                    resp_data = await resp.json()
                    tasks = self.handle_response(resp_data)
                    task_length += len(tasks)
                    async for task in tasks:
                        task.set_queue(self.get_queue())
                        await task.enqueue()
                except TaskError as e:
                    self._logger.error(e.args)
                    raise
        return task_length


class DelayAcquisitionTask(AbstractTask):
    pass


class StoreTask(AbstractTask):

    def __init__(self):
        AbstractTask.__init__(self)


class ImmediateStoreTask(StoreTask):

    def __init__(self, data_list, Session):
        StoreTask.__init__(self)
        self._data_list = data_list
        self._Session = Session

    def run(self):
        self._logger.info(
            'ImmediateStoreTask: store {} tables'.format(len(self._data_list)))
        session = self._Session()
        try:
            session.add_all(self._data_list)
            session.commit()
            return 0
        except DBAPIError as e:
            session.rollback()
            self._logger.error(e)
            raise
        finally:
            session.close()


class DelayStoreTask(StoreTask):

    _store = dict()
    _queue = None
    _in_queue = False

    def __init__(self, store_type, data_list, Session):
        StoreTask.__init__(self)
        self._set_store(store_type, data_list)
        self._store_type = store_type
        self._Session = Session

    async def enqueue(self):
        if self.__class__._in_queue:
            return
        else:
            await StoreTask.enqueue(self)
            self.__class__._in_queue = True

    @classmethod
    def set_queue(cls, queue):
        cls._queue = queue

    @classmethod
    def _set_store(cls, store_type, data_list):
        store = cls._store.get(store_type)
        if not store:
            store = dict()
            cls._store[store_type] = store
        for item in data_list:
            store_key = item.__tablename__
            if not store.get(store_key):
                store[store_key] = list()
            store[store_key].append(item)

    @classmethod
    def add_store(cls, store_type, data_list):
        cls._set_store(store_type, data_list)

    def _clear_store(self):
        self.__class__._store[self._store_type].clear()

    def _get_store_list(self):
        store = self.__class__._store[self._store_type]
        store_list = list()
        for k, v in store.items():
            store_list.extend(v)
        return store_list

    async def run(self):
        store_list = self._get_store_list()
        if len(store_list) == 0:
            return 0
        elif len(store_list) >= 20:
            self._logger.info(
                'DelayStoreTask: store {} tables'.format(len(store_list)))
            session = self._Session()
            try:
                session.add_all(store_list)
                session.commit()
                self._clear_store()
                return 0
            except DBAPIError as e:
                session.rollback()
                self._logger.error(e)
                raise
            finally:
                session.close()
        else:
            await self.enqueue()
            return 0
