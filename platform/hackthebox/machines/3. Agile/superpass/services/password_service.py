import csv
import datetime
import sqlalchemy as sa
import superpass.data.db_session as db_session
from superpass.data.password import Password
from superpass.data.user import User
from superpass.services.utility_service import get_random
from typing import Optional

def get_passwords_for_user(userid: int):

    session = db_session.create_session()
    user = session.query(User) \
        .options(sa.orm.joinedload(User.passwords))\
        .filter(User.id == userid) \
        .first()

    session.close()

    return user.passwords


def get_password_by_id(id: int, userid: int) -> Optional[Password]:

    session = db_session.create_session()
    password = session.query(Password)\
        .filter(
            Password.id == id,
            User.id == userid
        ).first()

    session.close()

    return password


def add_password(site, username, password, userid):

    p = Password(url=site, username=username, password=password, user_id=userid)

    session = db_session.create_session()
    session.add(p)
    session.commit()
    session.close()

    return p


def delete_password(id):

    session = db_session.create_session()
    p = session.query(Password).filter(Password.id == id).first()
    session.delete(p)
    session.commit()
    session.close()


def update_password(id, site, username, password):

    session = db_session.create_session()
    p = session.query(Password).filter(Password.id == id).first()
    p.url = site
    p.username = username
    p.password = password
    p.last_updated = datetime.datetime.now()
    session.add(p)
    session.commit()
    session.close()

    return p


def generate_csv(user):

    rand = get_random(10)
    fn = f'{user.username}_export_{rand}.csv'
    path = f'/tmp/{fn}'

    header = ['Site', 'Username', 'Password']
    
    session = db_session.create_session()
    passwords = session.query(Password) \
        .filter(Password.user_id == user.id) \
        .all()
    session.close()

    with open(path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows((p.get_dict().values() for p in passwords))
 
    return fn
