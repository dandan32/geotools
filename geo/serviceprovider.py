#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# File gislocation.py
# Author: dandan<pipidingdingting@163.com>
# Time: 2016-05-08 20:05
"""
互联网地图服务提供商 web service 接口调用模块
使用GCJ02，WGS84及BD09坐标系

"""
from geo import BaseServiceProvider
from geo import utils
from geo import coordinatetransform


# 百度天气api
# http://lbsyun.baidu.com/index.php?title=car/api/weather

class Baidu(BaseServiceProvider):
    """百度地图"""

    geocoding_url = 'http://api.map.baidu.com/geocoder/v2/'
    location_url = 'http://api.map.baidu.com/location/ip'
    conv_url = 'http://api.map.baidu.com/geoconv/v1/'
    poi_url = 'http://api.map.baidu.com/place/v2/search'
    weather_url = 'http://api.map.baidu.com/telematics/v3/weather'

    def __init__(self, key,timeout=200):
        super(Baidu, self).__init__(timeout)
        self.key = key
        self.t = 'BD09'

    def geoconv(self, lat, lng, f='WGS84'):
        """
        坐标转换服务
        f参数代表from：取1为 wgs84坐标系，3为国测局坐标
        """
        if f == 'WGS84':
            f = 1
        elif f == 'GCJ02':
            f = 3
        else:
            raise ValueError
        data = {
            'coords':'%s,%s' %(lat, lng),
            'from': f,
            'to': 5,
            'output':'json',
            'ak':self.key
        }
        response = utils.request_json(self.conv_url, data, self.timeout)
        if response.get('status', -1) == 0:
            lng = response['result'][0]['y']
            lat = response['result'][0]['x']
            return lat, lng
        return None, None    

    def geocoding(self, address, city, city_limit=True):
        """地理编码服务"""
        data = {
            'address': address,
            'city': city,
            'city_limit': 'true' if city_limit else 'false',
            'output': 'json',
            'ret_coordtype': 'gcj02ll',
            'ak': self.key
        }
        response = utils.request_json(self.geocoding_url, data, self.timeout)
        if response.get('status', -1) == 0:
            if 'location' in response['result'].keys():
                lat = response['result']['location']['lat']
                lng = response['result']['location']['lng']
                return lat, lng
        return None, None

    def reversecoding(self, lat, lng, f='WGS84'):
        """逆地理编码服务"""
        if f == 'WGS84':
            f = 'wgs84ll'
        elif f == 'GCJ02':
            f = 'gcj02ll'
        elif f == 'BD09':
            f = 'bd09ll'

        data = {
            'location': '%s,%s' %(lat, lng),
            'output': 'json',
            'coordtype': f,
            'ak': self.key
        }
        response = utils.request_json(self.geocoding_url, data, self.timeout)

        if response['status'] == 0:
            return response['result']['formatted_address']
        return None

    def geoweather(self, city):
        """天气"""
        data = {
            'location': city,
            'output':'json',
            'ak':self.key
        }
        response = utils.request_json(self.weather_url, data, self.timeout)
        if response['status'] == 'success':
            return response['results'][0]['weather_data'][0]['date']

    def geocoding_poi(self, address, city, city_limit=True):
        """根据poi信息获取地理位置"""
        data={
            'query': address,
            'region': city,
            'city_limit': 'true' if city_limit else 'false',
            'output': 'json',
            'ret_coordtype': 'gcj02ll', # 返回国测局坐标
            'ak': self.key,
        }
        response = utils.request_json(self.poi_url, data, self.timeout)
        # 判断获取的poi是否与地址相符合
        if response['status'] == 0 and len(response['results']) >= 1:
            for each in response['results']:
                if 'location' in each.keys() and each['name'] == address:
                    return response['results'][0]['location']['lat'], response['results'][0]['location']['lng']
        return None, None
    
    def location(self, host):
        """
        根据host ip定位
        好像不够准确
        """
        data={
            'ip':host,
            'ak':self.key,
            'coor':'gcj02'
        }
        response = utils.request_json(self.location_url, data, self.timeout)
        if response['status'] == 0:
            return response['content']['point']['y'], response['content']['point']['x']
        return None, None



