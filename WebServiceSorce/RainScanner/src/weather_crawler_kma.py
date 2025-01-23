def weather_crawler():
    from selenium import webdriver
    import time
    from bs4 import BeautifulSoup

    url = 'https://www.weather.go.kr/w/index.do'
    dv = webdriver.Chrome()
    dv.get(url)
    time.sleep(5)
    soup = BeautifulSoup(dv.page_source, "html.parser")
    dv.close()

    w_list = soup.select('ul.item > li > span.wic')
    li_list = soup.select('ul.item > li')
    print(len(li_list))
    precipitation_list = []
    for li in li_list:
        el = li.select('span')
        if '강수확률' in str(el):
            precipitation_list.append(str(el).split('<span>')[1].split('</span')[0])

    return [w_list[1].text,w_list[2].text,w_list[4].text,w_list[8].text], [precipitation_list[1],precipitation_list[2],precipitation_list[4],precipitation_list[8]]

print(weather_crawler())