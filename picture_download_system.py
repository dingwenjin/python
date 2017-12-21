import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import os

def getHtml(url):
    header  = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
    html = requests.get(url,headers=header).content.decode('gb2312','ignore').encode('utf-8')
    return html


#****************************************获取对应主题的不同图片册不完全地址入口*******************************
def get_Page_Picture_root(html):
    soup = BeautifulSoup(html,"html.parser")
    lis = soup.find_all("li",{"class":"photo-list-padding"})
    titles = []
    urls = []
    page_picture = {}
    for li in lis:
        url = li.find("a")['href']               #不完全的url
        #print(url)
        urls.append(url)
        title = li.find('span')['title']
        #print(title)
        titles.append(title)
    page_picture = dict(zip(titles,urls))
    return page_picture


#*********************************************图片册入口,返回不同图片册的完整url列表************************************
def get_list_picture(page_picture,root_url):
    list_picture_url = []
    for url in page_picture.values():                    #不同图片册的不完整url
        full_detail_url = root_url+url                        #合成图片册完整的url
        #print(full_detail_url)                                 #图片册url
        list_picture_url.append(full_detail_url)
    #print("\n\n")
    return list_picture_url

#************************************获取相同图片册的不同图片**************************************
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
                img_url = li.find('img', srcs=re.compile('http://.*?\.(.*?)g'))['srcs']      #解决jpg、jpeg和png三种格式的图片
            else:
                img_url = li.find('img', src=re.compile('http://.*?\.(.*?)g'))['src']
            count += 1
            #print(img_url)
            large_img_url = img_url.replace('t_s144x90c5','t_s960x600c5')          #合成另一个大图片路径
            large_img_urls.append(large_img_url)
    return large_img_urls


#***************************************************下载图片********************************************
def download_img(large_img_urls,title_picture_url,picture_book_num,picture_type_location,page_num_dir,zhuti_picture_type_location_of_page):
    global num
    num = 1                    #图片名字,这里采用简单的数字

    title = str(title_picture_url).replace('/', '').replace('*', '').replace('?', '').replace('"', '').replace(':', '').replace('<', '').replace('>', '').replace("|", '')  #去掉写入文件标题不合法的字符
    path_title = os.path.join(zhuti_picture_type_location_of_page, title)              #创建到页目录
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


#**************************************选择要下载的题材*******************************************
def choice(type):
    if type == '风景' or type == 'fengjing':
        type = 'fengjing'
    elif type == '动漫' or type == 'dongman':
        type = 'dongman'
    elif type == '美女' or type == 'meinv':
        type = 'meinv'
    elif type == '创意' or type == 'chuangyi':
        type = 'chuangyi'
    elif type == '卡通' or type == 'katong':
        type = 'katong'
    elif type == '汽车' or type == 'qiche':
        type = 'qiche'
    elif type == '游戏' or type == 'youxi':
        type = 'youxi'
    elif type == '可爱' or type == 'keai':
        type = 'keai'
    elif type == '明星' or type == 'mingxing':
        type = 'mingxing'
    elif type == '建筑' or type == 'jianzhu':
        type = 'jianzhu'
    elif type == '植物' or type == 'zhiwu':
        type = 'zhiwu'
    elif type == '静物' or type == 'jingwu':
        type = 'jingwu'
    elif type == '动物' or type == 'dongwu':
        type = 'dongwu'
    elif type == '影视' or type == 'yingshi':
        type = 'yingshi'
    elif type == '车模' or type == 'chemo':
        type = 'chemo'
    elif type == '体育' or type == 'tiyu':
        type = 'tiyu'
    elif type == '品牌' or type == 'pinpai':
        type = 'pinpai'
    elif type == '星座' or type == 'xingzuo':
        type = 'xingzuo'
    elif type == '美食' or type == 'meishi':
        type = 'meishi'
    elif type == '节日' or type == 'jieri':
        type = 'jieri'
    else:
        type = 'qita'

    return type


