from bs4 import BeautifulSoup
import pandas as pd
import requests

key = 'Pzsb0eNOILTcVDvL964SX%2BMsPUJNdeoaiwiUzjstmhIYzGdzOwDs66icIeWo99PfLOyJ3%2BfMIfsJ6fd6XKxdYg%3D%3D'
min_year = 2020
max_year = 2021
pressure_lcsCh_list = []
while True:
    if max_year >= 2025:
        break
    url = f'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList?serviceKey={key}&numOfRows=999&pageNo=1&dataCd=ASOS&dateCd=HR&stnIds=108&endDt={max_year}1231&endHh=01&startHh=01&startDt={min_year}0101'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    page_num = int(int(soup.select_one('totalCount').text)/999)
    print(url)
    for page in range(page_num+1):
        url = f'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList?serviceKey={key}&numOfRows=999&pageNo={page+1}&dataCd=ASOS&dateCd=HR&stnIds=108&endDt={max_year}1231&endHh=01&startHh=01&startDt={min_year}0101'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.select('item')
        for item in items:
            date = item.select_one('tm').text
            pv = item.select_one('pv').text
            lcsCh = item.select_one('lcsCh').text
            pressure_lcsCh_list.append([date, pv, lcsCh])
    min_year += 1
    max_year += 1
df = pd.DataFrame(pressure_lcsCh_list)
df.to_csv('/Volumes/ESD-ISO/project_preson/project_data/웹크롤링데이터/2020-2024_증기압_최저운고_데이터.csv')