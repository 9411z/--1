# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved

This module provide a netSpider for https://www.no-ichigo.jp/search

Authors:zhangqi70@baidu.com
Date:2023/08/10
"""
import os.path

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
from parsel import Selector
from tqdm import tqdm
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import re
import datetime
import itertools


# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions


# def GetHtml_run(url):
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option("detach", True)
#     options.add_argument(f'user-agent={UserAgent().random}')
#     service = Service(executable_path='/Users/yanghao31/Desktop/software/chromedriver_mac_arm64/chromedriver')
#     driver = webdriver.Chrome(service=service)
#     print('准备完毕')
#
#     # 设置页面加载超时时间为10秒钟
#     driver.set_page_load_timeout(30)
#
#     try:
#         driver.get(url)
#         # 等待页面完全加载完成
#         driver.implicitly_wait(30)
#         # WebDriverWait(driver, 30).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#         html = driver.page_source
#     except TimeoutException:
#         print("页面加载超时")
#         html = ''
#     driver.quit()
#     return html


def GetHtml_run(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument(f'user-agent={UserAgent().random}')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    # print('准备完毕')

    # 设置页面加载超时时间为10秒钟
    driver.set_page_load_timeout(30)
    bigHtml=''

    try:
        driver.get(url)
        # 等待页面完全加载完成
        driver.implicitly_wait(30)
        # WebDriverWait(driver, 30).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        html = driver.page_source
        bigHtml+=html
    except TimeoutException:
        print("页面加载超时")
        html = ''

    # js = "window.scrollTo(0, document.body.scrollHeight)"
    # driver.execute_script(js)  # 模拟鼠标滚轮，滑动页面至底部

    driver.quit()
    return bigHtml
def GetHtml2(url):
    maxnum = 3
    for i in range(maxnum):
        time.sleep(random.random()*0.4 + 0.2)
        try:
            ip, port = 'i652.kdltps.com', 15818
            headers = {'User-Agent': UserAgent().random}
            proxies = {'http': 'http://{}:{}@{}:{}'.format('t18976558949721', 'wb5x8c6w', ip, port),
                       'https': 'http://{}:{}@{}:{}'.format('t18976558949721', 'wb5x8c6w', ip, port)}
            session = requests.session()
            session.headers.update(headers)
            session.proxies.update(proxies)
            session.keep_alive = False

            res = session.get(url, timeout=10)
            if res.status_code == 200 or res.status_code == 304:
                return res.text
            else:
                print(res.status_code)

        except  Exception as e:
            print(e)
            print(url)

        print('失败{}次'.format(i))
        time.sleep(random.random() * 2)
    return ''

def GetHtml(url):
    """

    Args:
        url: 请求的url

    Returns: 请求的响应

    """
    try:
        res = requests.get(url, headers={'user-agent': UserAgent().random})
        if res.status_code == 200:
            return res.text
        else:
            print(res.status_code)

    except  Exception as e:
        print(e)
        print(url)


def GetInformation(html, cssString):
    """

       Args:
           html: 请求的响应
           cssString: css的值

       Returns: 解析的结果

    """
    sel = Selector(text=html)
    items = sel.css(cssString).getall()
    return items
def GetUrlsPages(url):
    # url = "https://zeotogen.blog.fc2.com"  # 替换为目标剧本网页的URL
    html = GetHtml(url)
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html, 'html.parser')

    # 找到包含页码的HTML元素（这里以li标签为例）
    page_list = soup.find('div', class_='pageList').find_all('li')

    # 初始化最大页数为0
    max_page = 0

    # 遍历页码元素，找出最大的页数
    print("len(page_list):", len(page_list))
    for li in page_list:
        # 判断是否包含页码数字
        if li.find('a'):
            page_num = int(li.find('a').text)
            if page_num > max_page:
                max_page = page_num

    print("最大页数:", max_page)
    return max_page
# 获取所有的剧本信息
def GetnovelInfo(novel_category, novel_url):
    """

       Args:

       Returns: 所有剧本的信息

    """

    # url1 = "https://www.no-ichigo.jp/love"
    # counter = itertools.count()
    progress_bar = tqdm()
    i = 3269
    while True:
        try:
            # 发送网络请求获取HTML内容
            url = novel_url.format(i)
            response = GetHtml_run(url)
            pattern = re.compile('<div class="item">(.*?)</div>', re.S)
            # 这个类型的小说一页有多少个
            novel_items = re.findall(pattern, response)
            print("len:", len(novel_items))
            print("i:", i)
            # iteration = next(counter)
            # 打印进度和提示信息
            progress_bar.set_description('进度:正在下载第{}本小说'.format(i))
            progress_bar.update(1)  # 更新进度条
            if len(novel_items) < 1:
                break
            i = i + 1
            print("i:", i)

            k = 1
            for item in novel_items:
                # 提取URL
                url_pattern = re.compile('<a href="(.*?)">', re.S)
                url_match = re.search(url_pattern, item)
                text_url = url_match.group(1)
                k = k + 1
                if k == 5:
                    break

                # print("URL:", url)
                # response_text = GetHtml_run(text_url)
                # pattern_link = r'<a\s+href="(.*?)">.*?</a>'
                # link_match = re.search(pattern_link, response_text)
                # if link_match:
                #     link = link_match.group(1)
                # else:
                #     break
                content_url = text_url.replace('/read/book/book_id/', '/book/n') + "/"
                # 提取标题
                title_pattern = re.compile(r'<a.*?>(.*?)\s*</a>', re.S)
                title_match = re.search(title_pattern, item)
                # title = title_match.group(1)
                if title_match:
                    title = title_match.group(1)
                    # print("标题:", title)
                else:
                    # print("未找到标题")
                    title = "未找到标题"
                # print("标题:", title)
                # return
                novel_html = GetHtml_run(text_url)
                pattern_time = re.compile('最終更新日<br>\s*(.*?)\s*</p>', re.S)
                match = pattern_time.search(novel_html)

                if match:
                    date_str = match.group(1)
                    mod_time_stamp_str = datetime.datetime.strptime(date_str, "%Y/%m/%d")
                    mod_time_stamp = int(mod_time_stamp_str.timestamp())
                else:
                    mod_time_stamp_str = "0"
                    mod_time_stamp = 0

                # pattern_kind = re.compile(r'ジャンル/(.*?)<br>')
                # match = pattern.search(novel_html)

                category_pattern = re.compile(r'ジャンル/(.*?)<br>', re.S)
                category_match = re.search(category_pattern, novel_html)

                if category_match:
                    category = category_match.group(1).strip()
                else:
                    category = novel_category
                lang = "Japanese"

                pattern_like = re.compile(r'<span class="balloonInner like">(\d+)</span>')
                match = pattern_like.search(novel_html)

                if match:
                    like_nums = int(match.group(1))
                    # print(number)  # 输出结果为 "0"
                else:
                    like_nums = 0
                # pattern_charpter = re.compile(r'<a href="(.*?)">(Chapter\d+)[□■](.*?)</a>')
                #
                # matches = pattern_charpter.findall(novel_html)
                # chapter_links = []
                #
                # for match in matches:
                #     chapter_link = {
                #         'title': match[1] + ":" + match[2],
                #         'link': match[0]
                #     }
                #     chapter_links.append(chapter_link)
                # page_numbers = []
                # pattern_pages = r'/(\d+)$'
                # is_first_page = True
                # total_pages = 0
                # for chapter in chapter_links:
                #     if is_first_page:
                #         htlm_pages1 = GetHtml_run(chapter['link'])
                #         pattern = r'\((\d+)/(\d+)\)'
                #         match = re.search(pattern, htlm_pages1)
                #
                #         if match:
                #             total_pages = match.group(2)
                #             print(total_pages)
                #         else:
                #             total_pages = 0
                #             print("未找到匹配的内容")
                #     print(f"Title: {chapter['title']}")
                #     print(f"Link: {chapter['link']}")
                #     match = re.search(pattern_pages, chapter['link'])
                #     if match:
                #         number = match.group(1)
                #         page_numbers.append(number)
                j = 1
                while True:
                    next_page_url = content_url + "{}".format(j)
                    # one_page_html = GetHtml_run(next_page_url)
                    # if one_page_html:
                    #     pattern_text = r'<div>(.*?)</div>'
                    #     result = re.search(pattern_text, one_page_html, re.DOTALL)
                    one_page_html = GetHtml_run(next_page_url)
                    # one_charpter_text = ""
                    text = ""
                    if one_page_html:
                        # pattern_text = '</div>\s*</aside>\s*<div>(.*?)</div>'
                        # result = re.search(pattern_text, one_page_html, re.DOTALL)
                        cssText = '.page.bookText div *::text'
                        result = GetInformation(one_page_html, cssText)

                        if result:
                            # extracted_text = result.group(1)
                            # print(''.join(result))
                            # ''.join(lst)
                            text += ''.join(result)
                            # print("result:", result)
                        else:
                            print("result:")
                            break
                        j = j + 1
                        if j == 5:
                            break
                # for j, chapter in range(chapter_links):
                #     one_charpter_text = ""
                #     while (j + 1) < page_numbers[j]:
                #         if j == 0:
                #             next_page_url = chapter['link']
                #         else:
                #             charpter_first_page_url = chapter['link']
                #             slash_index = charpter_first_page_url.rfind('/')
                #             base_url = charpter_first_page_url[:slash_index + 1]
                #             next_page_url = base_url.format(j+1)
                #         one_page_html = GetHtml_run(next_page_url)
                #         if one_page_html:
                #             pattern_text = r'<div>(.*?)</div>'
                #             result = re.search(pattern_text, one_page_html, re.DOTALL)
                #             if result:
                #                 extracted_text = result.group(0)
                #                 print(extracted_text)
                #             else:
                #                 print("No match found.")
                #             one_charpter_text += extracted_text
                #         else:
                #             break

                novel_info = {
                    "title": title,
                    # "charpter_title": chapter['title'],
                    "category": category,
                    # "mod_time_stamp_str": mod_time_stamp_str,
                    "mod_time_stamp": mod_time_stamp,
                    # "text_url": chapter['link'],
                    "like_nums": like_nums,
                    "text": text,
                    "lang": lang
                }
                dir = "./novels"
                if not os.path.exists(dir):
                    os.makedirs(dir)

                file_name = "./novels/" + title + ".json"
                # if os.path.exists(file_name):
                #     os.remove(file_name)
                with open(file_name, 'a+', encoding='utf-8') as f:
                    json.dump(novel_info, f, ensure_ascii=False)
                    f.write('\n')

                    #     one_charpter_text += extracted_text
                    # novel_info = {
                    #     "title": title,
                    #     "charpter_title": chapter['title'],
                    #     "category": category,
                    #     "mod_time_stamp_str": mod_time_stamp_str,
                    #     "mod_time_stamp": mod_time_stamp,
                    #     "text_url": chapter['link'],
                    #     "like_nums": like_nums,
                    #     "text": one_charpter_text,
                    # }
                    # file_name = title + ".json"
                    # with open(file_name, 'a', encoding='utf-8') as f:
                    #     json.dump(novel_info, f, ensure_ascii=False)
                    #     f.write('\n')
        except Exception as e:
            print('Error:', e)
            pass
        finally:
            print('finally...')
            pass
def GetAllKindsNovels():
    domainUrl = {
        "恋愛": "https://www.no-ichigo.jp/love",  # 恋爱关系
        "青春・友情": "https://www.no-ichigo.jp/friend",  # 青春、友谊
        "ノンフィクション・実話": "https://www.no-ichigo.jp/nonfic",  # 非虚构、真实故事
        "ミステリー・サスペンス": "https://www.no-ichigo.jp/mystery",  # 神秘悬念 "
        "ホラー・オカルト": "https://www.no-ichigo.jp/horror",  # 恐怖/神秘
        "ファンタジー<": "https://www.no-ichigo.jp/fantasy",  # 幻想
        "歴史・時代": "https://www.no-ichigo.jp/history",  # >历史/时代
         "コメディ": "https://www.no-ichigo.jp/comedy",  # 喜剧
        "絵本・童話": "https://www.no-ichigo.jp/fairy",  # 图画书/童话故事
        "実用・エッセイ": "https://www.no-ichigo.jp/essay",  # 实践/论文
        "詩・短歌・俳句・川柳": "https://www.no-ichigo.jp/poetry",  # 诗歌、短歌、俳句、千流
        "その他": "https://www.no-ichigo.jp/other",  # 其他的
    }
    # for
    for key, value in domainUrl.items():
        GetnovelInfo(key, value)

if __name__ == '__main__':
    # print("1111")
    # GetnovelInfo()
    # GetUrlsPages("https://www.no-ichigo.jp/read/book/book_id/1276517")
    # ==================
    # HTML = GetHtml_run("https://www.no-ichigo.jp/read/book/book_id/1276517")
    # # # print("HTML:", HTML)
    # # file_name = "./novel.txt"
    # # with open(file_name, "w", encoding="utf-8") as file:
    # #     file.write(HTML)
    # # html = '''
    # <a href="" class="good-poll-register btnBookLikeOn" data-book-id="1276517" data-url="/web-api/book/n1276517/good/poll">
    #     <span class="text">いいね！する</span>
    #     <span class="balloon"><span class="balloonInner like">15</span></span>
    # </a>
    # '''
    #
    # soup = BeautifulSoup(html, 'html.parser')
    # number_element = soup.find('span', class_='balloonInner like')
    #
    # if number_element:
    #     number = number_element.text
    #     print(number)  # 输出结果为 "0"
    # else:
    #     print("未找到匹配的字符串")
    # pattern_charpter = re.compile(r'<a href="(.*?)">(Chapter\d+)[□■](.*?)</a>')
    #
    # matches = pattern_charpter.findall(HTML)
    # chapter_links = []
    #
    # for match in matches:
    #     chapter_link = {
    #         'title': match[1] + ":" + match[2],
    #         'link': match[0]
    #     }
    #     chapter_links.append(chapter_link)
    # chapter_links.sort(key=lambda x: int(re.search(r'\d+', x['title']).group()))  # 按照数字排序
    #
    # for chapter in chapter_links:
    #     print(f"Title: {chapter['title']}")
    #     print(f"Link: {chapter['link']}")
    # HTML = GetHtml_run("https://www.no-ichigo.jp/read/book/book_id/1276517")
    # # print("HTML:", HTML)
    # file_name = "./novel.txt"
    # with open(file_name, "w", encoding="utf-8") as file:
    #     file.write(HTML)
    # html = '''

    # 使用itertools.count()创建一个无限迭代器

    GetAllKindsNovels()
    # 创建tqdm进度条对象

    # ttps: // www.no - ichigo.jp / read / book / book_id / 1240311
    # urls = [
    #     "https://www.no-ichigo.jp/book/n1276517/18",
    #     "https://www.no-ichigo.jp/book/n1276517/19",
    #     "https://www.no-ichigo.jp/book/n1276517/20"
    # ]
    #
    # pattern = r'/(\d+)$'
    #
    # numbers = []
    #
    # for url in urls:
    #     match = re.search(pattern, url)
    #     if match:
    #         number = match.group(1)
    #         numbers.append(number)

    #####=========

    # text = '''<div>騒動から半年経った今は順調に、それもいつも通りに日々を過ごしていた。<br>
    # <br>
    # 「社長、コーヒーです」<br>
    # <br>
    # 私は上司である名取竜馬（ﾅﾄﾘﾘｭｳﾏ）のデスクにコーヒーを置いた。<br>
    # <br>
    # 「どうも、だけど２人だけの時は“お兄ちゃん”って呼んでもいいんだぞ？」<br>
    # <br>
    # 彼はそう言った後、コーヒーをすすった。<br>
    # <br>
    # 「いいえ、社長のことをそう呼ぶ訳にはいきません。<br>
    # <br>
    # プライベートでは兄妹かも知れませんが、会社では上司と部下です」<br>
    # <br>
    # そう言い返した私に、<br>
    # 「桃子ちゃん、顔が怖いよ。<br>
    # <br>
    # 元はとても美人なんだから、怖い顔してたら逃げられちゃうよ」<br>
    # <br>
    # 竜馬は笑いながら言い返した。<br>
    # <br>
    # 「お世辞でもありがとうございます。<br>
    # <br>
    # ではまだ仕事が残っているので失礼します。<br>
    # <br>
    # 隣の秘書室にいますので、何かご用がありましたら」<br>
    # <br>
    # 私は会釈をすると、社長室から立ち去った。</div>'''
    #
    # pattern = r'<div>(.*?)</div>'
    # result = re.search(pattern, text, re.DOTALL)
    #
    # if result:
    #     extracted_text = result.group(0)
    #     print(extracted_text)
    # else:
    #     print("No match found.")


    # HTML = GetHtml_run("https://www.no-ichigo.jp/book/n1276517/1")
    # # print("HTML:", HTML)
    # file_name = "./cha1.txt"
    # # with open(file_name, "w", encoding="utf-8") as file:
    # #     file.write(HTML)
    # pattern = r'\((\d+)/(\d+)\)'
    # match = re.search(pattern, HTML)
    #
    # if match:
    #     total_pages = match.group(2)
    #     print(total_pages)
    # else:
    #     print("未找到匹配的内容")
    # print("1111111")
    # # GetAllKindsNovels()
    #
    # url = "https://www.no-ichigo.jp/book/n762593"
    # # url = "https://www.no-ichigo.jp/book/n1276517/18"
    #
    # one_page_html = GetHtml_run(url)
    # one_charpter_text = ""
    # extracted_text = ""
    # if one_page_html:
    #     #pattern_text = '</div>\s*</aside>\s*<div>(.*?)</div>'
    #     #result = re.search(pattern_text, one_page_html, re.DOTALL)
    #     cssText='.page.bookText div *::text'
    #     result=GetInformation(one_page_html,cssText)
    #
    #     if result:
    #         #extracted_text = result.group(1)
    #         print(''.join(result))
    #         print("extracted_text:", extracted_text)
    #     else:
    #         print("no extracted_text:")
    #     # text_content = []
    #     # for text_match in text_matches:
    #     #     text_content.append(text_match.strip())
    #     #
    #     # print("1111:", text_content)
    #     # pattern_text = r'<\/div>\s+<\/aside>\s+<div>(.*?)<\/div>'
    #     # result = re.search(pattern_text, one_page_html, re.DOTALL)
    #     # if result:
        #     extracted_text = result.group(0)
        #     print("extracted_text:", extracted_text)
        #     # print(""extracted_text)
        # else:
        #     print("No match found.")
        # one_charpter_text += extracted_text
        # pattern_br = r'<br />\s*'
        # pattern_text = r'>(.*?)<br />'
        #
        # br_matches = re.findall(pattern_br, one_page_html)
        # text_matches = re.findall(pattern_text, one_page_html)
        #
        # br_tags = len(br_matches)
        # text_content = [text.strip() for text in text_matches]

        # print("Number of <br> tags:", br_tags)
        # print("Text content:")
        # for content in text_content:
        #     one_charpter_text += content
        #     # print(content)
    # else:
    #     print("None.")
    # print("one_charpter_text:", one_charpter_text)
    # print("text_content:", text_content)



