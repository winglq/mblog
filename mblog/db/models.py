from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
db_engine = None
sql_session = None
db_file_path = "/var/lib/mblog/mblog.db"


def get_db_engine():
    global db_engine, db_file_path
    if db_engine is None:
        db_engine = create_engine("sqlite:///%s" % db_file_path, echo=False,
                                  connect_args={'check_same_thread': False})
    return db_engine


def get_session():
    global sql_session
    if sql_session is None:
        sql_session = sessionmaker(bind=get_db_engine())()
    return sql_session


class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    user = Column(String)
    code = Column(String)
    hold_position = Column(Integer)
    bid_price = Column(Float(precision=2))
    stop_loss_price = Column(Float(precision=2))
    selled = Column(Boolean)
    sell_price = Column(Float(precision=2))


if __name__ == "__main__":
    import os
    if not os.path.exists(db_file_path):
        Base.metadata.create_all(get_db_engine())
    s = Stock(code='123456', hold_position=600, bid_price=1.234,
              stop_loss_price=1.00, selled=False,
              user='qing')
    session = get_session()
    session.add(s)
    session.commit()
