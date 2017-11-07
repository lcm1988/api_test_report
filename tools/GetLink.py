#!/usr/bin/python3.5
#coding:utf-8

def GetLink(links={}):
    l=[]
    for url,content in links.items():
        print(url,content)
        l.append('''<a href="%s">%s</a>'''%(url,content))
    return '<br>'.join(l)
