#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Geocoding tools: base on the service provided by Baidu, Amap, Tencent
"""

from geo import coordinatetransform


class Point(object):

    def __init__(self, lat,lng, t='WGS84', address=''):
        self.lat = lat
        self.lng = lng
        self.t = t
        self.address = address

    def toGCJ02(self):
        if self.t == 'GCJ02':
            return self.lat, self.lng
        elif self.t == 'WGS84':
            return coordinatetransform.transformWGStoGCJ(self.lat, self.lng)
        elif self.t == 'BD09':
            return coordinatetransform.transformBDtoGCJ(self.lat, self.lng)

    def toWGS84(self):
        if self.t == 'GCJ02':
            return coordinatetransform.transformGCJtoWGS(self.lat, self.lng)
        elif self.t == 'WGS84':
            return self.lat, self.lng
        elif self.t == 'BD09':
            return coordinatetransform.transformBDtoWGS(self.lat, self.lng)


    def toBD09(self):
        if self.t == 'GCJ02':
            return coordinatetransform.transformGCJtoBD(self.lat, self.lng)
        elif self.t == 'WGS84':
            lat, lng = coordinatetransform.transformWGStoGCJ(self.lat, self.lng)
            return coordinatetransform.transformGCJtoBD(lat, lng)
        elif self.t == 'BD09':
            return self.lat, self.lng

    def __str__(self):
        return '[%s] %s,%s; %s' % (self.t, self.lat, self.lng, self.address)


class BaseServiceProvider(object):
    """地图服务基类"""

    geocoding_url = ''
    regeocoding_url = ''
    location_url = ''
    conv_url = ''
    poi_url = ''
    weather_url = ''

    def __init__(self, timeout=200):
        self.timeout = timeout

    def  geoconv(self, lat, lng, f='WGS84'):
        """坐标转换服务"""
        raise NotImplementedError

    def geocoding(self, address, city, city_limit=True):
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

from geo.serviceprovider import Baidu, Amap, Tencent

ServiceProviderDict = {
    'BaiDu': Baidu,
    'Amap': Amap,
    'Tencent':Tencent
}

class MapService(object):

    def __init__(self, sp, key, timeout):
        if sp not in ServiceProviderDict:
            raise ValueError('未集成该地图服务提供商：%s' % sp)
        self.sp = ServiceProviderDict[sp](key, timeout=200)

    def  geoconv(self, lat, lng, f='WGS84'):
        """坐标转换服务"""
        lat, lng = self.sp.geoconv(lat, lng,f)
        p = Point(lat, lng, self.sp.t)
        return p

    def geocoding(self, address, city, city_limit=True):
        """地理编码服务"""
        lat, lng = self.sp.geocoding(address, city, city_limit=city_limit)
        p = Point(lat, lng, self.sp.t)
        return p

    def reversecoding(self, lat, lng, f='WGS84'):
        """逆地理编码服务"""
        address = self.sp.reversecoding(lat, lng, f=f)
        p = Point(None, None, self.sp.t, address)
        return p

    def geocoding_poi(self, address, city, city_limit=True):
        """poi信息获取"""
        lat, lng = self.sp.geocoding_poi(address, city, city_limit=city_limit)
        p = Point(lat, lng, self.sp.t)
        return p

    def geopoi(self):
        """poi信息获取"""
        raise NotImplementedError

    def geoweather(self, city):
        """天气"""
        if isinstance(self.sp, Tencent):
            raise NotImplementedError
        lat, lng = self.sp.geoweather(city)
        p = Point(lat, lng, self.sp.t)
        return p

    def location(self, host):
        """根据host ip定位"""
        lat, lng = self.sp.location(host)
        p = Point(lat, lng, self.sp.t)
        return p

# TODO 代理类

