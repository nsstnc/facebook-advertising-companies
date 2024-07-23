import json
from FacebookAPI import FacebookAPI
from config import MARKETING_API_ACCESS_TOKEN, APP_ID, APP_SECRET, PROXIE, BUSINESS_MANAGER_ID


proxie = PROXIE

token = MARKETING_API_ACCESS_TOKEN
app_id = APP_ID
app_secret = APP_SECRET
business_manager_id = BUSINESS_MANAGER_ID
time_range ={'since': '2024-01-01', 'until': '2024-07-22'}

api = FacebookAPI(token, app_id, app_secret, business_manager_id, proxie)

api.get_advertising_campaign(time_range=time_range)
