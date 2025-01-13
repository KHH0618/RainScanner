from datetime import datetime
from urllib.request import urlretrieve
import requests
import os
from bs4 import BeautifulSoup
import time
import image_corrupt_chk
key = 'Pzsb0eNOILTcVDvL964SX%2BMsPUJNdeoaiwiUzjstmhIYzGdzOwDs66icIeWo99PfLOyJ3%2BfMIfsJ6fd6XKxdYg%3D%3D'
satellite_image = ['ir105','vi006','wv069', 'sw038', 'rgbt', 'rgbdn']
yesterday = datetime.today().strftime("%Y%m")+str(datetime.today().day-1)
image_list = []
image_paths = []

path = 'D:/KHH'
file_chk_list = os.listdir(path=path)
if yesterday not in file_chk_list:
    print('API에서 크롤링을 먼저 진행하세요')

else:
    path += '/' + yesterday
    for image_file_path in os.listdir(path=path):
        print(image_file_path)
        for 
        image_list.append(os.listdir(path=path+  '/' +  image_file_path))
    
    for image_path_list in image_list:
        print(image_path_list)
        image_path_list = os.listdir(path=image_path_list)
        print(image_path_list)
        for image_path in image_corrupt_chk.check_image_corruption(image_path_list):
            image_paths.append(image_path)

print(image_paths)