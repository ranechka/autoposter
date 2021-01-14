import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("Copy of UT Confessions (new) (Responses)").sheet1  # Open the spreadhseet


def getConfession(row):
    text = sheet.cell(row, 2).value # Get row's confession text
    if(row > 1):
        prevText = sheet.cell(row-1, 2).value # Get previous row's confession text
