from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from mysql.connector import Error
from mysql.connector import errorcode
from datetime import datetime
import mysql.connector
import time
import pytz

time_th = pytz.timezone('Asia/Bangkok')
date_time = datetime.now(time_th)
url = 'https://www.worldometers.info/coronavirus/country/thailand/'
response = get(url)
html_soup = BeautifulSoup(response.text,'html.parser')
data = html_soup.find_all('span')
confirm_casses = data[4].text
dead = data[5].text
recovery = data[6].text

def insert_todb(last_update, confirm_casses, recovery, dead):
    try:
        connection = mysql.connector.connect(host='34.122.124.80',
                                             database='smart_home',
                                             user='nsr-admin',
                                             password='natthapon024299')
        query = """insert into covid19_thai (last_update,confirm_case,recovery,dead) VALUES (%s,%s,%s,%s)"""
        attr = (last_update, confirm_casses, recovery, dead)
        cursor = connection.cursor()
        cursor.execute(query, attr)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into sub table")
        cursor.close()
    except mysql.connector.Error as error:
        print("Failed to insert record into sub table {}".format(error))
    finally:
        if (connection.is_connected()):
            connection.close()
            print("MySQL connection is closed")
insert_todb(date_time,confirm_casses,recovery,dead)
print('confirm casses: ',confirm_casses)
print('dead: ',dead)
print('recovery: ', recovery)