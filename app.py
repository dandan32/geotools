#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# Author: dandan<pipidingdingting@163.com>
# Created on 2017/5/15 20:33
# file: app.py.py

import geo

baidu = geo.MapService('BaiDu','0Ecc7840b61120c61892522f079fddc6',10)
tencent = geo.MapService('Tencent','P4ZBZ-SKRWU-TSRVY-232G7-OLJWJ-J4BI5',10)
amap = geo.MapService('Amap','d7d3dae3696d775033d3d04ee2eeb355',10)
# p = baidu.geoconv(23.15296,113.345055,f='WGS84')
# print(p)
# p = tencent.geoconv(23.152963281229162,113.345055696811,f='WGS84')
# print(p)
# p = amap.geoconv(23.152963281229162,113.345055696811,f='WGS84')
# print(p)
#
#
# p = baidu.geocoding('华南理工大学','广州市')
# print(p)
# p = tencent.geocoding('华南理工大学','广州市')
# print(p)
# p = amap.geocoding('华南理工大学','广州市')
# print(p)


# p = baidu.reversecoding(23.15296,113.345055,f='WGS84')
# print(p)
# p = tencent.reversecoding(23.152963281229162,113.345055696811,f='WGS84')
# print(p)
# p = amap.reversecoding(23.152963281229162,113.345055696811,f='WGS84')
# print(p)

p = baidu.geocoding_poi('华南理工大学五山校区','广州市')
print(p)
p = tencent.geocoding_poi('华南理工大学','广州市')
print(p)
p = amap.geocoding_poi('华南理工大学(五山校区)','广州市')
print(p)

baidu.geoweather('番禺|广州')



