import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service

#   CONSTANTS
NUMBER_OF_SEARCH_DAYS = 7
FLIGHT_WEBSITE_URL = 'https://www.easemytrip.com'
Google_Forum_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdUslBveWDt7cqAq17mgdesGFWIgir5xnxCLwRnVdHE1UkC0A/viewform?usp=sf_link"
d = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

#   FLIGHT DETAILS LIST
flight_name_list = []
flight_arrival_time_list = []
flight_departure_time_list = []
flight_fare_list = []
flight_dates = []
Month_dates = []


#   USER INPUT
SOURCE = 'DEL'
DESTINATION = 'LKO'

user_date = input('Please input date in dd/mm/yyyy format:\n')
user_month = d[int(user_date[3:5])-1]


#   STARTING SERVICE
service = Service('/Users/gautam/Desktop/test/chromedriver')
driver = webdriver.Chrome(service=service)
action = ActionChains(driver=driver)

driver.get(url=FLIGHT_WEBSITE_URL)
time.sleep(2)
#************* GETTING FROM HOME PAGE TO MAIN PAGE *************



#************* DATE EXTRACTION *************
dates = driver.find_element(By.XPATH, '//*[@id="frmHome"]/div[5]/div[2]/div[3]/div[1]/div[3]')
dates.click()
time.sleep(2)
##  GETTING NEXT 6 MONTHS DATES
for i in range(3):
    for i1 in range(2, 7):
        active = driver.find_element(By.CSS_SELECTOR, f'.main .box .days .bor-d{i1}1')
        d = active.find_elements(By.CSS_SELECTOR, "li[id*='/']")
        for j in d:
            Month_dates.append(j.get_property('id'))
    for i1 in range(2, 7):
        active = driver.find_element(By.CSS_SELECTOR, f'.main1 .box1 .days .bor-d{i1}1')
        d = active.find_elements(By.CSS_SELECTOR, "li[id*='/']")
        for j in d:
            Month_dates.append(j.get_property('id'))

    driver.find_element(By.XPATH, '//*[@id="dvcalendar"]/div/div[2]/div/div[1]/div[3]').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="dvcalendar"]/div/div[2]/div/div[1]/div[3]').click()
    time.sleep(1)

## CLEANING OF DATA IN MONTHS_DATES LIST
i = 0
while i < len(Month_dates):
    if '0000' in Month_dates[i]:
        Month_dates.pop(i)
    else:
        i += 1

## CLICKING ON THE USER DESIRED DATE
action.move_by_offset(xoffset=40, yoffset=50).perform()
action.click().perform()
dates.click()
flag = -1
for i in range(0,len(Month_dates)):
    if user_date in Month_dates[i]:
        flag = 1
        index1 = i
        for date in range(index1, index1+NUMBER_OF_SEARCH_DAYS):
            flight_dates.append(Month_dates[date][-10:])
        for m in range(6):
            month_name1 = driver.find_element(By.XPATH, '//*[@id="dvcalendar"]/div/div[1]/div/div[1]/div[2]').text
            month_name2 = driver.find_element(By.XPATH, '//*[@id="dvcalendar"]/div/div[2]/div/div[1]/div[2]').text
            if user_month in month_name1 or user_month in month_name2:
                break
            else:
                driver.find_element(By.XPATH, '//*[@id="dvcalendar"]/div/div[2]/div/div[1]/div[3]').click()
                time.sleep(1)
                driver.find_element(By.XPATH, '//*[@id="dvcalendar"]/div/div[2]/div/div[1]/div[3]').click()
                time.sleep(1)
        time.sleep(1)
        driver.find_element(By.ID, f'{Month_dates[i]}').click()
        time.sleep(2)
        break
## RAISING ERROR IF USER INPUT DATE IS NOT FOUND IN MONTH_DATES LIST
if flag == -1:
    driver.quit()
    raise ValueError
#************* DATE EXTRACTION COMPLETE  *************



#************* INPUTTING FIELDS ON HOMEPAGE  *************
destination = driver.find_element(By.ID, 'FromSector_show')
destination.click()
destination.send_keys(SOURCE)
time.sleep(1.5)
destination.send_keys(Keys.ENTER)
time.sleep(1.5)

source = driver.find_element(By.ID, 'Editbox13_show')
source.click()
source.send_keys(DESTINATION)
time.sleep(1.5)
source.send_keys(Keys.ENTER)
time.sleep(1.5)

action.move_by_offset(xoffset=40, yoffset=50).perform()
action.click().perform()

search_button = driver.find_element(By.CLASS_NAME, 'src_btn')
time.sleep(1)
search_button.click()

time.sleep(5)
#************* END OF HOME PAGE WORK  *************



#************* FETCHING FLIGHT DATA  *************
next_day_button = driver.find_elements(By.CLASS_NAME, 'txt-m1')[1]
price_button = driver.find_element(By.XPATH, '//*[@id="ResultDiv"]/div/div/div[3]/div[5]/a')
price_button.click()
for i in range(NUMBER_OF_SEARCH_DAYS):
    flight_name = driver.find_element(By.XPATH, '//*[@id="ResultDiv"]/div/div/div[4]/div[1]/div[1]/div[1]/div[1]/div/div[2]/span[1]').text
    departure_time = driver.find_element(By.XPATH, '//*[@id="ResultDiv"]/div/div/div[4]/div[1]/div[1]/div[1]/div[2]/span[1]').text
    arrival_time = driver.find_element(By.XPATH, '//*[@id="ResultDiv"]/div/div/div[4]/div[1]/div[1]/div[1]/div[4]/span[1]').text
    fare = driver.find_element(By.ID, 'spnPrice1').text

    flight_name_list.append(flight_name)
    flight_arrival_time_list.append(arrival_time)
    flight_departure_time_list.append(departure_time)
    flight_fare_list.append(fare)

    next_day_button.click()
    time.sleep(3)
#************* END OF FETCHING OF FLIGHT DATA *************



#************* UPDATING IN GOOGLE FORMS  *************
driver.get(Google_Forum_URL)
time.sleep(2)

for i in range(NUMBER_OF_SEARCH_DAYS):

    date_answer = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    date_answer.send_keys(flight_dates[i][:10])

    flight_name_answer = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    flight_name_answer.send_keys(flight_name_list[i])

    flight_departure_answer = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    flight_departure_answer.send_keys(flight_departure_time_list[i])

    flight_arrival_answer = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input')
    flight_arrival_answer.send_keys(flight_arrival_time_list[i])

    flight_fare_answer = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input')
    flight_fare_answer.send_keys(flight_fare_list[i])

    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()

    submit_another_response = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submit_another_response.click()
    time.sleep(2)

#************* END IN GOOGLE FORMS  *************
driver.quit()