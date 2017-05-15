#!/usr/bin/env python
#-*- coding:UTF-8 -*-
# Author: dandan<pipidingdingting@163.com>
# Created on 
# file: utilss.py
# Created on 2016/5/11 0:13
# file: utils.py

import urllib
import urllib.parse
import urllib.request
import json
import logging


def uppack_json(text):
    """解析json"""
    try:
        return json.loads(text)
    except json.JSONDecodeError as error:
        logging.error('JSON DECODEERROR!')
        logging.error(error.msg)
    return None


def request_stream(url, data, timeout, method='GET'):
    """获取流式返回"""
    # 处理参数
    url_parsed = list(urllib.parse.urlparse(url))
    url_parsed[4] = urllib.parse.urlencode(data)
    request_url = urllib.parse.ParseResult(*url_parsed).geturl()

    logging.debug(request_url)
    # 请求数据
    request = urllib.request.Request(request_url)
    response = urllib.request.urlopen(request, timeout=timeout)

    return response


def request(*args, **kwargs):
    """获取完整文本"""
    response = request_stream(*args, **kwargs)
    return response.read().decode('utf-8')


def request_json(*args, **kwargs):
    """请求json数据"""
    text = request(*args, **kwargs)
    return uppack_json(text)



