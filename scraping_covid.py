from psycopg2 import connect
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
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
new = '+' + soup.find('div',{'class':'mybg1'}).find('h4').text
html_soup = BeautifulSoup(response.text,'html.parser')
data = html_soup.find_all('span')
confirm_casses = data[4].text
dead = data[5].text
recovery = data[6].text

def insert_todb(last_update, confirm_casses, recovery, dead, new):
    conn = connect(host='18.136.100.9',
                    database='smarthome',
                    user='postgres',
                    password='bu12345',
                    port='5432')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO covid_update (last_update,confirm_case,recovery,dead,new) VALUES (%s,%s,%s,%s,%s)",(last_update, confirm_casses, recovery, dead, new))
    conn.commit()
    print(cursor.rowcount, "Record inserted successfully into sub table")
    cursor.close()
  
            
insert_todb(date_time,confirm_casses,recovery,dead,new)
print('confirm casses: ',confirm_casses)
print('dead: ',dead)
print('recovery: ', recovery)
print('new: ',new)
