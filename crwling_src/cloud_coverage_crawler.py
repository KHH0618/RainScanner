from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

cloudiness = []
for year in range(2020,2025):
    url = f'https://www.weather.go.kr/w/observation/land/past-obs/obs-by-element.do?stn=108&yy={year}&obs=59'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    elemonts = soup.select('table#weather_table tr')
    for elemont in elemonts:
        cloudiness.append([year]+[el.text.split('\n')[1].replace('\xa0','0') if el.text.split('\n')[1]=='\xa0' else el.text.split('\n')[1] for el in elemont.select('td')])
for cl in cloudiness:
    if len(cl) == 1:
        cloudiness.remove(cl)

cloudiness_df = pd.DataFrame(cloudiness)
cloudiness_df.to_csv(r'D:\KHH\project_preson\project_data\웹크롤링데이터\2020-2024운량데이터.csv',index=False)