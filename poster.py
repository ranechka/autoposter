import gspread
from oauth2client.service_account import ServiceAccountCredentials
# from pprint import pprint

row = int(input("Please input row of oldest unseen confession:: ")) # 6830
lc = int(input("Please input the next LC value:: "))
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
# print("creds done")
spreadsheet = client.open("Copy of UT Confessions (new) (Responses)") # Open the spreadhseet
# print("Spreadsheet opened")
sheet = spreadsheet.get_worksheet(0)

# Gets the first unseen confession
def getConfession():
    global row
    assert(row > 1)
    text = sheet.cell(row, 2).value # Get row's confession text
    prevText = sheet.cell(row-1, 2).value # Get previous row's confession text
    while(text == prevText): # Check for duplicate of the previous row
        row = row + 1
        prevText = text
        text = sheet.cell(row, 2).value # Get row's confession text
    return text

# Displays confession
# Asks user whether to post, skip, or exit Autoposter
# Calls teardown or fbPoster
def toPost(confession):
    global row
    print(confession)
    answer = input("Post this confession? (yes/no) \nAnything else for exit\n")
    if(answer == 'no'):
        # Mark as seen
        row = row + 1
    elif(answer == 'yes'):
        # Mark as seen
        row = row + 1
        fbPoster(confession)
    else:
        teardown()

# Formats the text into a confesison with LC number
# Uses selenium to post to Facebook
def fbPoster(text):
    print("YOU MADE IT")
    pass


def teardown():
      # Close selenium
      sys.exit("Later bitch")

toPost(getConfession())

