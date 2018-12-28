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
    souhu_vip_url = 'http://www.3aym.cn/?url='
    youku_vip_url = 'http://jqaaa.com/jx.php?url='
    # 搜狐视频搜索网址,获取搜索后的第一页（正则pattern）
    source_url = "https://so.tv.sohu.com/mts?wd="
    # 获取每个视频包含视频名和视频url在<h2>标签内
    h2_pattern = r'<h2>[\w\W]*?</h2>'
    video_name_pattern = r'title="([\w\W]*?)"'
    goal_name_pattern = r'title="([\w\W]*?)"'
    video_url_pattern = r'href="//([\w\W]*?)"'

    def __input_video(self):
        # wd = input('请输入视频名字：'
        wd = '无心法师1'
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

    # def __analysisyouku(self, html):
    #     # 针对优酷的分析爬取
    #     video_num_pattern = r'target="_blank">(\w*?)</a>'
    #     video_url_pattern = r'href="//([\w\W]*?);'
    #     results = re.findall(self.h2_pattern,str(html))
    #     results = []
    #     names_urls = []
    #     video_urls = []
    #     for result in results:
    #         sec_url = re.findall(r'href="//([\w\W]*?)" title',result)[0]
    #         ahead_name = re.findall(self.video_name_pattern,result)[0]
    #         name_url = {ahead_name:sec_url}
    #         names_urls.append(name_url)
    #
    #     securls = []
    #     for res in names_urls:
    #         for name,url in res.items():
    #             url = "https://"+url
    #             ahead = name
    #             securls.append(url)
    #     for url in securls:
    #         html = self.__get_content(url)
    #         all_content = re.findall(r'episode cfix[\w\W]*?</div>',html)
    #         all_content = str(all_content)
    #         nums = re.findall(video_num_pattern,all_content)
    #         urls = re.findall(video_url_pattern,all_content)
    #         for num in nums:
    #             video_url = '<a href="'+vip_url+'https://'+urls[int(num)-1]+'" target="_blank">'+ahead+'第'+num+'集'+'</a>'
    #             if int(num)%5==0:
    #                 video_url = video_url+'<br/>'
    #             video_urls.append(video_url)
    #     return video_urls
    def __analysis(self, html):
        # 第一页
        video_num_pattern = r'target="_blank">([\w\W]*?)<em'
        video_url_pattern = r'href="//([\w\W]*?)"'
        # 判断搜索结果
        if 'youku' in html:
            goal_pattern = r'episode cfix([\w\W]*?)</div>'
            vip_url = self.youku_vip_url
            video_num_pattern = 'blank">([\w]*?)</a>'
        else:
            goal_pattern = r'series2([\w\W]*?)ul'
            vip_url = self.souhu_vip_url
        results = re.findall(r'ssItem cfix([\w\W]*?)des lan_des',html)
        name_urls = []
        for result in results:
            h2_content = re.findall(self.h2_pattern, result)[0]
            if '电影' in result:
                movie_name = re.findall(Spider.video_name_pattern, h2_content)[0]
                movie_url = re.findall(Spider.video_url_pattern, h2_content)[0]
                name_url = '<a href="'+self.souhu_vip_url+'https://'+movie_url+'" target="_blank">'+movie_name+'</a>'
                name_urls.append(name_url)
                return name_urls
            elif '电视剧' in result:
                # 跳转第二页
                names_securls =[]
                sec_url = re.findall(r'href="//([\w\W]*?)" title',h2_content)[0]
                ahead_name = re.findall(self.video_name_pattern,h2_content)[0]
                name_securl = {ahead_name: sec_url}
                names_securls.append(name_securl)
            securls = []
            for res in names_securls:
                for name,nurl in res.items():
                    securl = "https://"+nurl
                    ahead = name
                    securls.append(securl)
            for url in securls:
                html = self.__get_content(url)  # 第三页内容爬取
                all_content = re.findall(goal_pattern, html)
                if all_content:
                    nums = re.findall(video_num_pattern,all_content[0])
                    urls = re.findall(video_url_pattern,all_content[0])
                    for num in nums:
                        video_url = '<a href="'+vip_url+'https://'+urls[int(num)-1]+'" target="_blank">'+ahead+'第'+num+'集'+'</a>'
                        if int(num)%5==0:
                            video_url = video_url+'<br/>'
                        name_urls.append(video_url)
                else:
                    print('无资源')
            return name_urls
    # def __refine(self, lists):
    #     for lis in lists:
    #         lis["url"] = (Spider.vip_url + lis["url"].strip())
    #     return lists
    #
    # def __my_print(self, lists):
    #     for lis in lists:
    #         print(lis['name'] + '\t' + lis['url'])

    def __save_video_lists(self, lists):
        if lists:
            name = lists[0].split('>')[1].replace('</a','')
            with open('./{name}.md'.format(name=name), 'w', encoding='utf-8') as f:
                for l in lists:
                    f.writelines(str(l)+'\n')
                f.close()
        else:
            print('无资源')



    def go(self):
        url = self.__input_video()
        html = self.__get_content(url)
        # if 'youku' not in html:
        video_lists = self.__analysis(html)
        print(video_lists)
        # else:
        #     video_lists = self.__analysisyouku(html)
        #     print(video_lists)
        self.__save_video_lists(video_lists)


if __name__ == "__main__":
    spider = Spider()
    spider.go()

