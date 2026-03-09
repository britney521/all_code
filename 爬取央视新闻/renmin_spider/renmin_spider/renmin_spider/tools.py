# -*- coding:utf-8 -*-
import re

from fake_useragent import UserAgent


class MyException(Exception):
    pass


class tools:
    def getpath(self, nowurl, url):
        baseurl = url
        if "?" in url:
            baseurl = url[:url.rfind('?')]
        if nowurl[:4] == "http":
            return nowurl
        elif nowurl[0] == "/":
            return re.search(r'(https?://[^/]+?)/', baseurl).group(1) + nowurl
        elif nowurl[:3] == "../":
            return self.getpath(nowurl[3:], re.search(r'(https?://.+)/', baseurl).group(1))
        elif nowurl[:2] == "./":
            return re.search(r'(https?://.+)/', baseurl).group(1) + nowurl[1:]
        elif nowurl[0] == "?":
            return baseurl + nowurl
        else:
            return re.search(r'(https?://.+)/', baseurl).group(1) + "/" + nowurl


    def isWeb(self, url):
        tmpurl = url
        if "?" in url:
            tmpurl = tmpurl[:tmpurl.rfind('?')]
        for i in self.typeOfFile:
            if re.search(i, tmpurl, re.I):
                return False
        return True

