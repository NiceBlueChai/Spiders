#!/usr/bin/python
# -*- coding: utf-8 -*-
# json string:
import urllib3
import random
import execjs  # 安装 pip install PyExecJS
import json
import re


def Cre_Token_Js(Goods_ID_F):  # JavaScript加密生成token
    Js_File_Name = "./MMM_GET_TOKEN.js"  # JS的路径，根据需要修改
    f = open(Js_File_Name, 'r', encoding='utf-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    # return htmlstr
    js = execjs.compile(htmlstr)
    Token = js.call('d.encrypt', 'http://item.jd.com/' +
                    Goods_ID_F+'.html', '2', 'true')
    return Token


def Spr_Date(Date):  # Date数据查询的整理
    Re_Date = re.findall(
        "\[Date.UTC\(([\s\S]*?,[\s\S]*?,[\s\S]*?)\),(.*?)\]", Date)
    Re_Date_Final = ''
    for Date_i in Re_Date:
        Re_Date_Final = Re_Date_Final + \
            str(Date_i[0].replace(',', '.',)) + "," + \
            str(Date_i[1].replace(',', '.',)) + ","
    print(Re_Date_Final)
    return Re_Date_Final
