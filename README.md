# socketio-async-client-example

I can't figure how to properly shut down AsyncClient. Everything I've tried with no luck.
I always get this warning:

```
C:\async-client\venv\lib\site-packages\engineio\asyncio_client.py:206:\
   RuntimeWarning: coroutine 'ClientSession.close' was never awaited
ERROR - asyncio - Unclosed client session
client_session: <aiohttp.client.ClientSession object at 0x000000FF462BC588>
```

My code for client is endless loop because I need to use AsyncClient with other asyncio code which do other operations. So I extracted the code related to socketio into working example and publish it here:

https://github.com/bialix/socketio-async-client-example

There are 2 files: client-example.py and client-example2.py. The former is simple code, the latter trying to catch Ctrl+C signal and do graceful shutdown based on the examples I found on the internet. No matter what I've tried I can't get rid of aiohttp.client.ClientSession warning.

I need help, please.
