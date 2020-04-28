# Created on 2018年2月24日
# author: zhangbo

import tkinter as tk
import os


def f11():
    os.system("python startRunner_sns_android.py")


def f22():
    print("******敬请期待！！！******")


window = tk.Tk()
window.title('狐友自动化测试工具')
window.geometry('400x400')

f1 = tk.Frame(window, width=200, height=200, bg='blue', borderwidth=2)
f2 = tk.Frame(window, width=200, height=200, bg='red', borderwidth=2)
f3 = tk.Frame(window, width=200, height=200, bg='gray', borderwidth=2)
f4 = tk.Frame(window, width=200, height=200, bg='yellow', borderwidth=2)

f1.grid(row=0, column=0)
f2.grid(row=0, column=1)
f3.grid(row=1, column=0)
f4.grid(row=1, column=1)

l1 = tk.Button(window, text='SNS自动化测试--Android端', width=25, command=f11).grid(row=0, column=0)
l2 = tk.Button(window, text='SNS自动化测试--iOS端', width=25, command=f22).grid(row=0, column=1)
l3 = tk.Button(window, text='墨客自动化测试--Android端', width=25, command=f22).grid(row=1, column=0)
l4 = tk.Button(window, text='墨客自动化测试--iOS端', width=25, command=f22).grid(row=1, column=1)

window.mainloop()
