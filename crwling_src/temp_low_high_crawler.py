from bs4 import BeautifulSoup
import requests
import pandas as pd

temp_low_high_list = ['10', '08']
temp_low = []
temp_high = []
for temp in temp_low_high_list:
    for year in range(2020,2025):
        url = f'https://www.weather.go.kr/w/observation/land/past-obs/obs-by-element.do?stn=108&yy={year}&obs={temp}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        elemonts = soup.select('table#weather_table tr')
        for elemont in elemonts:
            if temp == '08':
                temp_high.append([year]+[el.text.split('\n')[1].replace('\xa0','0') if el.text.split('\n')[1]=='\xa0' else el.text.split('\n')[1] for el in elemont.select('td')])
            else:
                temp_low.append([year]+[el.text.split('\n')[1].replace('\xa0','0') if el.text.split('\n')[1]=='\xa0' else el.text.split('\n')[1] for el in elemont.select('td')])
            
for temp in temp_low:
    if len(temp) == 1:
        temp_low.remove(temp)
for temp in temp_high:
    if len(temp) == 1:
        temp_high.remove(temp)

pd.DataFrame(temp_low).to_csv(r'D:\KHH\project_preson\project_data\웹크롤링데이터\2020-2024최저기온데이터.csv',index=False)
pd.DataFrame(temp_high).to_csv(r'D:\KHH\project_preson\project_data\웹크롤링데이터\2020-2024최고기온데이터.csv',index=False)