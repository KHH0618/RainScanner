from datetime import datetime
from urllib.request import urlretrieve
import requests
import os
from bs4 import BeautifulSoup
import time
yesterday = datetime.today().strftime("%Y%m")+'0'+str(datetime.today().day-1)
key = 'Pzsb0eNOILTcVDvL964SX%2BMsPUJNdeoaiwiUzjstmhIYzGdzOwDs66icIeWo99PfLOyJ3%2BfMIfsJ6fd6XKxdYg%3D%3D'
satellite_image = ['ir105','vi006','wv069', 'sw038', 'rgbt', 'rgbdn'] 

if yesterday not in os.listdir(path=os.getcwd()):
        os.makedirs(name=os.getcwd()+'/'+yesterday)

for image in satellite_image :
    if image not in os.listdir(path=os.getcwd()+'/'+yesterday):
        os.makedirs(name=os.getcwd()+'/'+yesterday+'/'+image)
        
    path = os.getcwd()+'/'+yesterday+'/'+ image
    print(path, '경로에 파일이 저장됩니다')
    url='http://apis.data.go.kr/1360000/SatlitImgInfoService/getInsightSatlit?serviceKey={}&numOfRows=10&pageNo=1&sat=g2&data={}&area=ko&time={}'.format(key,image,yesterday)
    print(url)
    time.sleep(1)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'xml')
    for image_ulr_tag in soup.select('satImgC-file'):
        image_url = str(image_ulr_tag).split('<satImgC-file>')[1].split('</satImgC-file>')[0]
        img_response = requests.get(image_url)
        img_name = os.path.join(path, os.path.basename(image_url[-20:-8])+'.png')
        with open(img_name, 'wb') as f:
            f.write(img_response.content)
    print(image, '사진 저장 완료')
