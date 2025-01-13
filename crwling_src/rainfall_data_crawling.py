from bs4 import BeautifulSoup
import requests
import pandas as pd

rainfall = []
for year in range(1960,2025):
    url = f'https://www.weather.go.kr/w/observation/land/past-obs/obs-by-element.do?stn=108&yy={year}&obs=21'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    elemonts = soup.select('table#weather_table tr')
    for elemont in elemonts:
        rainfall.append([year]+[el.text.split('\n')[1].replace('\xa0','0') if el.text.split('\n')[1]=='\xa0' else el.text.split('\n')[1] for el in elemont.select('td')])

for rf in rainfall:
    if len(rf) == 1:
        rainfall.remove(rf)

rainfall_df = pd.DataFrame(rainfall)
rainfall_df.to_csv('/Volumes/ESD-ISO/project_preson/project_data/웹크롤링데이터/2020-2024상대습도데이터.csv',index=False)