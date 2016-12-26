# MatchDataStore

使用 Steam Api 获取 Dota 比赛数据。

每个 http 请求包裹在一个 Task 类中，放入 asyncio 队列， http 请求通过 aiohttp 模块发起

Python 3.5可用。