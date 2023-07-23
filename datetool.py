from bs4 import BeautifulSoup
import requests as rq 
from datetime import datetime
import os
from tabulate import tabulate
import numpy as np
from unidecode import unidecode
import time 
import pandas as pd 


response = rq.get('https://www.time.ir/')
resp = response.text

soup = BeautifulSoup(resp, 'html.parser')

# date_format = 1
dates = ['jalali', 'miladi small', 'qamari small']

def date(date_format = 1):
    div = soup.find_all('span', class_ = 'show date')
    date= div[date_format - 1].text
    return date

def date_numeric(date_format = 1):
    div = soup.find_all('span', class_ = 'show numeral')
    date= div[date_format - 1].text
    return date

def full_status(date_format = 1):
    div = soup.find_all('span', class_ = 'show date')
    date= div[date_format - 1].text
    print('date:', date)
    div = soup.find_all('span', class_ = 'show numeral')
    date= div[date_format - 1].text
    print('date numeric:', date)
    print('time:', datetime.now().strftime('%H:%M:%S'))
    print('date format:', date_format)
    return f'date numeric: {date}\ntime: {datetime.now().strftime("%H:%M:%S")}\n'

def calendar(date_format = 1):
    div = soup.find_all('div', class_ = 'dayHeader')
    days_header = []
    for i in div:
        days_header.append(i.text)
    
    div = soup.find_all('div', class_ = 'dayList')
    days = []
    for i in div:
        dyna = i.find_all('div', class_ = f'{dates[date_format - 1]}')
        for j in dyna:
            days.append(j.text)


    final_days_header = []
    for i in days_header[0]:
        if i != '\n':
            if i == 'ش': final_days_header.append('sh')
            elif i == 'ی': final_days_header.append('ye')
            elif i == 'د': final_days_header.append('do')
            elif i == 'س': final_days_header.append('se')
            elif i == 'چ': final_days_header.append('ch')
            elif i == 'پ': final_days_header.append('pa')
            elif i == 'ج': final_days_header.append('jo')
            days = unidecode(' '.join(days)).split(' ')
        
    
        
    if date_format == 3:
        final_days_header = ['We', 'Th', 'Fr', 'Sa', 'Su', 'Mo', 'Tu'] 
        days = unidecode(' '.join(days)).split(' ')


    days = np.reshape(days, (-1, 7))
    
    return pd.DataFrame(days, columns=final_days_header).to_string(index=False)
    # return tabulate(days, final_days_header, tablefmt = 'outline')

# Telegram: https://t.me/iliyaFaramarzi
# instagram: https://www.instagram.com/faramarziiliya/
# github: https://github.com/iliyafaramarzi?tab=repositories
# linkedin: https://ir.linkedin.com/in/iliya-faramarzi-13109a21a