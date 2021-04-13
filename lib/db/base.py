from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.db.setup import Base, UserRole, UserAuth, UserSalt, UserLogin, UserInfo, TokenPerm


class DatabaseInstance:
    def __init__(self, db_host, db_name, db_user, db_pass):
        self.engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}')

        # Свяжим engine с метаданными класса Base,
        # чтобы декларативы могли получить доступ через экземпляр DBSession
        Base.metadata.bind = self.engine

        db_session = sessionmaker(bind=self.engine)
        # Экземпляр DBSession() отвечает за все обращения к базе данных
        # и представляет «промежуточную зону» для всех объектов,
        # загруженных в объект сессии базы данных.
        self.session = db_session()


def make_dict_result(result):
    json_res = result.__dict__
    del json_res['_sa_instance_state']
    return json_res
