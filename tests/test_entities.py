import sqlalchemy as db
from entities import User, Room, Invitation
from sqlalchemy.orm import sessionmaker


def test_1():
    engine = db.create_engine('sqlite:///../chat.db', echo=False)

    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(User).filter(User.nickname.in_(['alice', 'bob'])).delete()

    alice = User(nickname="alice")
    bob = User(nickname="bob")

    session.add(alice)
    session.add(bob)

    session.commit()

    session.query(Room).filter_by(name="测试房间").delete()

    room = Room(name="测试房间")
    session.add(room)

    session.commit()

    #user.join(room)
    print(room.members)

    alice.join(room)
    session.commit()
    print("alice join", room.members)

    alice.leave(room)
    session.commit()
    print("alice leave", room.members)

    print("members", room.members)
    print("messages", room.messages)

    alice.join(room)
    bob.join(room)
    session.commit()

    alice.say(room, "hello from alice")
    bob.say(room, "hello from bob")
    session.commit()

    print("messages", room.messages)


def test_invitations():
    engine = db.create_engine('sqlite:///../chat.db', echo=False)

    Session = sessionmaker(bind=engine)
    session = Session()

    inv = Invitation()

