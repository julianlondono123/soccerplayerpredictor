from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys;
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
import time
import pandas as pd
import openpyxl

dash = '-'
df = pd.read_excel(r'C:\Users\j\Desktop\italy.xlsx')

df = df[~df.position.str.contains("Back")]
df = df[~df.position.str.contains("Goalkeeper")]
df = df[~df.position.str.contains("Midfield")]
df = df[df.fee > 5]
df = df.drop_duplicates(subset=['player_name'])

df["goal_cont"] = ""

df.reset_index(inplace=True)
df = df.drop("index", axis=1)

driver = webdriver.Chrome("C:/Users/j/Desktop/chromedriver.exe")
driver.get('https://www.transfermarkt.us')
driver.implicitly_wait(15)
driver.switch_to.frame(driver.find_element_by_id('sp_message_iframe_382471'))
driver.implicitly_wait(15)
popup = driver.find_element_by_xpath('//*[@id="notice"]/div[3]/div[2]/button')
driver.implicitly_wait(15)
time.sleep(2)
popup.click()
driver.implicitly_wait(15)
time.sleep(2)
driver.switch_to.default_content()

for x in df.index:

    player_name = df['player_name'][x]

    search_box = driver.find_element_by_name('query')
    search_box.send_keys(player_name)

    driver.implicitly_wait(2)

    search_box.send_keys(Keys.RETURN);

    driver.implicitly_wait(4)

    name_link = driver.find_element_by_link_text(player_name)
    name_link.click()

    driver.implicitly_wait(9)

    view_stats = driver.find_element_by_link_text('View full stats')
    view_stats.click()

    driver.implicitly_wait(6)

    dropdown = driver.find_element_by_xpath(
        '/html/body/div[3]/div[11]/div[1]/div[1]/div[2]/form/div/div/table/tbody/tr/td[2]/div/div')
    time.sleep(2)
    dropdown.click()
    dropdown.click()

    time.sleep(5)

    season_search = driver.find_element_by_xpath(
        '/html/body/div[3]/div[11]/div[1]/div[1]/div[2]/form/div/div/table/tbody/tr/td[2]/div/div/div/div/input')
    season_search.send_keys('20/21')
    season_search.send_keys(Keys.RETURN)

    show_button = driver.find_element_by_xpath(
        '/html/body/div[3]/div[11]/div[1]/div[1]/div[2]/form/div/div/table/tbody/tr/td[3]/input')
    show_button.click()

    goals = driver.find_element_by_xpath('/html/body/div[3]/div[11]/div[1]/div[2]/div[3]/div/table/tfoot/tr/td[4]').text
    assists = driver.find_element_by_xpath(
        '/html/body/div[3]/div[11]/div[1]/div[2]/div[3]/div/table/tfoot/tr/td[5]').text

    if goals == dash:
        goals = 0
    if assists == dash:
        assists = 0

    goal_contributions = int(goals) + int(assists)

    df['goal_cont'][x] = goal_contributions
    df.to_excel("output.xlsx")

print(df)
