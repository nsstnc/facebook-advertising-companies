import json
from FacebookAPI import FacebookAPI
from GoogleSpreadSheet import GoogleSpreadSheet
from config import MARKETING_API_ACCESS_TOKEN, APP_ID, APP_SECRET, PROXIE, BUSINESS_MANAGER_ID

proxie = PROXIE
token = MARKETING_API_ACCESS_TOKEN
app_id = APP_ID
app_secret = APP_SECRET
business_manager_id = BUSINESS_MANAGER_ID
time_range = {'since': '2024-01-01', 'until': '2024-07-22'}

api = FacebookAPI(token, app_id, app_secret, business_manager_id, proxie)

google_client = GoogleSpreadSheet("service_secret.json")

sheets = api.get_advertising_campaign(time_range=time_range)

# existing_url="https://docs.google.com/spreadsheets/d/1xKm-XNUU2EdQL9AiYDzTPc-M2vZ4xXV9arSbSMB2rK8/edit?usp=sharing"

emails = ['egorgolubev0484@gmail.com']
spreadsheet_url = google_client.write_to_google_sheets(df_dict=sheets, emails=emails, spreadsheet_name=f"campaign_data_{time_range['since']}_{time_range['until']}")

print(f"Таблицы собраны и записаны в Google Sheets: {spreadsheet_url}")
