class Client:
    def __init__(self):
        self.stop = False
        self.sio = socketio.AsyncClient()

    async def main(self):
        while not self.stop:
            try:
                await self.sio.connect("http://127.0.0.1:10069")
                await self.sio.wait()
            except socketio.exceptions.ConnectionError:
                await asyncio.sleep(0.1)

def main():
    k = Client()
    loop = asyncio.get_event_loop()
    try:
        group = asyncio.gather(k.main(), other_async_code)
        loop.run_until_complete(group)
    finally:
        loop.close()

if __name__ == "__main__":
    sys.exit(main())
