from selenium import webdriver
from time import ctime, sleep
import requests
from bs4 import BeautifulSoup
from json import loads


def getDriver(root_url):
    driver = webdriver.Chrome()
    driver.get(root_url)
    elem = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[5]/div[2]')
    # sleep(2)
    elem.find_element_by_xpath('//*[@id="content"]/div/div[2]/div[4]/div[2]/h2/a').click()  # 加载的为电影
    return driver
    # url = driver.current_url
    # print(url)


def getUrl(driver):
    movie_url_root = driver.current_url
    return movie_url_root


def getHtml(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    html = requests.get(url, headers=header).content.decode('utf-8')  # decode("utf-8")将bytes转化为str，因为json为str类型
    # html = BeautifulSoup(html,"html.parser")
    html = loads(html)['subjects']
    titles = []
    urls = []
    movies = {}
    for i in range(20):
        movie = html[i]
        title = movie['title']
        titles.append(title)
        url = movie['url']
        urls.append(url)
        print(title)
        print(url)


def getMovie(movie_url_root):
    movie_url = movie_url_root.replace('explore#!', 'j/search_subjects?')  # 将入口地址配置成js的链接地址
    print(movie_url + '\n\n')
    # getHtml(movie_url)

    urls = []  # 真正抓取电影的链接
    for num in range(0, 100, 20):
        url = movie_url + str(num)  # 合成新的js地址
        urls.append(url)
    for url in urls:
        print(url + '\n')
        getHtml(url)
        print("\n\n")


if __name__ == '__main__':
    root_url = 'https://movie.douban.com/'
    driver = getDriver(root_url)
    movie_url_root = getUrl(driver)
    movie_url_root = movie_url_root[:-1]  # 去掉最后一个字符
    # print(movie_url)
    getMovie(movie_url_root)
    # urls = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0'
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	