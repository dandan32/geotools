#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# File coordinatetransform.py
# Time: 2016-05-09 11:03
"""
坐标系统转换

WGS-84: World Geodetic System 1984，是为GPS全球定位系统使用而建立的坐标系统
GCJ-02是由中国国家测绘局（G表示Guojia国家，C表示Cehui测绘，J表示Ju局）制订的地理信息系统的坐标系统。
BD09表示百度坐标
高德\腾讯使用的是GCJ-02坐标

"""
import math

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率




def transformBDtoWGS(bd_lat, bd_lng):
    """
    百度坐标系(BD-09)坐标转换WGS-84坐标
    :param bd_lat:百度坐标纬度
    :param bd_lng:百度坐标经度
    :return:lat, lng
    """
    x_pi = bd_lat * bd_lng / 180.0
    x = bd_lng - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    lat = z * math.sin(theta)
    lng = z * math.cos(theta)
    return lat, lng




def transformGCJtoBD(lat, lng):
    """
    火星坐标系(GCJ-02)坐标转换百度坐标系(BD-09)坐标
    :param lat:火星坐标纬度
    :param lng:火星坐标经度
    :return:bd_lat, bd_lng
    """
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lat = z * math.sin(theta) + 0.006
    bd_lng = z * math.cos(theta) + 0.0065

    return bd_lat, bd_lng


def transformBDtoGCJ(bd_lat, bd_lng):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德
    :param bd_lat:百度坐标纬度
    :param bd_lng:百度坐标经度
    :return:lat, lng
    """
    x = bd_lng - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    lat = z * math.sin(theta)
    lng = z * math.cos(theta)

    return lat, lng


def transformWGStoGCJ(w_lat, w_lng):
    """
    WGS84转GCJ02(火星坐标系)
    :param w_lat:WGS84坐标系的纬度
    :param w_lng:WGS84坐标系的经度
    :return: g_lat, g_lng
    """
    if out_of_china(w_lng, w_lat):  # 判断是否在国内
        return w_lng, w_lat
    dlat = transformlat(w_lng - 105.0, w_lat - 35.0)
    dlng = transformlng(w_lng - 105.0, w_lat - 35.0)
    radlat = w_lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    g_lat = w_lat + dlat
    g_lng = w_lng + dlng

    return g_lat, g_lng


def transformGCJtoWGS(g_lat, g_lng):
    """
    GCJ02(火星坐标系)转GPS84
    :param g_lat:火星坐标系纬度
    :param g_lng:火星坐标系的经度
    :return:
    """
    if out_of_china(g_lng, g_lat):
        return g_lng, g_lat
    dlat = transformlat(g_lng - 105.0, g_lat - 35.0)
    dlng = transformlng(g_lng - 105.0, g_lat - 35.0)
    radlat = g_lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = g_lat + dlat
    mglng = g_lng + dlng
    w_lat = g_lat * 2 - mglat
    w_lng = g_lng * 2 - mglng

    return w_lat, w_lng


def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 * math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 * math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 * math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 * math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    if lng < 72.004 or lng > 137.8347:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False

