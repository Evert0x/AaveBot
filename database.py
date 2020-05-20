from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, String, Sequence, Boolean, DateTime, \
    Integer, desc, and_
from sqlalchemy import create_engine, Table, MetaData, ForeignKey, text, bindparam, TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from telegram import Bot
import settings

Base = declarative_base()
engine = create_engine('sqlite:///meme.db')
Session = sessionmaker(bind=engine)

class TxCall(Base):
    __tablename__ = "txcalls"

    code = Column(String(32), primary_key=True)
    userid = Column(String(64), nullable=False)
    address = Column(String(64), nullable=False)
    msg_id = Column(Integer, nullable=False)

    @staticmethod
    def insert(s, code, userid, address, msg_id):
        x = TxCall(
            code=code,
            userid=userid,
            address=address,
            msg_id=msg_id
        )
        s.add(x)
        return x

    @staticmethod
    def get(s, code):
        return s.query(TxCall).filter(TxCall.code == code).first()

class HealthNotification(Base):
    __tablename__ = "health_notification"

    userid = Column(String(64), primary_key=True)
    address = Column(String(64), nullable=False)
    factor = Column(Integer, nullable=False)

    @staticmethod
    def get(s, userid):
        return s.query(HealthNotification).filter(HealthNotification.userid==userid).first()

    @staticmethod
    def get_all(s):
        return s.query(HealthNotification).all()

    @staticmethod
    def upsert(s, userid, address, factor):
        data = s.query(HealthNotification).\
            filter(HealthNotification.userid==userid).\
            first()

        if data:
            data.factor = factor
        else:
            s.add(HealthNotification(
                userid=userid,
                address=address,
                factor=factor
            ))

if __name__ == '__main__':
    Base.metadata.create_all(engine)