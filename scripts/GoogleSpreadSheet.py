import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSpreadSheet:
    def __init__(self, client_secret_filepath):
        # Аутентификация и создание клиента gspread
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(client_secret_filepath, scope)
        self.client = gspread.authorize(credentials)


    def create_spreadsheet(self, emails, spreadsheet_name):
        spreadsheet = self.client.create(spreadsheet_name)
        for email in emails:
            spreadsheet.share(email, perm_type='user', role='writer')

        return spreadsheet.url

    def write_to_google_sheets(self, df_dict, spreadsheet_url):
        # открытие существующей таблицы
        spreadsheet = self.client.open_by_url(spreadsheet_url)



        for sheet_name, df in df_dict.items():
            try:
                # Попытка открытия существующего листа
                worksheet = spreadsheet.worksheet(sheet_name)
                worksheet.clear()  # Очистка листа перед записью новых данных
            except gspread.exceptions.WorksheetNotFound:
                # Создание нового листа, если он не существует
                worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=df.shape[0], cols=df.shape[1])

            set_with_dataframe(worksheet, df)

        return spreadsheet.url


