import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import os

def getHtml(url):
    header  = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
    html = requests.get(url,headers=header).content.decode('gb2312','ignore').encode('utf-8')
    return html


#****************************************��ȡ��Ӧ����Ĳ�ͬͼƬ�᲻��ȫ��ַ���*******************************
def get_Page_Picture_root(html):
    soup = BeautifulSoup(html,"html.parser")
    lis = soup.find_all("li",{"class":"photo-list-padding"})
    titles = []
    urls = []
    page_picture = {}
    for li in lis:
        url = li.find("a")['href']               #����ȫ��url
        #print(url)
        urls.append(url)
        title = li.find('span')['title']
        #print(title)
        titles.append(title)
    page_picture = dict(zip(titles,urls))
    return page_picture


#*********************************************ͼƬ�����,���ز�ͬͼƬ�������url�б�************************************
def get_list_picture(page_picture,root_url):
    list_picture_url = []
    for url in page_picture.values():                    #��ͬͼƬ��Ĳ�����url
        full_detail_url = root_url+url                        #�ϳ�ͼƬ��������url
        #print(full_detail_url)                                 #ͼƬ��url
        list_picture_url.append(full_detail_url)
    #print("\n\n")
    return list_picture_url

#************************************��ȡ��ͬͼƬ��Ĳ�ͬͼƬ**************************************
def get_detail_picture(picture_url):
    html = getHtml(picture_url)
    soup = BeautifulSoup(html,"html.parser")
    lis = soup.find("ul",{"id":"showImg"}).find_all("li")
    #print(lis)
    large_img_urls = []
    count = 1
    picture_num = len(lis)
    while count <= picture_num:
        for li in lis:
            if count > 4:
                img_url = li.find('img', srcs=re.compile('http://.*?\.(.*?)g'))['srcs']      #���jpg��jpeg��png���ָ�ʽ��ͼƬ
            else:
                img_url = li.find('img', src=re.compile('http://.*?\.(.*?)g'))['src']
            count += 1
            #print(img_url)
            large_img_url = img_url.replace('t_s144x90c5','t_s960x600c5')          #�ϳ���һ����ͼƬ·��
            large_img_urls.append(large_img_url)
    return large_img_urls


#***************************************************����ͼƬ********************************************
def download_img(large_img_urls,title_picture_url,picture_book_num,picture_type_location,page_num_dir,zhuti_picture_type_location_of_page):
    global num
    num = 1                    #ͼƬ����,������ü򵥵�����

    title = str(title_picture_url).replace('/', '').replace('*', '').replace('?', '').replace('"', '').replace(':', '').replace('<', '').replace('>', '').replace("|", '')  #ȥ��д���ļ����ⲻ�Ϸ����ַ�
    path_title = os.path.join(zhuti_picture_type_location_of_page, title)              #������ҳĿ¼
    #print(path_title)
    if os.path.exists(path_title):
        return
    else:
        os.mkdir(r'E:\%s\%s\%s'%(picture_type_location,page_num_dir,title))
    for large_img_url in large_img_urls:
        img = requests.get(large_img_url).content
        tmp = str(num)+'.jpg'
        path = os.path.join(path_title,tmp)
        with open(path,'wb') as f:
            f.write(img)
            num += 1


#**************************************ѡ��Ҫ���ص����*******************************************
def choice(type):
    if type == '�羰' or type == 'fengjing':
        type = 'fengjing'
    elif type == '����' or type == 'dongman':
        type = 'dongman'
    elif type == '��Ů' or type == 'meinv':
        type = 'meinv'
    elif type == '����' or type == 'chuangyi':
        type = 'chuangyi'
    elif type == '��ͨ' or type == 'katong':
        type = 'katong'
    elif type == '����' or type == 'qiche':
        type = 'qiche'
    elif type == '��Ϸ' or type == 'youxi':
        type = 'youxi'
    elif type == '�ɰ�' or type == 'keai':
        type = 'keai'
    elif type == '����' or type == 'mingxing':
        type = 'mingxing'
    elif type == '����' or type == 'jianzhu':
        type = 'jianzhu'
    elif type == 'ֲ��' or type == 'zhiwu':
        type = 'zhiwu'
    elif type == '����' or type == 'jingwu':
        type = 'jingwu'
    elif type == '����' or type == 'dongwu':
        type = 'dongwu'
    elif type == 'Ӱ��' or type == 'yingshi':
        type = 'yingshi'
    elif type == '��ģ' or type == 'chemo':
        type = 'chemo'
    elif type == '����' or type == 'tiyu':
        type = 'tiyu'
    elif type == 'Ʒ��' or type == 'pinpai':
        type = 'pinpai'
    elif type == '����' or type == 'xingzuo':
        type = 'xingzuo'
    elif type == '��ʳ' or type == 'meishi':
        type = 'meishi'
    elif type == '����' or type == 'jieri':
        type = 'jieri'
    else:
        type = 'qita'

    return type


