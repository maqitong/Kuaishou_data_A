"""
一、 数据来源分析
    1.（爬什么） 需求分析
        获取快手热榜所有视频中的
            -视频
            -视频标题
            -分类
            -评论
            -点赞数
            -播放量
    2.（去哪爬） 接口分析
        2.1 确定是动态还是静态

二、 爬虫代码实现
    1.发送请求
    2.数据获取
    3.数据解析
    4.数据保存
        -保存成csv文件
            导入：import csv
            读取：
            写入：
"""
import csv
import os.path

import httpx
import re
import json

def get_rank(url, headers, cookies, params):
    with httpx.Client() as client:
        response = client.get(url, headers=headers, cookies=cookies, params=params)
        return response.text


def parse_rank(html):
    result_list = []
    result = re.findall(r'window.__APOLLO_STATE__=(.*?);[(]function', html, re.S)
    json_dic = json.loads(result[0])    #  re.findall返回值是列表（.*?）

    for key in json_dic['defaultClient']:    #  把字典中的key取出 == for key in dic.keys():
        if key.startswith('VisionHotRankItem'):
            result_dict = {}
            result_dict['rank'] = json_dic['defaultClient'][key]['rank']
            result_dict['name'] = json_dic['defaultClient'][key]['name']
            result_dict['hotValue'] = json_dic['defaultClient'][key]['hotValue']
            result_list.append(result_dict)

    return result_list

    # root_rank = rank['defaultClient']['defaultClient']['dict_r']

def save_data(data):
    if not os.path.exists('./数据'):
        os.mkdir('./数据')
    with open('./数据/榜单.csv', 'w', encoding='utf-8-sig', newline='') as f:
        #  csv的写入
        # csv_writer = csv.writer(f)  #  写入列表
        hand = ['rank', 'name', 'hotValue']  # 表头
        csv_writer = csv.DictWriter(f, fieldnames=hand)  #  写入字典
        csv_writer.writeheader()
        csv_writer.writerows(data)  #  创建写手


def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42",

    }
    cookies = {
        "kpf": "PC_WEB",
        "clientid": "3",
        "did": "web_1712a745d28adca024fc9d8898cdfa34",
        "userId": "3503868975",
        "kpn": "KUAISHOU_VISION",
        "kuaishou.server.web_st": "ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqAB-5cgt7OTxEMy3ViRIwP0cZ4UL2UQmhqzI9jwd1IzgqQx1NqaenzZQAzCMNJEObWvREdU2SapPKf5fr3KFi4npIL6yRz3EH7PJ7trhJqsPFAprIBBBoAYXGLTBKbbbCb6g3YtIGYyA8Po8Q_jrPhpNPHm9Pb7JQJQmOIPDT3UbM6OpvXwk5FBwmvoidN9B0Ul1C2-fU-oleRtk8jxnd3oLBoSg3ZkWJHNsQvvc8vsvUksYr6BIiA5Imt5ijBXpDNX_e_yRfkcxI7Bg8oPTpPZYWHjBeOjSigFMAE",
        "kuaishou.server.web_ph": "f8a64d4d1bc193441ce5f050757e9d0a1c78"
    }
    url = "https://www.kuaishou.com/"
    params = {
        "isHome": "1"
    }
    html = get_rank(url, headers, cookies, params)
    data = parse_rank(html)
    save_data(data)




if __name__ == '__main__':
    main()