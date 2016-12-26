import asyncio
from asyncio import Queue

import uvloop
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
import reponse_processing
import tables
import utils
from tasks import DelayStoreTask, InitTask


def make_engine():
    engine = create_engine(config.CONNECT_STRING, echo=True)
    return engine


def create_session_maker(engine):
    Session = sessionmaker(bind=engine)
    return Session


def create_all_tables(engine):
    Base = tables.Base
    Base.metadata.create_all(engine)

async def main(loop):
    engine = make_engine()
    utils.Utils.set_session_make(create_session_maker(engine))
    create_all_tables(engine)
    queue = Queue(loop=loop)
    init = InitTask(config.team_url, reponse_processing.handle_team_reponse)
    init.set_queue(queue)
    queue.put_nowait(init)
    while True:
        try:
            task = await queue.get()
            if queue.empty() and isinstance(task, DelayStoreTask):
                task.immediate_run()
                break
            else:
                await task.run()
        except Exception as e:
            print('Some error has happened!')
            return


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.ensure_future(main(loop)))
