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
    driver = webdriver.PhantomJS()            #�������������
    driver.get(url)
    print("����..."+driver.title)
    elem = driver.find_element_by_id('kwdselectid')                             #��ȡ�����ĵ�Ԫ
    elem.clear()                                                                   #���������
    elem.send_keys(keys)                                                            #�����û�����
    elem.find_element_by_xpath('//*[@id="work_position_input"]').click()                        #ȡ��Ĭ�ϵĳ���
    elem.find_element_by_xpath('//*[@id="work_position_click_multiple_selected_each_060000"]/span').click()      #ѡ��ȡ���ĳ���
    elem.find_element_by_xpath('//*[@id="work_position_click_bottom_save"]').click()                   #ȷ��ȡ��,��ʱ��ȫ����Χ
    elem.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/button').click()                              #�������
    return driver                                  #�����������


class craw_url(threading.Thread):                                 #�û���ȡ��ҳԴ��
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
                url = self.URL+str(page)+'.html'     #Ҫ��ȡ���ݵ�ҳ��url
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
                #content = self.driver.page_source                             #�ؼ�,��ȡ��ǰҳ���Դ��,������߳�ͬʱ������������ͬץȡһ��ҳ��
                #content = str(content).encode('utf-8')
                data_queue.put(html)                  #����ȡ����ҳԴ����뵽data_queue������

                break                                         #�����,��Ȼ�ͻ����,����ҳԴ�������к��˳���ǰ��ѭ��,�����ж϶����Ƿ��ǿ�
                #size = data_queue.qsize()
                #print(size)
                #print(self.data_queue.get())


class Thread_Parser(threading.Thread):
    def __init__(self,data_queue,lock):
        threading.Thread.__init__(self)
        self.data_queue = data_queue
        self.lock = lock                        #������


    def run(self):
        #print("aaa")
        #while not self.data_queue.empty():
            #print("111")
        item = self.data_queue.get()            #��data_queue��ȡ��һҳ
        self.parser_data(item)                  #����ҳ������������У�����������û���Ҫ������
        self.data_queue.task_done()             #�����źţ���ʾ��ҳԴ��������

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
                f.write("\n\n�� "+str(num)+" ҳ\n")
                #print("�� "+str(num)+" ҳ")
                for each in position:
                    f.write("\n�� " + str(i) + " ������\n")
                    f.write("position: " + each.a.get('title')+"\n")
                    f.write("company: " + company[i].string+"\n")
                    f.write("location: " + location[i].string+"\n")
                    if salary[i].string == None:
                        f.write("salary: ��������"+"\n")
                    else:
                        f.write("salary: " + salary[i].string+"\n")
                    f.write("publish: " + publish[i].string+"\n")
                    f.write("\n")
                    i += 1
                num += 1


            '''
            #for each in position:
                print("\n�� " + str(i) + " ������")
                print("position: " + each.a.get('title'))
                print("company: " + company[i].string)
                print("location: " + location[i].string)
                if salary[i].string == None:
                    print("salary: ��������")
                else:
                    print("salary: " + salary[i].string)
                print("publish: " + publish[i].string)
                print("\n\n")
                i += 1
                '''


        '''
        self.driver.find_element_by_link_text("��һҳ").click()
        url = self.driver.current_url
        page_queue.put(url)
        print(url)

        
        self.driver.find_element_by_link_text("��һҳ").click()
        url = self.driver.current_url
        url = soup.find("div", {"class": "dw_page"}).find("li", {"class": "bk"}).find("a").attrs['href']
        print(url)
        page_queue.put(url)
       '''

data_queue = Queue(1000)                  #����data_queue����,���ڴ����ҳԴ��,���������1000
page_queue = Queue(1000)                  #����page_queue����,���ڴ����ҳ�ı��,���������1000
lock = threading.Lock()

def main(URL,driver):
    #page_data =driver.page_source         #��ȡ��ǰҳ��Դ��

    #page_queue.put(url)
    #data_queue.put(page_data)

    for page in range(1,21):
        page_queue.put(page)         #���ɱ����1~20�����������

    page_threads = []                 #�߳��б����ڴ���߳�
    for i in range(20):
        t = craw_url(page_queue,URL,driver)
        #t.setDaemon(True)
        t.start()
        page_threads.append(t)

    data_threads= []
    for i in range(20):
        #print("aaaa")
        t = Thread_Parser(data_queue,lock)                  #����ҳ����,��������ʱ��Ҫ����
        #t.setDaemon(True)
        t.start()                                #�����߳�
        data_threads.append(t)                   #���̷߳����б�

    for t in page_threads:                       #�������߳�,Ŀ����Ϊ�˵ȴ����е�page_threads�����н�����������ӣ����������ǰ����(���߳�������ֱ���˳����˿����߳̿��ܻ�û����)
        t.join()

    for t in data_threads:                       #�������߳�,Ŀ����Ϊ�˵ȴ����е�page_threads�����н���
        t.join()


if __name__ == '__main__':
    url = "http://www.51job.com/"
    keys = input('������Ҫ�����Ĺؼ��֣�')
    print("Start time is: %s", ctime())
    start = datetime.now()
    driver = getMainPage(url,keys)
    url = driver.current_url            #��ȡҳ�浱ǰurl
    print(url)
    pattern = re.compile(r"^http:.*?\.html")
    URL = re.match(pattern, url).group().split('.html')[0][:-1]         #��ȡ�����ǰ׺,�������ڲ�ѯ��ͬ�Ĺؼ���

    main(URL,driver)
    end = datetime.now()

    print("totle time is : %s" % (end - start))
