import datetime
import sqlalchemy as sa
from  sqlalchemy import orm
from superpass.data.modelbase import SqlAlchemyBase

class Password(SqlAlchemyBase):
    __tablename__ = "passwords"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    last_updated_data = sa.Column(sa.DateTime, default=datetime.datetime.now)
    url = sa.Column(sa.String(256))
    username = sa.Column(sa.String(256))
    password = sa.Column(sa.String(256))
    
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    user = orm.relation('User')

    def __repr__(self):
        return f'<Password {self.url}: {self.username} / {"*" * len(self.password)}>'


    def get_dict(self):
        return {"url": self.url, "username": self.username, "password": self.password}