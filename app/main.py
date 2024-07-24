from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import *
import datetime
from fastapi import HTTPException, Depends
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from scripts.FacebookAPI import FacebookAPI
from scripts.GoogleSpreadSheet import GoogleSpreadSheet
from app.config import MARKETING_API_ACCESS_TOKEN, APP_ID, APP_SECRET, PROXIE, BUSINESS_MANAGER_ID
from sqlalchemy.orm import Session
from database import Base, engine, init_db, get_session
from models import Tables, Accounts, AccountFields, CampaignFields, AdsFields
from functools import partial

app = FastAPI(
    title="facebook-advertising-campaigns",
)

proxie = PROXIE
google_client = GoogleSpreadSheet("../scripts/service_secret.json")
scheduler = BackgroundScheduler()
# existing_url="https://docs.google.com/spreadsheets/d/1xKm-XNUU2EdQL9AiYDzTPc-M2vZ4xXV9arSbSMB2rK8/edit?usp=sharing"

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def periodic_task(api, url, account_fields, campaign_fields, ad_fields, time_range):
    print(f"Запущен сбор статистики с {time_range['since']} по {time_range['until']} по ссылке {url}")
    sheets = api.get_advertising_campaign(account_fields, campaign_fields, ad_fields, time_range=time_range)
    google_client.write_to_google_sheets(df_dict=sheets, spreadsheet_url=url)


def start_task(account_id,
               name,
               interval_in_minutes: int,
               api: FacebookAPI,
               url: str,
               account_fields,
               campaign_fields,
               ad_fields,
               time_range):
    scheduler.add_job(
        partial(periodic_task,
                api=api,
                url=url,
                account_fields=account_fields,
                campaign_fields=campaign_fields,
                ad_fields=ad_fields,
                time_range=time_range),
        trigger=IntervalTrigger(minutes=interval_in_minutes),
        id=str(account_id),
        name=name,
        replace_existing=True,
    )


@app.post("/start_insights")
def start_insights(account_id: int, emails: List[str], date_start: datetime.date, date_end: datetime.date,
                   interval_in_minutes: int,
                   spreadsheet_url: str = None,
                   account_fields: Optional[List[AccountFields]] = Query(None),
                   ad_fields: Optional[List[AdsFields]] = Query(None),
                   campaign_fields: Optional[List[CampaignFields]] = Query(None),
                   db: Session = Depends(get_session)):
    try:
        obj = db.query(Accounts).filter(Accounts.id == account_id).first()
        if not obj:
            raise HTTPException(status_code=404, detail="Объект не найден")

        # запрошенные поля
        account_fields = [x.value for x in account_fields]
        ad_fields = [x.value for x in ad_fields]
        campaign_fields = [x.value for x in campaign_fields]

        # собираем api
        api = FacebookAPI(obj.marketing_api_access_token,
                          obj.app_id,
                          obj.app_secret,
                          obj.business_manager_id,
                          proxie)

        time_range = {'since': date_start.strftime("%Y-%m-%d"),
                      'until': date_end.strftime("%Y-%m-%d")}

        # если таблица не задана, то создаем новую
        if spreadsheet_url is None:
            spreadsheet_url = google_client.create_spreadsheet(emails,
                                                               spreadsheet_name=f"campaign_data_{time_range['since']}_{time_range['until']}")
        values = {'url': spreadsheet_url}
        # добавляем ссылку на таблицу в БД
        stmt = insert(Tables).values(values)
        db.execute(stmt)
        db.commit()

        # запускаем по получение данных по интервалу
        start_task(account_id=account_id,
                   name=f"campaign_data_{time_range['since']}_{time_range['until']}",
                   interval_in_minutes=interval_in_minutes,
                   api=api,
                   url=spreadsheet_url,
                   account_fields=account_fields,
                   campaign_fields=campaign_fields,
                   ad_fields=ad_fields,
                   time_range=time_range)

        return {"status": "success",
                "message": "Периодическая задача запущена"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка базы данных {str(e)}")


@app.post("/stop_insights")
def stop_periodic_task(account_id: int):
    scheduler.remove_job(str(account_id))
    return {"message": "Периодическая задача остановлена"}


@app.post("/add_account")
def add_account(marketing_api_access_token: str, app_id: str, app_secret: str, business_manager_id: str,
                db: Session = Depends(get_session)):
    try:
        values = {
            'marketing_api_access_token': marketing_api_access_token,
            'app_id': app_id,
            'app_secret': app_secret,
            'business_manager_id': business_manager_id,
        }

        stmt = insert(Accounts).values(values)
        db.execute(stmt)
        db.commit()
        return {"status": "success"}

    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/get_accounts")
def get_accounts(db: Session = Depends(get_session)):
    try:
        accounts = db.query(Accounts).all()
        if not accounts:
            raise HTTPException(status_code=404, detail="Записи не найдены")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Ошибка базы данных")

    return {"status": "success",
            "data": accounts}


if __name__ == "__main__":
    init_db()
    scheduler.start()
    try:
        connection = engine.connect()
        print("Соединение с базой данных установлено")
        connection.close()
    except Exception as e:
        print(f"Ошибка соединения с базой данных: {e}")

    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
