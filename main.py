import aiohttp
from aiohttp import web
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from entities import User, AccessToken, RefreshToken

engine = sa.create_engine('sqlite:///chat.db', echo=False)

Session = sessionmaker(bind=engine)
session = Session()


def get_authenticated_user(access_token):
    return None

def auth_middleware_factory():
    @web.middleware
    async def auth_middleware(request, handler):
        access_token = request.headers.get("Authorization").replace("Bearer ", "")
        user = get_authenticated_user(access_token)
        if user:
            resp = await handler(user, request)
        else:
            resp = await handler(request)
        return resp
    return auth_middleware


app = web.Application(
    middlewares=[
        auth_middleware_factory()
    ]
)


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


async def history_handler(request):
    return web.json_response([

    ])


def invalid_invitation(code):
    return False


async def reception_handler(request):
    body = request.json()
    code = body["invitation_code"]
    pubkey = body["pubkey"]
    nickname = body["nickname"]
    # return access_token, refresh_token

    # make sure the invitation is valid
    if invalid_invitation(code):
        return web.json_response({
            "message": "invalid invitation code: " + code
        }, status=400)

    user = User(nickname=nickname, pubkey=pubkey)
    session.add(user)

    access_token = AccessToken(token="YOUR_ACCESS_TOKEN")
    refresh_token = RefreshToken(token="YOUR_REFRESH_TOKEN")

    return web.json_response({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "issued_at": 1620297592,
    })


async def reception_challenge_handler(request):
    pass


def is_valid_access_token(token):
    return True


async def update_nickname(user, request):
    session.begin()

    nickname = await request.json()
    if isinstance(nickname, str):
        user.nickname = nickname

    session.commit()



app.add_routes([
    web.get('/hello', hello),
    web.get('/ws', websocket_handler),
    web.get("/history", history_handler),
    web.post("/token", reception_handler),
    web.put("/nickname", update_nickname),
])

web.run_app(app)
