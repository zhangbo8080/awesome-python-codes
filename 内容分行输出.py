#python版一行内容分行输出
#依山居 18:14 2015/11/4
 
a="aA1一bB2二cC3三dD4四eE5五fF6六gG7七hH8八iI9九"
"""
# 分行输出为:
# abcdefghi
# ABCDEFGHI
# 123456789
# 一二三四五六七八九
# """
import re
reg=["[a-z]","[A-Z]","\d","[^\da-zA-Z]"]
for s in reg:    
    pattern=re.compile(s)
    s=pattern.findall(a)
    print("".join(s))