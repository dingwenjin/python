from selenium import webdriver
from bs4 import BeautifulSoup
from time import ctime,sleep
from datetime import datetime
import csv
def getDriver(url,keys):
    driver = webdriver.Chrome()
    driver.get(url)
    #print(driver.current_url)
    print("进入..."+driver.title)
    elem = driver.find_element_by_id('txtZip')
    elem.send_keys(keys)
    sleep(1)
    elem.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[1]/span').click()
    sleep(2)
    return driver

def get7dContent(driver):
    elem = driver.find_element_by_id('someDayNav')
    elem.find_element_by_xpath('//*[@id="someDayNav"]/li[2]').click()
    return driver

def getContent(driver):
    #url = driver.current_url
    #print(url)
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")
    #print(soup)
    ul = soup.find("div",{"id":"7d"}).find("ul",{"class":"t clearfix"})
    lis = ul.find_all("li")
    #print(lis)
    weather_forecast = []
    date_all = []
    weather_all = []
    temprature_all = []
    wind_all = []
    tmp = []
    for li in lis:
        date = li.find("h1").string
        date = '2017-8-'+date
        #print(date)
        #date_all.append(date)
        tmp.append(date)
        weather = li.find("p",{"class":"wea"}).string
        #print(weather)
        #weather_all.append(weather)
        tmp.append(weather)
        temprarue = li.find("p",{"class":"tem"}).find("i").string
        #print(temprarue)
        #temprature_all.append(temprarue)
        tmp.append(temprarue)
        wind = li.find("p",{"class":"win"}).find("i").string
        #print(wind)
        #wind_all.append(wind)
        tmp.append(wind)
        weather_forecast.append(tmp)
        tmp = []
    return weather_forecast

def csv_write(weather_forecast,keys):
    csvFile = open(r'E:\python\python Spider\%s.csv'%keys,'a+',encoding='gbk',newline='')
    try:
        writer = csv.writer(csvFile)
        writer.writerow(('日期','天气','温度','风向'))
        for line in weather_forecast:
            writer.writerow(line)
    finally:
        csvFile.close()

if __name__ == '__main__':
    url = 'http://www.weather.com.cn/'
    keys = input("请输入要查找的城市: ")
    start = datetime.now()
    driver = getDriver(url,keys)
    driver = get7dContent(driver)
    weather_forecast = getContent(driver)
    #print(weather_forecast)
    csv_write(weather_forecast,keys)
    end = datetime.now()
    print("Duration time is: %s"%(end-start))