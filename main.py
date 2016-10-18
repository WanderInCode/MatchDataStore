import asyncio
import aiomysql
import sqlalchemy


async def main(loop):
    engine = await aiomysql.sa.create_engine(user='dota', db='dota', host='127.0.0.1',
                                             password='123456', loop=loop)
    pass

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
