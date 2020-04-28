# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2018/6/12 17:16'

str1 = ""
name_list = []
with open("D:/姓氏大全.txt") as f:
    lines = f.readlines()
    for line in lines:
        line1 = line.replace("\n", "")
        line2 = line1.strip()
        if "（" in line2:
            print(line2)
        if len(line2) < 4:
            name_list.append(line2)

name_list.sort(key=lambda x: len(x), reverse=True)

for x in name_list:
    str1 = str1 + x + "|"

with open("D:/liutong.txt", "w") as f1:
    f1.write(str1)
