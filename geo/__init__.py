#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Geocoding tools: base on the service provided by Baidu, Amap, Tencent
"""

class BaseServiceProvider(object):
    """"""

    geocoding_url = ''
    location_url = ''
    conv_url = ''
    poi_url = ''
    
    def __init__(self, timeout=200):
        self.timeout = timeout

    def  geoconv(self, lat, lng):
        """坐标转换服务"""
        raise NotImplementedError

    def geocoding(self, address, city):
        """地理编码服务"""
        raise NotImplementedError

    def reversecoding(self, lat, lng, f):
        """逆地理编码服务"""
        raise NotImplementedError

    def geocoding_poi(self, address, city, city_limit=True):
        """poi信息获取"""
        raise NotImplementedError

    def geopoi(self):
        """poi信息获取"""
        raise NotImplementedError

    def geoweather(self, city):
        """天气"""
        raise NotImplementedError

    def location(self, host):
        """根据host ip定位"""
        raise NotImplementedError

    @classmethod
    def toGCJ02(lat, lng):
        """转换为国测局坐标系"""
        raise NotImplementedError
        
    @classmethod
    def toWGS84(lat, lng):
        """转换为84坐标系"""
        raise NotImplementedError


class Point(object):

    def __init__(self, lat,lng, t='WGS84'):
        self.lat = lat
        self.lng = lng
        self.t = t
    
    def toGCJ02(self):
        pass

    def toWGS84(self):
        pass

    def toBD09(self):
        pass