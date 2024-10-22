from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=0.0)
    vpn_config = Column(String, nullable=True)
    subscription_expiration = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=False)
    vpn_config_created = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, balance={self.balance}, is_active={self.is_active})>"


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def create_database():
    """Создаем таблицы в базе данных"""
    Base.metadata.create_all(engine)


def add_user(telegram_id):
    """Добавляем нового пользователя в базу"""
    new_user = User(telegram_id=str(telegram_id))
    session.add(new_user)
    session.commit()


def get_user_by_telegram_id(telegram_id):
    """Получаем пользователя по Telegram ID"""
    return session.query(User).filter_by(telegram_id=str(telegram_id)).first()


def update_vpn_config_created(user):
    """Обновляем статус создания VPN-конфига для пользователя"""
    user.vpn_config_created = True
    session.commit()
