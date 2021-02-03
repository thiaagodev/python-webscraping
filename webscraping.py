import time 
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json


def make_rank(rank_type):
    driver.find_element_by_xpath(f"//div[@class='nba-stat-table__overflow']//table//thead//tr//th[@data-field='{rankings[rank_type]['field']}']").click()

    element = driver.find_element_by_xpath("//div[@class='nba-stat-table__overflow']//table")
    html_content = element.get_attribute('outerHTML')

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    df_full = pd.read_html(str(table))[0].head(10)
    df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', rankings[rank_type]['label']]]
    df.columns = ['pos', 'player', 'team', 'total']


    return df.to_dict('records')


url = 'https://www.nba.com/stats/players/traditional/?sorcleart=PTS&dir=-1'

option = Options()
option.headless = False
driver = webdriver.Firefox(options=option)

top10ranking = {}
rankings = {
    '3points': {'field': 'FG3M', 'label': '3PM'},
    'points': {'field': 'PTS', 'label': 'PTS'},
    'assistants': {'field': 'AST', 'label': 'AST'},
    'rebounds': {'field': 'REB', 'label': 'REB'},
    'steals': {'field': 'STL', 'label': 'STL'},
    'blocks': {'field': 'BLK', 'label': 'BLK'},
}


driver.get(url)
time.sleep(10)
driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()

time.sleep(5)

for key in rankings:
    top10ranking[key] = make_rank(key)

driver.quit()

json_ranking = json.dumps(top10ranking)
ranking = open('ranking.json', 'w')
ranking.write(json_ranking)
ranking.close()
