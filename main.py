import aiohttp
from aiohttp import web
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from entities import User, AccessToken, RefreshToken
import logging
import sys
import ssl

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

engine = sa.create_engine('sqlite:///chat.db', echo=False)

Session = sessionmaker(bind=engine)
session = Session()


def get_authenticated_user(access_token):
    return None

def auth_middleware_factory():
    @web.middleware
    async def auth_middleware(request: web.Request, handler):
        if "pubkey" in request.cookies:
            request.user = request.cookies["pubkey"]
        else:
            request.user = None
        return await handler(request)
    return auth_middleware


app = web.Application(
    middlewares=[
        auth_middleware_factory()
    ],
)


users = {

}


async def websocket_handler(request):
    user = request.user
    if not user:
        return web.HTTPForbidden()

    logging.info("[%s] Connected", user)

    ws = web.WebSocketResponse()

    users[user] = ws

    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.BINARY:
            data = msg.data
            # decode data
            # chunk type, routing, payload, room
            logging.info("[%s] --> %r", user, data)

            dead_users = []
            for pubkey, u in users.items():
                if u != ws:
                    try:
                        await u.send(data)
                    except:
                        dead_users.append(pubkey)
            for u in dead_users:
                users.pop(u, None)

    logging.info("[%s] Disconnected", user)
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


async def join_handler():
    pass


async def chunk_handler():
    pass


app.add_routes([
    web.get('/hello', hello),
    web.get('/ws', websocket_handler),
    web.get('/join', join_handler),
    web.get('/chunks', chunk_handler),
    web.get("/history", history_handler),
])

# ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
# ctx.load_cert_chain('/Users/yy/tmp/example.com.pem', '/Users/yy/tmp/example.com-key.pem')


# web.run_app(app, ssl_context=ctx)

web.run_app(app)
