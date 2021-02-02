import time 
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json

url = 'https://stats.nba.com/players/traditional/?PerMode=Totals&Season=2019-20&SeasonType=Regular%20Season&sort=PLAYER_NAME&dir=-1'

option = Options()
option.headless = False
driver = webdriver.Firefox(options=option)

driver.get(url)
time.sleep(10)

driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()

time.sleep(5)
driver.find_element_by_xpath("//div[@class='nba-stat-table__overflow']//table//thead//tr//th[@data-field='PTS']").click()

element = driver.find_element_by_xpath("//div[@class='nba-stat-table__overflow']//table")
html_content = element.get_attribute('outerHTML')

soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')

df_full = pd.read_html(str(table))[0].head(10)
df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', 'PTS']]
df.columns = ['pos', 'player', 'team', 'total']

top10ranking = {}
top10ranking['points'] = df.to_dict('records')

driver.quit()

json_ranking = json.dumps(top10ranking)
ranking = open('ranking.json', 'w')
ranking.write(json_ranking)
ranking.close()