class Amap(BaseServiceProvider):
    """高德地图"""

    geocoding_url = 'http://restapi.amap.com/v3/geocode/geo'
    regeocoding_url = 'http://restapi.amap.com/v3/geocode/regeo'
    location_url = 'http://restapi.amap.com/v3/ip'
    conv_url = 'http://restapi.amap.com/v3/assistant/coordinate/convert'
    poi_url = 'http://restapi.amap.com/v3/place/text'
    weather_url = 'http://restapi.amap.com/v3/weather/weatherInfo'

    def __init__(self, key, timeout=200):
        super(Amap, self).__init__(timeout)
        self.key = key
        self.t = 'GCJ02'

    def geoconv(self, lat, lng, f='WGS84'):
        """
        坐标转换
        支持WGS84, BD09 坐标系转换为 GCJ02坐标系
        """
        if f == 'WGS84':
            lat, lng = coordinatetransform.transformWGStoGCJ(lat, lng)
        elif f == 'BD09':
            lat, lng = coordinatetransform.transformBDtoGCJ(lat, lng)
        else:
            raise ValueError

        data = {
            'locations': ('%s,%s' %(lng, lat)),
            'coordsys': f,
            'key': self.key
        }
        response = utils.request_json(self.conv_url, data, self.timeout)
        if response['status'] == '1':
            lng, lat = map(float, response['locations'].split(','))
            return lat, lng
        return None, None    

    def geocoding(self, address, city, city_limit=True):
        """地理编码服务"""
        data = {
            'address': address,
            'city': city,
            'output': 'json',
            'key': self.key,
        }
        if not city_limit:
            data.pop('city')
        response = utils.request_json(self.geocoding_url, data, self.timeout)
        if response.get('status', -1) == '1':
            if 'location' in response['geocodes'][0].keys():
                location_str = response['geocodes'][0]['location'].split(',')
                return float(location_str[1]), float(location_str[0])
        return None, None
    
    def reversecoding(self, lat, lng, f='WGS84'):
        data = {
            'key': self.key,
            'location': '%s,%s' %(lng, lat),
            'output': 'json'
        }
        response = utils.request_json(self.regeocoding_url, data, self.timeout)
        if response.get('status', -1) == '1' and 'regeocode' in response:
            return response['regeocode']['formatted_address']
        return None
    
    def geoweather(self, city):
        """天气服务"""
        data = {
            'city': city,
            'output':'json',
            'key':self.key
        }
        response = utils.request_json(self.weather_url, data, self.timeout)
        if response['status'] == '1':
            return '%s %s' %(response['lives'][0]['weather'],response['lives'][0]['temperature'])
        return None

    def geocoding_poi(self, address, city, city_limit=True):
        
        data = {
            'keywords': address,
            'city': city,
            'output': 'json',
            'citylimit': 'true',
            'key': self.key,
        }
        response = utils.request_json(self.poi_url, data, self.timeout)
        if response.get('status', '-1') == '1':
            for each in response['pois']:
                if 'location' in each.keys() and address == each.get('name',''):
                    location_str = each['location'].split(',')
                    return float(location_str[1]), float(location_str[0])
        return None, None
    
    def location(self, host):
        """根据host ip定位"""
        data={
            'ip':host,
            'key':self.key,
            'output':'json',
        }
        response = utils.request_json(self.location_url, data, self.timeout)
        if response['status'] == '1':
            (x1,y1), (x2,y2) = (map(float,each.split(',')) for each in response['rectangle'].split(';'))
            return (y1+y2)/2, (x1+x2)/2
        return None, None



class Tencent(BaseServiceProvider):
    """腾讯地图"""

    geocoding_url = 'http://apis.map.qq.com/ws/geocoder/v1/'
    location_url = 'http://apis.map.qq.com/ws/location/v1/ip'
    conv_url = 'http://apis.map.qq.com/ws/coord/v1/translate'
    poi_url = 'http://apis.map.qq.com/ws/place/v1/search'
    weather_url = ''
    timeout = 200

    def __init__(self, key, timeout=200):
        super(Tencent, self).__init__(timeout)
        self.key = key
        self.t = 'GCJ02'

    def geoconv(self, lat, lng, f='WGS84'):
        if f=='WGS84':
            f = 1
        elif f=='BD09':
            f = 3
        else:
            raise ValueError
        data = {
            'locations': '%s,%s' %(lat, lng),
            'type':f,
            'key':self.key,
            'output':'json',
        }
        response = utils.request_json(self.conv_url, data, self.timeout)
        if response['status'] == 0:
            return response['locations'][0]['lat'], response['locations'][0]['lng']
        print(response)
        return None, None

    def geocoding(self, address, city, city_limit=True):
        """地理编码服务"""
        data = {
            'address': '%s%s' %(city, address),
            'output': 'json',
            'key': self.key
        }
        response = utils.request_json(self.geocoding_url, data, self.timeout)
        if response.get('status', -1) == 0:
            return response['result']['location']['lat'], response['result']['location']['lng']
        return None, None

    def reversecoding(self, lat, lng, f='WGS84'):
        if f == 'WGS84':
            f = 1
        elif f == 'BD09':
            f = 3
        else:
            raise ValueError
        data = {
            'location': '%s,%s' %(lat, lng),
            'coord_type':f,
            'output':'json',
            'key': self.key,
        }
        response = utils.request_json(self.geocoding_url, data, self.timeout)
        if response['status'] == 0:
            return response['result']['address']
        return None

    def geocoding_poi(self, address, city, city_limit=True):
        data = {
            'keyword': address,
            'boundary': 'region(%s,0)' % city,
            'page_size': 20,
            'page_index': 1,
            'output': 'json',
            'key': self.key
        }
        response = utils.request_json (self.poi_url, data, self.timeout)
        if response.get('status', -1) == 0:
            for each in response['data']:
                if address == each.get('title',''):
                    return each['location']['lat'], each['location']['lng']
        return None, None

    def location(self, host):
        """根据host ip定位"""
        data={
            'ip':host,
            'key':self.key,
            'output':'json',
        }
        response = utils.request_json(self.location_url, data, self.timeout)
        if response['status'] == 0:
            return response['result']['location']['lat'],response['result']['location']['lng']
        return None, None




class Google(BaseServiceProvider):
    """谷歌地图"""


    def geoweather(self, city):
        pass

    def geopoi(self):
        pass

    def location(self, host):
        pass

    def geocoding_poi(self, address, city, city_limit=True):
        pass

    def geocoding(self, address, city):
        pass

    def geoconv(self, lat, lng):
        pass

    def reversecoding(self, lat, lng, f):
        pass
