#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, MetaData
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
import time
import pytz

time_th = pytz.timezone('Asia/Bangkok')
date_time = datetime.now(time_th)
url = 'https://www.worldometers.info/coronavirus/country/thailand/'
url2 = 'https://ddc.moph.go.th/viralpneumonia/index.php'
response = get(url)
response2 = get(url2)
soup = BeautifulSoup(response2.text, 'html.parser')
new_cases = soup.find('div',{'class':'mybg1'}).find('h4').text
html_soup = BeautifulSoup(response.text,'html.parser')
data = html_soup.find_all('span')
confirm_cases = data[4].text
dead_cases = data[5].text
recovery_cases = data[6].text

db_string = "postgresql://postgres:bu12345@18.136.100.9:5432/smarthome"
db = create_engine(db_string)

meta = MetaData(db)
covid_table = Table('covid_updates', meta,
                Column('last_update'),
                Column('confirm_case'),
                Column('recovery'),
                Column('dead'),
                Column('new'),
                Column('createdAt'),
                Column('updatedAt'))

with db.connect() as conn:
    select_statement = covid_table.select()
    insert_statement = covid_table.insert().values(last_update=date_time,
                                                   confirm_case=confirm_cases,
                                                   recovery=recovery_cases,
                                                   dead=dead_cases,
                                                   new=new_cases,
                                                   createdAt=date_time,
                                                   updatedAt=date_time)

    conn.execute(insert_statement)   

print('confirm casses: ',confirm_cases)
print('dead: ',dead_cases)
print('recovery: ', recovery_cases)
print('new: ',new_cases)
