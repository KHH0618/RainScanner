import requests
from bs4 import BeautifulSoup

key = 'Pzsb0eNOILTcVDvL964SX%2BMsPUJNdeoaiwiUzjstmhIYzGdzOwDs66icIeWo99PfLOyJ3%2BfMIfsJ6fd6XKxdYg%3D%3D'

url = f'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList?serviceKey={key}&numOfRows=10&pageNo=1&dataCd=ASOS&dateCd=HR&stnIds=108&endDt=20241230&endHh=01&startHh=01&startDt=20241130'
print(url)
response = requests.get(url)
soup = BeautifulSoup(response.text, 'xml')
item_list = soup.select('item')
for item in item_list:
    time = item.select_one('tm').text
    loc = item.select_one('stnNm').text
    tamp = item.select_one('ta').text
    print(time)