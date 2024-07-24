from sqlalchemy import Column, Integer, String
from database import Base
import enum


class AdsFields(enum.Enum):
    account_id = 'account_id'
    account_name = 'account_name'
    campaign_id = 'campaign_id'
    campaign_name = 'campaign_name'
    ad_name = 'ad_name'
    ad_id = 'ad_id'
    impressions = 'impressions'
    clicks = 'clicks'
    cpm = 'cpm'
    spend = 'spend'
    account_currency = 'account_currency'
    ctr = 'ctr'
    created_time = 'created_time'
    date_start = 'date_start'
    date_stop = 'date_stop'


class CampaignFields(enum.Enum):
    id = 'id'
    name = 'name'
    status = 'status'
    budget_remaining = 'budget_remaining'
    start_time = 'start_time'
    stop_time = 'stop_time'


class AccountFields(enum.Enum):
    account_id = 'account_id'
    name = 'name'
    owner = 'owner'
    account_status = 'account_status'
    balance = 'balance'
    created_time = 'created_time'
    amount_spent = 'amount_spent'
    currency = 'currency'


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
