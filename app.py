#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# Author: dandan<pipidingdingting@163.com>
# Created on 2016/12/29 23:37
# file: app.py



import unittest
import geo.serviceprovider as serviceprovider

class BaiDuTest(unittest.TestCase):

    def setUp(self):
        self.baidu = serviceprovider.Baidu('0Ecc7840b61120c61892522f079fddc6')
    
    def test_geoconv(self):
        lat, lng = self.baidu.geoconv(23.152963281229162,113.345055696811,f='GCJ02')
        print('[BAIDU GEO CONVERT]', lat, lng)

    def test_geocoding(self):
        lat, lng = self.baidu.geocoding('华南理工大学','广州市')
        print('[BAIDU GEO CODING]', lat, lng)

    def test_reversecoding(self):
        address = self.baidu.reversecoding(23.152963281229162,113.345055696811,f='GCJ02')
        print('[BAIDU GEO REVERSE]', address)

    def test_geoweather(self):
        weather = self.baidu.geoweather('广州市')
        print('[BAIDU GEO WEATHER]', weather)

    def test_geocoding_poi(self):
        lat, lng = self.baidu.geocoding_poi('华南理工大学五山校区','广州市')
        print('[BAIDU GEO CODING POI]', lat, lng)

    def test_location(self):
        lat, lng = self.baidu.location(host='123.168.243.16')
        print('[BAIDU GEO LOCATION]', lat, lng)

class AmapTest(unittest.TestCase):

    def setUp(self):
        self.amap = serviceprovider.Amap('d7d3dae3696d775033d3d04ee2eeb355')
    
    def test_geoconv(self):
        lat, lng = self.amap.geoconv(23.152963281229162,113.345055696811,f='WGS84')
        print('[AMAP GEO CONVERT]', lat, lng)

    def test_geocoding(self):
        lat, lng = self.amap.geocoding('华南理工大学','广州市')
        print('[AMAP GEO CODING]', lat, lng)

    def test_reversecoding(self):
        address = self.amap.reversecoding(23.152963281229162,113.345055696811,f='GCJ02')
        print('[AMAP GEO REVERSE]', address)

    def test_geoweather(self):
        weather = self.amap.geoweather('广州市')
        print('[AMAP GEO WEATHER]', weather)

    def test_geocoding_poi(self):
        lat, lng = self.amap.geocoding_poi('华南理工大学(五山校区)','广州市')
        print('[AMAP GEO CODING POI]', lat, lng)

    def test_location(self):
        lat, lng = self.amap.location(host='123.168.243.16')
        print('[AMAP GEO LOCATION]', lat, lng)


class TencentTest(unittest.TestCase):

    def setUp(self):
        self.tencent = serviceprovider.Tencent('P4ZBZ-SKRWU-TSRVY-232G7-OLJWJ-J4BI5')
    
    def test_geoconv(self):
        lat, lng = self.tencent.geoconv(23.152963281229162,113.345055696811,f='WGS84')
        print('[TENCENT GEO CONVERT]', lat, lng)

    def test_geocoding(self):
        lat, lng = self.tencent.geocoding('华南理工大学','广州市')
        print('[TENCENT GEO CODING]', lat, lng)

    def test_reversecoding(self):
        address = self.tencent.reversecoding(23.152963281229162,113.345055696811,f='WGS84')
        print('[TENCENT GEO REVERSE]', address)

    def test_geoweather(self):
        weather = self.tencent.geoweather('广州市')
        print('[AMAP GEO WEATHER]', weather)

    def test_geocoding_poi(self):
        lat, lng = self.tencent.geocoding_poi('华南理工大学(五山校区)','广州市')
        print('[TENCENT GEO CODING POI]', lat, lng)

    def test_location(self):
        lat, lng = self.tencent.location(host='123.168.243.16')
        print('[TENCENT GEO LOCATION]', lat, lng)

if __name__ == '__main__':
    unittest.main()
