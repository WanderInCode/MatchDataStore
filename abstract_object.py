class AbstractTask:

    def set_queue(self, queue):
        raise NotImplemented
    
    async def run(self):
        raise NotImplemented