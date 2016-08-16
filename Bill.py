"""Author: Merlin Teach"""
import time
import pickle
import os

def record(re_ex, reason):
    re_ex = int(re_ex)
    s = str(re_ex) + "," + reason + "," + time.strftime("%Y %m %d", time.localtime())
    with open("record_file", "a") as rf:
        rf.write(s+"\n")
    with open("total", "rb+")  as tf:
        total_data = pickle.load(tf)
        index = "ex"
        if re_ex > 0:
            index = "re"
        total_data[index] = re_ex + total_data[index]
        total_data["balance"] = total_data["ex"] + total_data["re"]
    os.remove("total")
    with open("total", "wb+")  as tf:
        pickle.dump(total_data, tf)

def search(date, reason):
    print("开始检索数据...")
    result = []
    final = []
    try:
        with open("record_file", "r") as rf:
            if date is "today":
                date = time.strftime("%Y %m %d", time.localtime())
            for line in rf:
                if date is "all":
                    result.append(line)
                elif date in line:
                    result.append(line)
            if reason is not None:
                for i in result:
                    if reason in i:
                        final.append(i)
            else:
                final = result[:]
    except IOError as err:
        print("出问题啦!(逗比别以为机智的Merlin Teach设计失误，你能看到这句话证明我猜到了出错，否则你看到的就是这样的东西了:" + str(err))
        print("咳咳说正事，出现此问题:")
        print("1.你脑抽的删了文件")
        print("2.你傻逼的没有录入信息就像查找信息")
    print("完成.")
    return final
    
def b():#为什么这个函数名这么短呢。。。因为我实在想不出名字了
    with open("total", "rb+") as tf:
        data = pickle.load(tf)
        print("总支出: " + str(data["ex"]))
        print("总收入: " + str(data["re"]))
        print("余额: " + str(data["balance"]))

def f_output(list):
    n_list = []
    for i in list:
        n_i = ""
        for it in i.split(","):
            n_i += it
            n_i += "\t"
        n_list.append(n_i)
    return n_list

def help():
    print("输入Date:today获取今日账单")
    print("输入日期(例:Date:1777 07 07)获取当日账单")
    print("输入Reason:原因获取匹配账单")
    print("输入D&R:日期:原因获取匹配账单")
    print("输入Record:数字:原因录入账单")
    print("尽管似乎这并不完整但我不想写了自己看源码吧")
    print("什么？你说我代码一团糟？我****")
    
print("一个神奇的满是bug的记账程序 -Merlin Teach")
print("\n\n\t输入help以取得帮助(尽管事实上这毫无疑义)")
print("\n")

if not os.path.exists("total"):
    with open("total", "wb+") as tf:
        dic = {"re" : 0, "ex" : 0, "balance" : 0}
        pickle.dump(dic, tf)
if not os.path.exists("record_file"):
    with open("record_file", "w") as rf:
        pass

while True:
    s = input(">>>")
    reason = None
    date = "all"
    out = []
    try:
        if s is help:
            help()
        elif "Date" in s:
            _, date = s.split(":")
        elif "Reason" in s:
            _, reason = s.split(":")
        elif "D&R" in s:
            _, date, reason =s.split(":")
        else:
            if "Record" in s:
                _, re_ex, re = s.split(":")
                record(re_ex, re)
                b()
                continue
            elif "Balance" in s:
                b()
            else:
                print("我想你听不懂人话，准备退出")
                break
        out = f_output(search(date, reason))
    except ValueError:
        print("你的输入无效，输入help以得到帮助")
    if len(out) > 0:
        for i in out:
            print(i)
            b()
    