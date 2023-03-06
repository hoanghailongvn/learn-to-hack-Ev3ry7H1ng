from typing import Optional
from superpass.data.user import User
from superpass.data import db_session
from passlib.handlers.sha2_crypt import sha512_crypt as hasher

def create_user(username: str, password: str) -> Optional[User]:

    if get_user_by_name(username):
        return None

    user = User()
    user.username = username
    user.hashed_password = hasher.encrypt(password, rounds=200000)

    session = db_session.create_session()
    session.add(user)
    session.commit()
    session.close()
    
    return user


def login_user(username: str, password: str) -> Optional[User]:
    session = db_session.create_session()
    user = session.query(User).filter(User.username == username).first()

    if user and hasher.verify(password, user.hashed_password):
        session.close()
        return user
    session.close()
    return None


def get_user_by_name(username: str) -> Optional[User]:
    session = db_session.create_session()
    tmp = session.query(User).filter(User.username == username).first()
    session.close()
    return tmp


def get_user_by_id(uid: int) -> Optional[User]:
    session = db_session.create_session()
    tmp = session.query(User).filter(User.id == uid).first()
    session.close()
    return tmp
