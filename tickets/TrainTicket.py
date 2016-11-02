# _*_ coding:utf-8 _*_
__author__ = "lvhaidong"

from prettytable import PrettyTable

# 拿到对应的火车票进行显示
class TrainTicket(object):
    """docstring for TrainTicket"""
    def __init__(self, rows):
        self.rows = rows
        self.header = '车次 出发/到达站 出发/到达时间 历时(h/m) 商务座 一等座 二等座 软卧 硬卧 软座 硬座 无座'.split()


    # 查看运行的时间
    def __get_duration(self, row):
        if row['lishi'] == "99:59":
            return "列车停运"
        duration = row['lishi'].replace(':','H:') + "m"

        # 如果是不足一小时的,应该是去掉前面的4位, 只剩下分钟数,例如00H:25m 武清->北京
        if duration.startswith('00'):
            return duration[4:]

        # 当大于1小时的,就从第一位取值,显示小时数
        elif duration.startswith('0'):
            return duration[1:]
        return duration

    # 根据列表返回的字段,进行获取,拿到对应的值
    @property
    def trains(self):
        for row in self.rows:
            train = [
                # 车次
                row['station_train_code'],
                # 出发 到达站
                '\n'.join([ "\033[0;31;1m"+row['from_station_name']+"\033[0m",
                            "\033[0;34;1m"+row['to_station_name']+ "\033[0m"]),
                # 出发 到达时间
                '\n'.join(["\033[0;31;1m"+row['start_time']+"\033[0m",
                            "\033[0;34;1m"+ row['arrive_time'] + "\033[0m"]),
                # 历时
                self.__get_duration(row),
                # 商务座
                row['swz_num'],
                # 一等座
                row['zy_num'],
                # 二等座
                row['ze_num'],
                # 软卧
                row['rw_num'],
                # 硬卧
                row['yw_num'],
                # 软座
                row['yw_num'],
                # 硬座
                row['yz_num'],
                # 无座
                row['wz_num']
            ]

            # 内置函数,循环遍历
            yield train

    # 格式化打印
    def pretty_print(self):
        """
            数据已经获取到了，剩下的就是提取我们要的信息并将它显示出来。
            prettytable这个库可以让我们它像MySQL数据库那样格式化显示数据。
        """
        pt = PrettyTable()

        # 设置每一列的标题
        pt._set_field_names(self.header)

        # 添加每一行
        for train in self.trains:
            pt.add_row(train)

        print(pt)

