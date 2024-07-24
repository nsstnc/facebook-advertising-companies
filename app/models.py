from sqlalchemy import Column, Integer, String
from database import Base


class Tables(Base):
    __tablename__ = 'tables'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)


class Accounts(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    marketing_api_access_token = Column(String, nullable=False)
    app_id = Column(String, nullable=False)
    app_secret = Column(String, nullable=False)
    business_manager_id = Column(String, nullable=False)
