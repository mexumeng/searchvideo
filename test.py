#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "xumeng"
__date__ = "2018/12/23 22:23"
import re
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from urllib import parse
li = ['<h2>\n\t\t\t\t\t<a href="//tv.sohu.com/item/MTIxNDg5Mg==.html" title="虎啸龙吟" target="_blank" pb-url="meta$$mts'
      '$$mtsModule" _s_c="101" _s_pos="album" _s_type="title" _s_k="1214892" _s_d="youku" _s_a="33038587" _s_v="453768328"'
      ' _s_n="" _s_loc="1" _s_algid="200002" _s_ep="">虎啸龙吟</a>\n\t\t\t\t</h2>',
      '<h2>\n\t\t\t\t\t<a href="//tv.sohu.com/item/MTIxMjQwNg==.html" title="大军师司马懿之军师联盟" target="_blank" '
      'pb-url="meta$$mts$$mtsModule" _s_c="101" _s_pos="album" _s_type="title" _s_k="1212406" _s_d="youku" _s_a="33018598"'
      ' _s_v="453304546" _s_n="" _s_loc="2" _s_algid="200002" _s_ep="">大<font class="rd">军师</font>司马懿之'
      '<font class="rd">军师联盟</font></a>\n\t\t\t\t</h2>']

li = str(li)
reses = re.findall(r'href="//([\w\W]*?)" title',li)
video_num_pattern = r'target="_blank">(\w*?)</a>'
video_url_pattern = r'href="//([\w\W]*?);'
video_urls = []
for res in reses:
    url = "https://"+res
    print(url)
    options = Options()
    options.add_argument('-headless')  # 无头参数
    driver = Firefox(executable_path='geckodriver', firefox_options=options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径
    driver.get(url)
    html = driver.page_source
    html = parse.unquote(html)
    driver.quit()
    all_content = re.findall(r'episode cfix[\w\W]*?</div>',html)
    all_content = str(all_content)
    nums = re.findall(video_num_pattern,all_content)
    urls = re.findall(video_url_pattern,all_content)
    for num in nums:
        video_url = '军师联盟'+'第'+num+'集:'+urls[int(num)-1]
        video_urls.append(video_url)
    print(video_urls)