#*************************************************下载页数小于一页的情况********************************
def page_num_content(zhuti_url,page_num,picture_book_num,picture_type_location,zhuti_picture_type_location):

    page_num_dir = "第" + str(page_num) + "页"
    zhuti_picture_type_location_of_page = os.path.join(zhuti_picture_type_location, page_num_dir)  # 创建主题目录下的第几页目录
    if os.path.exists(zhuti_picture_type_location_of_page):
        return
    else:
        os.mkdir(r'E:\%s\%s' % (picture_type_location, page_num_dir))
    #print(zhuti_picture_type_location_of_page)
    page_url = zhuti_url +'/' +str(page_num)+'.html'                   #特定主题的入口地址
    html = getHtml(page_url)
    page_picture = get_Page_Picture_root(html)                  #同一页,不同图片册不完整的地址和标题,字典类型
    titles = []                                                 #存放同一页,不同图片册的名称
    for title in page_picture.keys():
        titles.append(title)

    list_picture_url = get_list_picture(page_picture,root_url)         #同一页,不同图片册完整的地址
    count = 1

    len_list = len(list_picture_url)

    if len_list < picture_book_num:                             #用于判断最后一页图片的册数有没有要求的册数多，这里是册数不够，也就是图片数不够用于要求的数目
        for picture_url in list_picture_url:
            title_picture_url = titles[count-1]
            large_img_urls = get_detail_picture(picture_url)                              #单个图片册
            download_img(large_img_urls, title_picture_url, picture_book_num, picture_type_location,page_num_dir,zhuti_picture_type_location_of_page)
            count += 1
        print("不好意思，您要求的图片数目没有了...")

    else:
        for picture_url in list_picture_url:
            title_picture_url = titles[count-1]
            if count<=picture_book_num:                            #判断是否达到用于要求下载的册数
                large_img_urls = get_detail_picture(picture_url)                              #单个图片册
                download_img(large_img_urls, title_picture_url, picture_book_num, picture_type_location,page_num_dir,zhuti_picture_type_location_of_page)
            else:
                break
            count += 1

#*************************************************下载页数大于一页的情况********************************
def pages_num_content(zhuti_url,page_num,picture_type_location,zhuti_picture_type_location):

    page_num_unchange = page_num                     #这里是为了返回页数,因为page_num会在后面变化，因此设置一个临时变量保存它
    for i in range(1,page_num):
        page_num_dir = "第"+str(i)+"页"
        zhuti_picture_type_location_of_page = os.path.join(zhuti_picture_type_location, page_num_dir)  # 创建主题目录下的第几页目录

        if os.path.exists(zhuti_picture_type_location_of_page):
            return
        else:
            os.mkdir(r'E:\%s\%s' % (picture_type_location,page_num_dir))

        page_url = zhuti_url +'/' +str(i)+'.html'                   #特定主题的入口地址
        #print(page_url)
        html = getHtml(page_url)
        page_picture = get_Page_Picture_root(html)                  #同一页,不同图片册不完整的地址和标题,字典类型
        titles = []                                                 #存放同一页,不同图片册的名称
        for title in page_picture.keys():
            titles.append(title)
        list_picture_url = get_list_picture(page_picture,root_url)         #同一页,不同图片册完整的地址

        count = 1
        if page_num >1:
            for picture_url in list_picture_url:
                title_picture_url = titles[count - 1]
                large_img_urls = get_detail_picture(picture_url)                     # 单个图片册
                download_img(large_img_urls, title_picture_url, picture_book_num,picture_type_location,page_num_dir,zhuti_picture_type_location_of_page)
                count += 1
            page_num -= 1
        else:
            break
        titles = []
    return page_num_content(zhuti_url,page_num_unchange,picture_book_num,picture_type_location,zhuti_picture_type_location)


def main(type,page_num,root_url,picture_book_num):
    picture_type_location = type
    type = choice(type)                                               #选择系统
    zhuti_url = root_url+str(type)                                  #选择的主题的url

    zhuti_picture_type_location = os.path.join('E:\\', picture_type_location)        #创建主题目录
    if os.path.exists(zhuti_picture_type_location):
        #print("目录 "+"%s"%zhuti_picture_type_location+"存在...")
        return
    else:
        #print("正在创建目录 "+"%s"%zhuti_picture_type_location+"...")
        os.mkdir(r'E:\%s' % picture_type_location)
    if page_num > 1:
        pages_num_content(zhuti_url,page_num,picture_type_location,zhuti_picture_type_location)
    else:
        page_num_content(zhuti_url,page_num,picture_book_num,picture_type_location,zhuti_picture_type_location)

if __name__ == '__main__':
    print("欢迎进入图片下载界面....")
    print("****************************************")
    print("|                                      |")
    print("|                                      |")
    print("|                                      |")
    print("|             图片下载系统             |")
    print("|                                      |")
    print("|                                      |")
    print("|                                      |")
    print("****************************************")
    print("--------------------------------------------------------------温馨提示------------------------------------------------------------------")
    print("您输入的信息应该是(包括对应的拼音)：风景,动漫,美女,创意,卡通,汽车,游戏,可爱,明星,建筑,植物,静物,动物,影视,车模,体育,品牌,星座,美食,节日,其它")
    type = str(input("请输入您要下载的图片的类型："))
    page_num = int(input("请输入您要下载的页数："))
    picture_book_num = int(input("请输入要下载的页内册数(默认最后一页的页内册数)："))
    root_url = 'http://desk.zol.com.cn/'
    start = datetime.now()
    main(type,page_num,root_url,picture_book_num)
    end = datetime.now()
    print("下载完毕...")
    print("总耗时为：%s"%(end-start))
