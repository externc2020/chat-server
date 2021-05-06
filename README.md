Sign your nickname

```
curl -X POST http://localhost:8080/api/token
{
    "pubkey": "your_pubkey",
    "signature": "..."
}
{
    "username": "admin",
    "password": "admin",
}
---
{
    "accessToken": "...",
    "refreshToken": "...",
    "issuedAt": "..."
}
```

List public rooms

```
curl -X GET http://localhost:8080/api/rooms \
-H 'Authorization: Bearer access_token'
---
[
    {"id": 1, "name": "room1"},
    {"id": 2, "name": "room2"}
]
```

Join the room

```
curl -X POST http://localhost:8080/api/rooms/1/join \
-H 'Authorization: Bearer access_token'
```

Leave the room

```
curl -X POST http://localhost:8080/api/rooms/1/leave \
-H 'Authorization: Bearer access_token'
```

Get historical messages of the room

```
curl -X GET http://localhost:8080/api/rooms/1/history?offset=0&size=10 \
-H 'Authorization: Bearer access_token'
```

Listen for new messages

```
wscat -c http://localhost:8080/ws
-> {"command": "login", "access_token": "..."}
-> {"command": "subscribe", "rooms": [1, 2]}
-> {"command": "unsubscribe", "rooms": [1, 2]}
<- {"room": 1, "user": 1, "message": "hello1"}
<- {"room": 2, "user": 2, "message": "hello2"}  
```