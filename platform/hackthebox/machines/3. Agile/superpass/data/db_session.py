import sqlalchemy as sa
import sqlalchemy.orm as orm
from superpass.data.modelbase import SqlAlchemyBase

__factory = None


def global_init(db_uri: str):
    global __factory

    if __factory:
        return

    if not db_uri or not db_uri.strip():
        raise Exception("You must specify a db string")

    engine = sa.create_engine(db_uri, echo=False)

    __factory = orm.sessionmaker(bind=engine)

    import superpass.data.__all_models
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> orm.Session:
    global __factory
    session = __factory()
    session.expire_on_commit = False
    return session