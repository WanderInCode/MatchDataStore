import asyncio
import uvloop
import aiomysql
import sqlalchemy


async def main(loop):
    pass

if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
