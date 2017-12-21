import requests
from bs4 import BeautifulSoup
from queue import Queue
from time import ctime,sleep
from datetime import datetime

def getHtml(url):
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
    html = requests.get(url,headers=header).content
    #print(html)
    html = html.decode('gbk','ignore').encode('utf-8')
    return html


def getChapters(html,root_url):
    soup = BeautifulSoup(html,"html.parser")
    #print(soup)
    a = soup.find_all("a")
    #print(a)
    urls = []
    titles = []
    chapters = {}
    for i in a[20:-5]:                              #ȡ��ǰ20���ͺ�5��<a>��ǩ������(��ʱ�õ�����С˵�������½ڲ���)
        #print(i)
        #print(i.string)
        #print(i.attrs['href'])
        url = i.attrs['href']                       #��ȡС˵������(��ȡ���ǲ�����������)
        url = root_url+url                          #�����������������������ƴ�������γɸ����½ڵ���������
        urls.append(url)
        #print(url)
        titles.append(i.string)                      #��ȡ�����½ڵı���

    chapters = dict(zip(titles,urls))                #�������½ڵı��������ת��Ϊ�ֵ����ͣ���Ϊ��������

    #for item in chapters.items():
    #    print(item)
    '''
    if "href" in i.attrs:
        url = i.attrs['href']
        #content = a.string
        print(url)
    '''
    return chapters

def getContent(chapters):
    titles = []
    for title in chapters.keys():
        title = str(title).replace('/','').replace('*','').replace('?','').replace('"','').replace(':','').replace('<','').replace('>','').replace("|",'')        #ȥ��д���ļ����ⲻ�Ϸ����ַ�
        titles.append(title)
    for title in titles:
        print(title)
    print("\n\n")
    urls = []
    for url in chapters.values():
        urls.append(url)
    for url in urls:
        print(url)

    global i                             #��Ϊ�����ȫ�ֱ���
    i = 0
    for url in urls:
        html = getHtml(url)
        soup = BeautifulSoup(html,"html.parser")
        content = soup.find("dd", {"id": "contents"}).get_text()           #��ȡ�����½ڵ�����
        content = str(content).replace('http://www.cbiquge.com','')        #�滻�����Ϸ����ַ�
        #print(content)
        '''
        f = open(r'E:\python\python Spider\storys\%s.txt'%titles[i],'w',encoding='utf-8')
        f.write(content)
        f.close()
        i += 1
        '''
        with open(r'E:\python\python Spider\storys\%s.txt'%titles[i],'w',encoding='utf-8') as f:
            f.write(content)
        i += 1


#def main():


if __name__ == '__main__':
    root_url = 'http://www.23us.us/html/1/1642/'      #��ڵ�ַ
    print("Starting time is: %s"%ctime())
    start = datetime.now()
    html = getHtml(root_url)
    chapters = getChapters(html,root_url)
    getContent(chapters)
    print("Ending time is: %s"%ctime())
    end = datetime.now()
    print("duration time is: %s"%(end-start))
