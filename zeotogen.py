# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved

This module provide a netSpider for https://zeotogen.blog.fc2.com/

Authors:zhangqi70@baidu.com
Date:2023/08/09
"""
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
from parsel import Selector
from tqdm import tqdm
# import time, random



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
# def GetUrlsPages():
#     url = "https://zeotogen.blog.fc2.com"  # 替换为目标剧本网页的URL
#     ua_list = UserAgent()
#     user_agent = ua_list.random
#     headers = {'User-Agent': user_agent}
#     # 发送网络请求获取HTML内容
#     response = requests.get(url, headers)
#     html = response.text
#     # 使用BeautifulSoup解析HTML内容
#     soup = BeautifulSoup(html, 'html.parser')
#     print("soup:", soup)
#     # 使用CSS选择器选择最后一个pager-item元素
#     last_pager_item = soup.select('.pager-item')[-1]
#     # 从选定的元素中提取数字
#     number = last_pager_item.text.strip()
#     print(number)
#     return number
# 获取所有的剧本信息
def GetDramaInfo():
    """

       Args:

       Returns: 所有剧本的信息

    """
    # 总共302页,动态加载页数无法获取
    for i in tqdm(range(1, 302), desc="Progress"):
        try:
            # 发送网络请求获取HTML内容
            j = 0
            url = "https://zeotogen.blog.fc2.com/page-{}.html".format(i - 1)
            # url = "https://zeotogen.blog.fc2.com"  # 替换为目标剧本网页的URL
            ua_list = UserAgent()
            user_agent = ua_list.random
            headers = {'User-Agent': user_agent}
            response = requests.get(url, headers)
            html = response.text

            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(html, 'html.parser')


            drama_items = soup.select('section.grid-item')

            for item in drama_items:
                # title_element = item.select_one('h2.grid-title a')
                title = item.select_one('h2.grid-title a').get_text()
                category = item.select_one('div.grid-category').get_text().strip('\n')
                description = item.select_one('p.grid-description').get_text().strip('\n').strip()
                time_stamp_str = item.select_one('time.grid-datetime').get('datetime')
                # comment_cnt =
                # 将datetime值转换为时间戳
                # time_stamp = datetime.datetime.strptime(time_stamp_str, "%Y-%m-%dT%M%z").timestamp()
                # title = item.get[""].get_text()  p class="grid-description
                # <a class="grid-a" href="https://zeotogen.blog.fc2.com/blog-entry-1712.html">
                text_url = item.select_one('a.grid-a').get('href')
                # 点赞网页
                # like_url = text_url.replace("https://zeotogen.blog.fc2.com/blog-entry-", "https://blogvote.fc2.com/pickup/zeotogen/")
                # original_url = "https://zeotogen.blog.fc2.com/blog-entry-1704.html"

                # 提取 blog-entry-1704 部分
                entry_number = text_url.split("/")[-1].split(".")[0].split("-")[-1]
                # print(entry_number)

                # 提取 zeotogen 部分
                web_site_name = text_url.split("//")[1].split(".")[0]
                # print(web_site_name)

                # 点赞的URL
                # like_url = f"https://blogvote.fc2.com/pickup/{web_site_name}/{entry_number}/clap"
                like_url = "https://blogvote.fc2.com/pickup/{}/{}/clap".format(web_site_name, entry_number)
                user_agent_like = ua_list.random
                headers_like = {'User-Agent': user_agent_like}
                response_like = requests.get(like_url, headers_like)
                html_like = response_like.text

                # 使用BeautifulSoup解析HTML内容
                soup_like = BeautifulSoup(html_like, 'html.parser')
                like_cnt = soup_like.select('div.clap_total_count span.clap_num')[0].text

                # url = 'https://zeotogen.blog.fc2.com/blog-entry-1457.html'
                html = GetHtml(text_url)
                cssText = '#inner-contents blockquote *::text'
                texts = GetInformation(html, cssText)
                # with open('text.txt', 'w', encoding='utf-8') as fd:
                #     fd.write(''.join(texts))

                # print(texts)
                newText = [str.strip(text).replace('\u3000', '') for text in texts]
                Dialogs = []
                roleId = 'A'
                flag = False
                GetNameFlag = True
                Names = []

                for i in range(len(newText)):
                    text = newText[i]
                    if text[:-1] == '：' and GetNameFlag:
                        Names.append(text + newText[i + 1])
                    if '**' in text and GetNameFlag:
                        GetNameFlag = False

                    try:
                        if text[-1] == '「':
                            roleId = text[0]
                            DiaGue = ''
                            flag = True
                            newDialog = {}
                        elif text[-1] == '」':
                            newDialog[roleId] = DiaGue

                            flag = False
                            Dialogs.append(newDialog)

                        elif flag:
                            DiaGue += text
                    except:
                        pass
                # 将相关信息写入JSON文件
                drama_info = {
                    "title": title,
                    "category": category,
                    "description": description,
                    "time_stamp_str": time_stamp_str,
                    "text_url": text_url,
                    "like_cnt": like_cnt,
                    "text": texts,
                    "dialogue": Dialogs
                }

                with open('zeotogen_dramas.json', 'a', encoding='utf-8') as f:
                    json.dump(drama_info, f, ensure_ascii=False)
                    f.write('\n')
                j += 1
                if (i % 5) == 0:
                    progress_desc = "Progress: 爬取进度为{:.2f}%,共爬取了{}个剧本".format(i / 302 * 100, j)
                    tqdm.write(progress_desc, end='\r')
        except Exception as e:
            print('Error:', e)
            pass
        finally:
            print('finally...')
            pass

if __name__ == '__main__':
    # print("1111")
    GetDramaInfo()
    # GetUrlsPages()
    # ==================




