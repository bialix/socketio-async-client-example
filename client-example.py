import asyncio
import logging
import sys

import socketio
import socketio.exceptions


logging.basicConfig(stream=sys.stdout, format="%(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger("main")
logger.setLevel("DEBUG")


class Client:
    def __init__(
        self,
        *,
        url: str = "http://127.0.0.1:10069",
        reconnect_timeout: float = 1,
    ):
        self.stop = False
        self.is_connected = None
        self.url = url
        self.reconnect_timeout = reconnect_timeout
        #
        self.sio = socketio.AsyncClient(
            logger=logging.getLogger("socketio"),
            engineio_logger=logging.getLogger("engineio"),
            reconnection_delay=reconnect_timeout,
        )
        self.sio.on("connect", self.on_connect)
        self.sio.on("connect_error", self.on_connect_error)
        self.sio.on("disconnect", self.on_disconnect)
        self.sio.on("answer", self.on_message)

    async def main(self):
        while not self.stop:
            try:
                logger.debug("trying to connect")
                await self.sio.connect(self.url)
                await self.sio.wait()
            except socketio.exceptions.ConnectionError:
                if self.stop:
                    break
                if self.reconnect_timeout:
                    await asyncio.sleep(self.reconnect_timeout)
                continue

    async def on_connect(self):
        logger.debug("connection established")
        self.is_connected = True
        message = {"foo": "bar"}
        logger.debug("send > %r", message)
        await self.sio.emit("cmd", message)

    async def on_message(self, data):
        logger.debug("recv < %r", data)

    async def on_disconnect(self):
        logger.debug("disconnected from server")
        self.is_connected = False

    async def on_connect_error(self, data):
        if self.is_connected != False:
            logger.warning("Connect error: %s", data)
        self.is_connected = False


def main():
    k = Client()

    loop = asyncio.get_event_loop()
    # loop.set_debug(True)

    try:
        group = asyncio.gather(
            k.main(),
        )
        loop.run_until_complete(group)
    except asyncio.CancelledError as e:
        logger.debug(e)
    finally:
        logger.debug("stopped")
        loop.close()


if __name__ == "__main__":
    sys.exit(main())
