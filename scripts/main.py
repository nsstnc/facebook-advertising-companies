from script import *
import json

from config import MARKETING_API_ACCESS_TOKEN, APP_ID, APP_SECRET, PROXIE, BUSINESS_MANAGER_ID


proxie = PROXIE

token = MARKETING_API_ACCESS_TOKEN
app_id = APP_ID
app_secret = APP_SECRET
business_manager_id = BUSINESS_MANAGER_ID
time_range ={'since': '2024-01-01', 'until': '2024-07-22'}

print(get_advertising_campaign(my_access_token=token, my_app_id=app_id, my_app_secret=app_secret, business_manager_id=business_manager_id, time_range=time_range, proxies=proxie))
