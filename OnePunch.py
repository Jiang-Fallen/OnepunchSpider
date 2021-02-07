#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
import  re
import os

_start_index = 1
_end_index = 183

_base_url = 'https://www.fzdm.com/manhua/132/'
_img_base_url = 'https://p5.manhuapan.com/'

def getUrlWithIndex(index):
    return _base_url + '%03d/' % index

def getImgName(page_index, img_index):
    return 'onepunch%03d_%d.jpg'%(page_index, img_index)

def downloadImage(imgUrl, imgName):
    # download path
    print('开始下载：' + imgName)
    save_path = './onepunch/'
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file_path = save_path + imgName
        r = requests.get(imgUrl)
        # 使用with语句可以不用自己手动关闭已经打开的文件流
        with open(file_path, "wb") as f:  # 开始写文件，wb代表写二进制文件
            print('下载完成：' + imgName)
            f.write(r.content)
    except IOError as e:
        print('文件操作失败', e)
    except Exception as e:
        print('下载图片错误', e)

def fetchComic(url, page_index):
    next_name = '下一页'
    next_html = ''
    cur_index = 1

    while next_name == '下一页':
        print('正在获取 %d章, %d节漫画' % (page_index, cur_index))
        request_url = url + next_html
        result = requests.get(request_url)
        soup_temp = BeautifulSoup(result.content, 'lxml')
        navi = soup_temp.findAll('div', {'class': 'navigation'})[0]
        soup_next = navi.findAll('a')[-1]

        # 下一个漫画页
        next_html = soup_next.get('href')
        next_name = soup_next.get_text()

        # 获取 image url
        soup_temp.script.decompose()
        img_path = re.search(r'\bmhurl="(.+?\.jpg)";', soup_temp.get_text())
        img_url = _img_base_url + img_path.group(1)
        downloadImage(img_url, getImgName(page_index, cur_index))
        cur_index += 1

def fetchPageUrl():
    for i in range(_start_index, _end_index + 1):
        url = getUrlWithIndex(i)
        fetchComic(url, i)


if __name__ == "__main__":
    fetchPageUrl()
