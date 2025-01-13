import requests
import pandas as pd
from bs4 import BeautifulSoup
key = 'Pzsb0eNOILTcVDvL964SX%2BMsPUJNdeoaiwiUzjstmhIYzGdzOwDs66icIeWo99PfLOyJ3%2BfMIfsJ6fd6XKxdYg%3D%3D'
# hm 습도
# pv 증기압
# td 이슬점온도
# pa 현지기압
# ps 해면기압
# dc10Tca 전운량
# clfmAbbrCd 운형
# lcsCh 최저운고
# m005Te 5cm 지중온도
# m01Te 10cm 지중온도
# m02Te	20cm 지중온도
# m03Te	30cm 지중온도
# vs	시정
# ws	풍속
# wd	풍향
# rn	강수량
# tm 시간

asos_list = []
for year in range(2020,2025):
    start_day = str(year) + '0101'
    end_day = str(year) + '1231'
    url = f'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList?serviceKey={key}&numOfRows=10&pageNo=1&dataCd=ASOS&dateCd=HR&stnIds=108&endDt={end_day}&endHh=01&startHh=01&startDt={start_day}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    cnt = soup.select_one('totalCount')
    print(cnt.text)
    for page in range(1, int(int(cnt.text)/10)+2):
        print(page)
        url = f'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList?serviceKey={key}&numOfRows=10&pageNo={page}&dataCd=ASOS&dateCd=HR&stnIds=108&endDt={end_day}&endHh=01&startHh=01&startDt={start_day}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'xml')
        elements = soup.select('item')
        for element in elements:
            hm = element.select_one('hm')
            pv = element.select_one('pv')
            ps = element.select_one('ps')
            td = element.select_one('td')
            pa = element.select_one('pa')
            dc10Tca = element.select_one('dc10Tca')
            clfmAbbrCd = element.select_one('clfmAbbrCd')
            lcsCh = element.select_one('lcsCh')
            m005Te = element.select_one('m005Te')
            m01Te = element.select_one('m01Te')
            m02Te = element.select_one('m02Te')
            m03Te = element.select_one('m03Te')
            vs = element.select_one('vs')
            ws = element.select_one('ws')
            wd = element.select_one('wd')
            rn = element.select_one('rn')
            tm = element.select_one('tm')
            asos_list.append([{'tm':tm.text, 'hm':hm.text, 'pv':pv.text, 'ps':ps.text, 'td':td.text, 'pa':pa.text, 'dc10Tca':dc10Tca.text, 'clfmAbbrCd':clfmAbbrCd.text, 'lcsCh':lcsCh.text, 'm005Te':m005Te.text, 'm01Te':m01Te.text, 'm02Te':m02Te.text, 'm03Te':m03Te.text, 'vs':vs.text, 'ws':ws.text, 'wd':wd.text, 'rn':rn.text}])
asos_df = pd.DataFrame(asos_list)
print(asos_df.info())
asos_df.to_csv('D:/KHH/project_preson/project_data/웹크롤링데이터/2020-2024ASOS_관측데이터.csv', index=False)
