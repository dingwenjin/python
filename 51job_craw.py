from selenium import webdriver
from time import ctime,sleep
import threading
import requests
import urllib.request
from queue import Queue
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re
import chardet
'''
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
'''
def getMainPage(url,keys):
    driver = webdriver.PhantomJS()            #启动浏览器引擎
    driver.get(url)
    print("进入..."+driver.title)
    elem = driver.find_element_by_id('kwdselectid')                             #获取输入框的单元
    elem.clear()                                                                   #清理输入框
    elem.send_keys(keys)                                                            #接收用户输入
    elem.find_element_by_xpath('//*[@id="work_position_input"]').click()                        #取消默认的城市
    elem.find_element_by_xpath('//*[@id="work_position_click_multiple_selected_each_060000"]/span').click()      #选中取消的城市
    elem.find_element_by_xpath('//*[@id="work_position_click_bottom_save"]').click()                   #确认取消,此时是全国范围
    elem.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/button').click()                              #点击搜索
    return driver                                  #返回引擎对象


class craw_url(threading.Thread):                                 #用户获取网页源码
    def __init__(self,page_queue,URL,driver):
        threading.Thread.__init__(self)
        self.page_queue = page_queue
        self.URL =URL
        self.driver = driver

    def run(self):
        self.crawing()

    def crawing(self):
        while True:
            if self.page_queue.empty():
                sleep(2)
            else:
                page = self.page_queue.get()
                url = self.URL+str(page)+'.html'     #要获取数据的页面url
                #page_dict = {}
                #page_dict[page] = url
                #print(url)
                #print("dwj")
                #header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
                #html = urllib.request.urlopen(url).read()
                html = requests.get(url).content
                '''
                encoding_dict = chardet.detect(html)
                web_encoding = encoding_dict['encoding']
                if web_encoding == 'utf-8' or web_encoding == 'UTF-8':
                    html = html
                else:
                '''
                html = html.decode('gbk', 'ignore').encode('utf-8')
                #content = requests.get(url)
                #content.encoding = 'utf-8'
                #content = self.driver.page_source                             #关键,获取当前页面的源码,当多个线程同时进来，将发生同抓取一个页面
                #content = str(content).encode('utf-8')
                data_queue.put(html)                  #将获取的网页源码放入到data_queue队列中

                break                                         #必须的,不然就会出错,将网页源码放入队列后退出当前的循环,从新判断队列是否是空
                #size = data_queue.qsize()
                #print(size)
                #print(self.data_queue.get())


class Thread_Parser(threading.Thread):
    def __init__(self,data_queue,lock):
        threading.Thread.__init__(self)
        self.data_queue = data_queue
        self.lock = lock                        #锁机制


    def run(self):
        #print("aaa")
        #while not self.data_queue.empty():
            #print("111")
        item = self.data_queue.get()            #从data_queue中取出一页
        self.parser_data(item)                  #将该页放入解析函数中，让其解析出用户想要的数据
        self.data_queue.task_done()             #发送信号，表示网页源码解析完成

    def parser_data(self,item):
        #print("222")
        soup = BeautifulSoup(item, "html.parser")
        position = soup.find_all("p", {"class": "t1"})
        company = soup.find_all("span", {"class": "t2"})
        location = soup.find_all("span", {"class": "t3"})
        salary = soup.find_all("span", {"class": "t4"})
        publish = soup.find_all("span", {"class": "t5"})

        i = 1
        global num
        num = 1
        with self.lock:

            with open(r"E:\python\python programming\python.txt","a") as f:
                f.write("\n\n第 "+str(num)+" 页\n")
                #print("第 "+str(num)+" 页")
                for each in position:
                    f.write("\n第 " + str(i) + " 个工作\n")
                    f.write("position: " + each.a.get('title')+"\n")
                    f.write("company: " + company[i].string+"\n")
                    f.write("location: " + location[i].string+"\n")
                    if salary[i].string == None:
                        f.write("salary: 工资面议"+"\n")
                    else:
                        f.write("salary: " + salary[i].string+"\n")
                    f.write("publish: " + publish[i].string+"\n")
                    f.write("\n")
                    i += 1
                num += 1


            '''
            #for each in position:
                print("\n第 " + str(i) + " 个工作")
                print("position: " + each.a.get('title'))
                print("company: " + company[i].string)
                print("location: " + location[i].string)
                if salary[i].string == None:
                    print("salary: 工资面议")
                else:
                    print("salary: " + salary[i].string)
                print("publish: " + publish[i].string)
                print("\n\n")
                i += 1
                '''


        '''
        self.driver.find_element_by_link_text("下一页").click()
        url = self.driver.current_url
        page_queue.put(url)
        print(url)

        
        self.driver.find_element_by_link_text("下一页").click()
        url = self.driver.current_url
        url = soup.find("div", {"class": "dw_page"}).find("li", {"class": "bk"}).find("a").attrs['href']
        print(url)
        page_queue.put(url)
       '''

data_queue = Queue(1000)                  #创建data_queue队列,用于存放网页源码,队列深度是1000
page_queue = Queue(1000)                  #创建page_queue队列,用于存放网页的编号,队列深度是1000
lock = threading.Lock()

def main(URL,driver):
    #page_data =driver.page_source         #获取当前页面源码

    #page_queue.put(url)
    #data_queue.put(page_data)

    for page in range(1,21):
        page_queue.put(page)         #生成编号是1~20，放入队列中

    page_threads = []                 #线程列表，用于存放线程
    for i in range(20):
        t = craw_url(page_queue,URL,driver)
        #t.setDaemon(True)
        t.start()
        page_threads.append(t)

    data_threads= []
    for i in range(20):
        #print("aaaa")
        t = Thread_Parser(data_queue,lock)                  #解析页面类,输入数据时需要上锁
        #t.setDaemon(True)
        t.start()                                #启动线程
        data_threads.append(t)                   #将线程放入列表

    for t in page_threads:                       #阻塞主线程,目的是为了等待所有的page_threads都运行结束。如果不加，程序可能提前结束(主线程运行完直接退出，此刻子线程可能还没结束)
        t.join()

    for t in data_threads:                       #阻塞主线程,目的是为了等待所有的page_threads都运行结束
        t.join()


if __name__ == '__main__':
    url = "http://www.51job.com/"
    keys = input('请输入要搜索的关键字：')
    print("Start time is: %s", ctime())
    start = datetime.now()
    driver = getMainPage(url,keys)
    url = driver.current_url            #获取页面当前url
    print(url)
    pattern = re.compile(r"^http:.*?\.html")
    URL = re.match(pattern, url).group().split('.html')[0][:-1]         #获取输入的前缀,可以用于查询不同的关键字

    main(URL,driver)
    end = datetime.now()

    print("totle time is : %s" % (end - start))
