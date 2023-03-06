from flask_login import UserMixin
import sqlalchemy as sa
from  sqlalchemy import orm
from typing import List
from superpass.services import password_service
from superpass.data.modelbase import SqlAlchemyBase
from superpass.data.password import Password


class User(UserMixin, SqlAlchemyBase):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    username = sa.Column(sa.String(256), nullable=False)
    hashed_password = sa.Column(sa.String(256), nullable=False)
    
    passwords: List[Password] = orm.relation("Password", back_populates='user')
    

    def __repr__(self):
        return f'<User {self.username}>'

    
    @property
    def has_passwords(self):
        return len(password_service.get_passwords_for_user(self.id)) > 0
