from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import json

stats_xpaths = {
    'Points': {'xpath': "/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/thead/tr/th[9]", 'label': 'PTS'},
    '3Points': {'xpath': "/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/thead/tr/th[13]", 'label': '3PM'},
    'Rebounds': {'xpath': "/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/thead/tr/th[21]", 'label': 'REB'},
    'Assists': {'xpath': "/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/thead/tr/th[22]", 'label': 'AST'},
    'Steals': {'xpath': "/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/thead/tr/th[24]", 'label': 'STL'},
    'Blocks': {'xpath': "/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/thead/tr/th[25]", 'label': 'BLK'},
}

table_xpath = '/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table'

nba_top10_stats = {}

def config_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return webdriver.Chrome(options=options)

def get_table_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.find(name='table')

def table_to_dataframe(table,stat):
    df_full = pd.read_html( str(table) )[0].head(10)
    df = df_full[['Unnamed: 0','PLAYER', 'TEAM', stats_xpaths[stat]['label']]]
    df.columns = ['Position', 'Player', "Team", stat]
    return df

def dict_to_json(dict):
    js = json.dumps(nba_top10_stats)
    fp = open('nba_stats.json','w')
    fp.write(js)
    return fp.close()


def get_nba_infos():
    driver = config_driver()

    driver.get("https://www.nba.com/stats/players/traditional/?dir=1&Season=2021-22&SeasonType=Regular%20Season&PerMode=Totals&sort=TEAM_ABBREVIATION")
    sleep(4)

    for stat in stats_xpaths:
        driver.find_element(by=webdriver.common.by.By.XPATH, value=stats_xpaths[stat]['xpath']).click()

        element = driver.find_element(by= webdriver.common.by.By.XPATH, value=table_xpath)
        html_content = element.get_attribute('outerHTML')

        table = get_table_from_html(html_content)

        df = table_to_dataframe(table, stat)

        nba_top10_stats[stat.lower()] = df.to_dict('records')

    driver.quit()

    dict_to_json(nba_top10_stats)


get_nba_infos()
