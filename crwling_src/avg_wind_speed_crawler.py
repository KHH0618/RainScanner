from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

avg_wind_speed = []
for year in range(1960,2025):
    url = f'https://www.weather.go.kr/w/observation/land/past-obs/obs-by-element.do?stn=108&yy={year}&obs=06'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    elemonts = soup.select('table#weather_table tr')
    for elemont in elemonts:
        el = elemont.select('td')
        e_list = []
        for e in el:
            e_list.append([str(e).split('(')[1].split(',')[0].replace("'", '') if 'script' in str(e) else str(e).split('>')[2].split('<')[0]])
        avg_wind_speed.append(e_list+[str(year)])
        
for wind in avg_wind_speed:
    if len(wind) == 1:
        avg_wind_speed.remove(wind)
pd.DataFrame(avg_wind_speed).to_csv('/Volumes/ESD-ISO/project_preson/project_data/웹크롤링데이터/1960-2024평균풍속데이터.csv', index=False)
# print(np.array(avg_wind_speed).shape)
# print(avg_wind_speed)