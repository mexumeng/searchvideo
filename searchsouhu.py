__author__ = "xumeng"
__date__ = "2018/11/19 15:00"
from urllib import parse
import re
import time
import datetime
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
'''
视频搜索-vip视频免费观看网址

'''


class Spider():

    # 解析vip视频的url
    vip_url = 'https://yangju.vip/vip/?url='
    # 搜狐视频搜索网址
    source_url = "https://so.tv.sohu.com/mts?wd="
    # root_pattern = r'<div class="series cfix">[\w\W]*?</div>'
    root_pattern = r'<div class="siteSeries cfix">[\w\W]*?</div>'
    goal_name_pattern = r'title="([\w\W]*?)"'
    goal_name_pattern2 = r'data-title="([\w\W]*?)" data-vinfo'
    goal_url_pattern = r'href="//([\w\W]*?)"'
    goal_url_pattern2 = r'data-url="//([\w\W]*?)" pb-url'
    second_page_pattern = r'<h2>[\w\W]*?</h2>'
    filename_pattern = r'title="([\W\w]*?)" target'

    def __input_video(self):
        wd = input('请输入视频名字：')
        wd = parse.unquote(wd)
        url = Spider.source_url + wd
        return url

    def __get_content(self, url):
        '''
        获取网页信息，返回字符串型网页内容
        '''
        options = Options()
        options.add_argument('-headless')  # 无头参数
        driver = Firefox(executable_path='geckodriver', firefox_options=options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径
        driver.get(url)
        html = driver.page_source
        html = parse.unquote(html)
        driver.quit()
        return html

    def __analysisyouku(self, html):
        # 针对优酷的分析爬取
        root2html = re.findall(self.second_page_pattern,str(html))
        # reses = re.findall(r'href="//([\w\W]*?)" title',str(roothtml))
        name_urls = []
        for r in root2html:
            sec_url = re.findall(r'href="//([\w\W]*?)" title',r)[0]
            ahead_name = re.findall(self.filename_pattern,r)[0]
            name_url = {ahead_name:sec_url}
            name_urls.append(name_url)
        video_num_pattern = r'target="_blank">(\w*?)</a>'
        video_url_pattern = r'href="//([\w\W]*?);'
        video_urls = []
        for res in name_urls:
            for name,url in res.items():
                url = "https://"+url
                ahead_name = name
            html = self.__get_content(url)
            all_content = re.findall(r'episode cfix[\w\W]*?</div>',html)
            all_content = str(all_content)
            nums = re.findall(video_num_pattern,all_content)
            urls = re.findall(video_url_pattern,all_content)
            for num in nums:
                video_url = ahead_name+'第'+num+'集--'+'<a href="'+self.vip_url+'https://'+urls[int(num)-1]+'" target="_blank"></a>'
                video_urls.append(video_url)
        return video_urls
    def __analysis(self, html):
        root_html = re.findall(Spider.root_pattern, html)
        # root_html2 = re.findall(Spider.root_pattern2, html)
        root_html = str(root_html)
        # root_html2 = str(root_html2)
        goal_names = re.findall(Spider.goal_name_pattern, root_html)
        goal_urls = re.findall(Spider.goal_url_pattern, root_html)
        # if '立即播放' in goal_names:
        #     goal_names = re.findall(Spider.goal_name_pattern2, root_html)
        #     goal_urls = re.findall(Spider.goal_url_pattern2, root_html)
        video_lists = []

        if len(goal_urls) > 0:
            if len(goal_urls) <= len(goal_names):
                range_num = len(goal_urls)
            else:
                range_num = len(goal_names)
            for i in range(0, range_num):
                dic = dict()
                dic['name'] = goal_names[i]
                dic['url'] = 'https://' + goal_urls[i]
                if '预告' not in goal_names[i]:
                    if len(goal_names[i]) > 2:
                        video_lists.append(dic)
        else:
            print("出错")
        return video_lists

    def __refine(self, lists):
        for lis in lists:
            lis["url"] = (Spider.vip_url + lis["url"].strip())
        return lists

    def __my_print(self, lists):
        for lis in lists:
            print(lis['name'] + '\t' + lis['url'])

    def __save_video_lists(self, lists):
        if isinstance(lists[0], dict):
            name = list[0]['name']
        else:
            name = lists[0].split("--")[0]
        with open('./{name}.md'.format(name=name), 'w', encoding='utf-8') as f:
            for l in lists:
                f.writelines(str(l)+'  ')
            f.close()

    def go(self):
        url = self.__input_video()
        html = self.__get_content(url)
        if 'youku' not in html:
            html = self.__analysis(html)
            video_lists = self.__refine(html)
            self.__my_print(video_lists)

        else:
            video_lists = self.__analysisyouku(html)
            print(video_lists)
        self.__save_video_lists(video_lists)



if __name__ == "__main__":
    spider = Spider()
    spider.go()