#*************************************************����ҳ��С��һҳ�����********************************
def page_num_content(zhuti_url,page_num,picture_book_num,picture_type_location,zhuti_picture_type_location):

    page_num_dir = "��" + str(page_num) + "ҳ"
    zhuti_picture_type_location_of_page = os.path.join(zhuti_picture_type_location, page_num_dir)  # ��������Ŀ¼�µĵڼ�ҳĿ¼
    if os.path.exists(zhuti_picture_type_location_of_page):
        return
    else:
        os.mkdir(r'E:\%s\%s' % (picture_type_location, page_num_dir))
    #print(zhuti_picture_type_location_of_page)
    page_url = zhuti_url +'/' +str(page_num)+'.html'                   #�ض��������ڵ�ַ
    html = getHtml(page_url)
    page_picture = get_Page_Picture_root(html)                  #ͬһҳ,��ͬͼƬ�᲻�����ĵ�ַ�ͱ���,�ֵ�����
    titles = []                                                 #���ͬһҳ,��ͬͼƬ�������
    for title in page_picture.keys():
        titles.append(title)

    list_picture_url = get_list_picture(page_picture,root_url)         #ͬһҳ,��ͬͼƬ�������ĵ�ַ
    count = 1

    len_list = len(list_picture_url)

    if len_list < picture_book_num:                             #�����ж����һҳͼƬ�Ĳ�����û��Ҫ��Ĳ����࣬�����ǲ���������Ҳ����ͼƬ����������Ҫ�����Ŀ
        for picture_url in list_picture_url:
            title_picture_url = titles[count-1]
            large_img_urls = get_detail_picture(picture_url)                              #����ͼƬ��
            download_img(large_img_urls, title_picture_url, picture_book_num, picture_type_location,page_num_dir,zhuti_picture_type_location_of_page)
            count += 1
        print("������˼����Ҫ���ͼƬ��Ŀû����...")

    else:
        for picture_url in list_picture_url:
            title_picture_url = titles[count-1]
            if count<=picture_book_num:                            #�ж��Ƿ�ﵽ����Ҫ�����صĲ���
                large_img_urls = get_detail_picture(picture_url)                              #����ͼƬ��
                download_img(large_img_urls, title_picture_url, picture_book_num, picture_type_location,page_num_dir,zhuti_picture_type_location_of_page)
            else:
                break
            count += 1

#*************************************************����ҳ������һҳ�����********************************
def pages_num_content(zhuti_url,page_num,picture_type_location,zhuti_picture_type_location):

    page_num_unchange = page_num                     #������Ϊ�˷���ҳ��,��Ϊpage_num���ں���仯���������һ����ʱ����������
    for i in range(1,page_num):
        page_num_dir = "��"+str(i)+"ҳ"
        zhuti_picture_type_location_of_page = os.path.join(zhuti_picture_type_location, page_num_dir)  # ��������Ŀ¼�µĵڼ�ҳĿ¼

        if os.path.exists(zhuti_picture_type_location_of_page):
            return
        else:
            os.mkdir(r'E:\%s\%s' % (picture_type_location,page_num_dir))

        page_url = zhuti_url +'/' +str(i)+'.html'                   #�ض��������ڵ�ַ
        #print(page_url)
        html = getHtml(page_url)
        page_picture = get_Page_Picture_root(html)                  #ͬһҳ,��ͬͼƬ�᲻�����ĵ�ַ�ͱ���,�ֵ�����
        titles = []                                                 #���ͬһҳ,��ͬͼƬ�������
        for title in page_picture.keys():
            titles.append(title)
        list_picture_url = get_list_picture(page_picture,root_url)         #ͬһҳ,��ͬͼƬ�������ĵ�ַ

        count = 1
        if page_num >1:
            for picture_url in list_picture_url:
                title_picture_url = titles[count - 1]
                large_img_urls = get_detail_picture(picture_url)                     # ����ͼƬ��
                download_img(large_img_urls, title_picture_url, picture_book_num,picture_type_location,page_num_dir,zhuti_picture_type_location_of_page)
                count += 1
            page_num -= 1
        else:
            break
        titles = []
    return page_num_content(zhuti_url,page_num_unchange,picture_book_num,picture_type_location,zhuti_picture_type_location)


def main(type,page_num,root_url,picture_book_num):
    picture_type_location = type
    type = choice(type)                                               #ѡ��ϵͳ
    zhuti_url = root_url+str(type)                                  #ѡ��������url

    zhuti_picture_type_location = os.path.join('E:\\', picture_type_location)        #��������Ŀ¼
    if os.path.exists(zhuti_picture_type_location):
        #print("Ŀ¼ "+"%s"%zhuti_picture_type_location+"����...")
        return
    else:
        #print("���ڴ���Ŀ¼ "+"%s"%zhuti_picture_type_location+"...")
        os.mkdir(r'E:\%s' % picture_type_location)
    if page_num > 1:
        pages_num_content(zhuti_url,page_num,picture_type_location,zhuti_picture_type_location)
    else:
        page_num_content(zhuti_url,page_num,picture_book_num,picture_type_location,zhuti_picture_type_location)

if __name__ == '__main__':
    print("��ӭ����ͼƬ���ؽ���....")
    print("****************************************")
    print("|                                      |")
    print("|                                      |")
    print("|                                      |")
    print("|             ͼƬ����ϵͳ             |")
    print("|                                      |")
    print("|                                      |")
    print("|                                      |")
    print("****************************************")
    print("--------------------------------------------------------------��ܰ��ʾ------------------------------------------------------------------")
    print("���������ϢӦ����(������Ӧ��ƴ��)���羰,����,��Ů,����,��ͨ,����,��Ϸ,�ɰ�,����,����,ֲ��,����,����,Ӱ��,��ģ,����,Ʒ��,����,��ʳ,����,����")
    type = str(input("��������Ҫ���ص�ͼƬ�����ͣ�"))
    page_num = int(input("��������Ҫ���ص�ҳ����"))
    picture_book_num = int(input("������Ҫ���ص�ҳ�ڲ���(Ĭ�����һҳ��ҳ�ڲ���)��"))
    root_url = 'http://desk.zol.com.cn/'
    start = datetime.now()
    main(type,page_num,root_url,picture_book_num)
    end = datetime.now()
    print("�������...")
    print("�ܺ�ʱΪ��%s"%(end-start))
