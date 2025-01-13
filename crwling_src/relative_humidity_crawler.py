from bs4 import BeautifulSoup
import requests
import pandas as pd

relative_humidity = []
for year in range(2020,2025):
    url = f'https://www.weather.go.kr/w/observation/land/past-obs/obs-by-element.do?stn=108&yy={year}&obs=12'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    elemonts = soup.select('table#weather_table tr')
    for elemont in elemonts:
        relative_humidity.append([year]+[el.text.split('\n')[1].replace('\xa0','0') if el.text.split('\n')[1]=='\xa0' else el.text.split('\n')[1] for el in elemont.select('td')])

for rh in relative_humidity:
    if len(rh) == 1:
        relative_humidity.remove(rh)

relative_humidity_df = pd.DataFrame(relative_humidity)
relative_humidity_df.to_csv(r'D:\KHH\project_preson\project_data\웹크롤링데이터\2020-2024상대습도데이터.csv',index=False)