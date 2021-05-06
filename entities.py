from sqlalchemy.orm import declarative_base
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship


Base = declarative_base()


room_members = Table(
    'room_members', Base.metadata,
    Column('room_id', Integer, ForeignKey('rooms.id')),
    Column('user_id', Integer, ForeignKey('users.id')),
)

user_friends = Table(
    'user_friends', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('friend_id', Integer, ForeignKey('users.id')),
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    rooms = relationship('Room', secondary=room_members)
    # friends = relationship('User', secondary=user_friends)

    def join(self, room):
        room.members.append(self)

    def leave(self, room):
        room.members.remove(self)

    def say(self, room, content):
        if self not in room.members:
            print("not in", room)
            return

        m = Message(content=content)
        m.user = self
        m.room = room

        room.messages.append(m)


class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    messages = relationship("Message")
    members = relationship("User", secondary=room_members)


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    room = relationship("Room")
    user = relationship("User")


class Invitation(Base):
    __tablename__ = "invatations"
    id = Column(Integer, primary_key=True)
    code = Column(String)
    user = relationship("User")
    expired_at = DateTime()
    count = Column(Integer)
    disabled = Column(Boolean)


class AccessToken(Base):
    __tablename__ = "access_tokens"
    id = Column(Integer, primary_key=True)
    token = Column(String)
    user = relationship("User")
    expired_at = DateTime()
    disabled = Column(Boolean)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True)
    token = Column(String)
    user = relationship("User")
    expired_at = DateTime()
    disabled = Column(Boolean)
