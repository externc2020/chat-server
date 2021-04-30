import aiohttp
from aiohttp import web


app = web.Application()


users = set()


async def websocket_handler(request):
    print("connected")
    ws = web.WebSocketResponse()

    users.add(ws)

    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'exit':
                await ws.close()
                users.remove(ws)
            else:
                print(msg.data)
                dead_users = []
                for u in users:
                    if u != ws:
                        try:
                            await u.send_str(msg.data)
                        except:
                            dead_users.append(u)
                for u in dead_users:
                    users.remove(u)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' % ws.exception())

    print('websocket connection closed')
    return ws


async def hello(request):
    return web.Response(text="Hello")


app.add_routes([
    web.get('/hello', hello),
    web.get('/ws', websocket_handler),
])

web.run_app(app)
