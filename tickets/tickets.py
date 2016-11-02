# _*_ coding:utf-8 _*_

"""
	Train tickets query via command-line.

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets beijing shanghai 2016-11-05
"""
from docopt import docopt

from stations import stations

from xpinyin import Pinyin

import requests

from TrainTicket import TrainTicket


def click():
    """command-line interface"""
    arguments = docopt(__doc__)

    # 汉字转拼音对象
    p = Pinyin() 

    # 发站
    # 如果用户输入的是汉字,转化为拼音去查找代号
    chinese_from_station = p.get_pinyin(arguments['<from>'].lower()).replace("-","")
    # 去station.py中去查找出发站对应的代号
    from_station = stations.get(chinese_from_station)


    # 到站
    # 如果用户输入的是汉字,转化为拼音去查找代号
    chinese_to_station = p.get_pinyin(arguments['<to>'].lower()).replace("-","")
    # 去station.py中去查找到站对应的代号
    to_station = stations.get(chinese_to_station)
   
    # print(to_station)

    # 时间
    date = arguments['<date>']
    # date = date.split('-')
    # date = '%04d-%02d-%02d' % (int(date[0]), int(date[1]), int(date[2]))

    # 构建URL 
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'\
            .format(date, from_station, to_station)

    # 添加verify=False参数不验证证书
    r = requests.get(url, verify=False)

    if 'data' not in r.json():
        print('未找到相应信息,请查看,是否已经日期不正确!')
        return
    rows = r.json()['data']['datas']

    trains = TrainTicket(rows)
    trains.pretty_print()


if __name__ == '__main__':
    click()
