import gspread, sys, json, time 
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
# from pprint import pprint

f = open("details.json")
details = json.load(f)
f.close()

row = int(input("Please input row of oldest unseen confession:: ")) # 6830
lc = int(input("Please input the next LC value:: "))
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
spreadsheet = client.open(details["spreadsheet_name"]) # Open the spreadhseet
sheet = spreadsheet.get_worksheet(0)


# Selenium
# Open a Chrome window
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(options=chrome_options)

# Log in to Facebook
email = details["email"]
password = details["password"]
driver.get('https://www.facebook.com/')
user =  driver.find_element_by_id('email')
user.send_keys(email)
pwd = driver.find_element_by_id('pass')
pwd.send_keys(password)
button = driver.find_element_by_id('u_0_b')
button.submit()
time.sleep(5)

# Navigate to group
group = details["group_link"]
driver.get(group)
time.sleep(3)

# Change to page user
driver.find_element_by_xpath("//div[@aria-label='Actor Selector']").click()
time.sleep(2)
paths = driver.find_elements_by_xpath('//span[contains(text(), "Bevo\'s Tea")]')

userSelect = driver.find_element_by_xpath('//span[contains(text(), "Choose How to Interact")]//following::span[contains(text(), "Bevo\'s Tea")]')
userSelect.click()
#paths[-1].click() 


# Gets the first unseen confession
def getConfession():
    global row
    assert(row > 1)
    text = sheet.cell(row, 2).value # Get row's confession text
    prevText = sheet.cell(row - 1, 2).value # Get previous row's confession text
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
    lc_text = "#LC" + str(lc)
    confess = '"{}"'.format(text)
    final_message = lc_text + '\n' + confess
    
    # Post to facebook group
    print(final_message)



def teardown():
      # Close selenium
      sys.exit("Later bitch")

toPost(getConfession())

