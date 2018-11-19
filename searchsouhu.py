__author__ = "xumeng"
__date__ = "2018/11/19 15:00"
from urllib import parse
import re
from selenium import webdriver

'''
视频搜索-搜狐视频免费观看网址

'''


class Spider():

    # 解析vip视频的url
    vip_url = 'https://cdn.yangju.vip/k/?url='
    # 搜狐视频搜索网址
    source_url = "https://so.tv.sohu.com/mts?wd="
    root_pattern = r'<div class="series cfix">[\w\W]*?</div>'
    goal_name_pattern = r'title="([\w\W]*?)">'
    goal_url_pattern = r'<a class="" href="//([\w\W]*?)" target'

    def __input_video(self):
        wd = input('请输入视频名字：')
        wd = parse.unquote(wd)
        url = Spider.source_url + wd
        return url

    def __get_content(self, url):
        '''
        获取网页信息，返回字符串型网页内容
        '''
        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.get(url)
        html = driver.page_source
        html = parse.unquote(html)
        return html

    def __analysis(self, html):
        root_html = re.findall(Spider.root_pattern, html)
        root_html = str(root_html)
        video_lists = []
        goal_names = re.findall(Spider.goal_name_pattern, root_html)
        goal_urls = re.findall(Spider.goal_url_pattern, root_html)
        for i in range(0, len(goal_names)):
            dic = dict()
            dic['name'] = goal_names[i]
            dic['url'] = 'https://' + goal_urls[i]
            if '预告' not in goal_names[i]:
                if len(goal_names[i]) > 2:
                    video_lists.append(dic)
        return video_lists

    def __refine(self, lists):
        for lis in lists:
            lis["url"] = (Spider.vip_url + lis["url"].strip())
        return lists

    def __my_print(self, lists):
        for lis in lists:
            print(lis['name'] + '\t' + lis['url'])

    def go(self):
        url = self.__input_video()
        html = self.__get_content(url)
        html = self.__analysis(html)
        video_lists = self.__refine(html)
        self.__my_print(video_lists)


spider = Spider()
spider.go()
