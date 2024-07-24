import time
from facebook_business.adobjects.adreportrun import AdReportRun
from typing import *

from typing import Dict
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.user import User
from facebook_business.adobjects.business import Business
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business import FacebookSession
import datetime


class FacebookAPI:
    def __init__(self, my_access_token: str, my_app_id: str, my_app_secret: str, business_manager_id: str,
                 proxies: Dict[str, str] = None):
        session = FacebookSession(
            my_app_id,
            my_app_secret,
            my_access_token,
            proxies,
        )
        self.api = FacebookAdsApi(session)
        self.business = Business(fbid=business_manager_id, api=self.api)

    def get_insights(self, fields, params):
        all_insights = []
        my_accounts = self.business.get_client_ad_accounts()
        for account in my_accounts:
            account = AdAccount(fbid=account['id'], api=self.api)
            insights = account.get_insights(params=params, fields=fields)
            for insight in insights:
                all_insights.append(insight)
        return all_insights

    def get_campaigns(self, fields, params):
        all_campaigns = []
        my_accounts = self.business.get_client_ad_accounts()
        for account in my_accounts:
            account = AdAccount(fbid=account['id'], api=self.api)
            campaigns = account.get_campaigns(params=params, fields=fields)
            for campaign in campaigns:
                all_campaigns.append(campaign)
        return all_campaigns

    def get_accounts(self, fields, params):
        all_accounts = []
        my_accounts = self.business.get_client_ad_accounts(params=params, fields=fields)
        for account in my_accounts:
            all_accounts.append(account)

        return all_accounts

    def get_advertising_campaign(self, account_fields, campaign_fields, ad_fields, time_range=Dict[str, str]):


        params_ads = {'time_range': time_range,
                      'time_increment': 1,
                      'level': 'ad',
                      'sort': ['created_time_descending'],
                      'export_format': 'xls'}

        params_campaigns = {'time_range': time_range,
                            'time_increment': 1,
                            'level': 'campaign',
                            'export_format': 'xls'}

        params_accounts = {'time_range': time_range,
                           'time_increment': 1,
                           'level': 'account',
                           'export_format': 'xls'}



        import pandas as pd

        all_insights = self.get_insights(ad_fields, params_ads)
        all_campaigns = self.get_campaigns(campaign_fields, params_campaigns)
        all_accounts = self.get_accounts(account_fields, params_accounts)

        # DataFrame из all_insights
        insights_data = []
        for insight in all_insights:
            row = {field: insight.get(field, None) for field in ad_fields}
            insights_data.append(row)
        df_insights = pd.DataFrame(insights_data, columns=ad_fields)

        # DataFrame из all_campaigns
        campaigns_data = []
        for campaign in all_campaigns:
            row = {field: campaign.get(field, None) for field in campaign_fields}
            campaigns_data.append(row)
        df_campaigns = pd.DataFrame(campaigns_data, columns=campaign_fields)
        # DataFrame из all_accounts
        accounts_data = []
        for account in all_accounts:
            row = {field: account.get(field, None) for field in account_fields}
            accounts_data.append(row)
        df_accounts = pd.DataFrame(accounts_data, columns=account_fields)

        df_dict = {
            "Insights": df_insights,
            "Campaigns": df_campaigns,
            "Accounts": df_accounts
        }
        return df_dict
        # with pd.ExcelWriter(f"campaign_data_{time_range['since']}_{time_range['until']}.xlsx") as writer:
        #     df_insights.to_excel(writer, sheet_name="Insights", index=False)
        #     df_campaigns.to_excel(writer, sheet_name="Campaigns", index=False)
        #     df_accounts.to_excel(writer, sheet_name="Accounts", index=False)
        #     print("Таблицы собраны")
