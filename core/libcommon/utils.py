#!/usr/bin/env python
#-*- coding: utf-8 -*-

def getUnit(unit, value, isB = 'false'):
    if isB == 'true':
        if unit == 'KB':
           value = round(float(value) / 1024, 2)
        elif unit == 'MB':
           value = round(float(value) / 1024/ 1024, 2)
        elif unit == 'GB':
           value = round(float(value) / 1024/ 1024/ 1024, 2)
        elif unit == 'TB':
           value = round(float(value) / 1024/ 1024/ 1024/ 1024, 2)
        return value
    else:
        if unit == 'KB':
           value = round(float(value) / 1, 2)
        elif unit == 'MB':
           value = round(float(value) / 1024, 2)
        elif unit == 'GB':
           value = round(float(value) / 1024/ 1024, 2)
        elif unit == 'TB':
           value = round(float(value) / 1024/ 1024/ 1024, 2)
        return value
        
def getUnit_2(unit, value):
    if unit == 'KB':
        value = round(float(value) / 1, 2)
    elif unit == 'MB':
        value = round(float(value) / 1024, 2)
    elif unit == 'GB':
        value = round(float(value) / 1024 /1024, 2)
    elif unit == 'TB':
        value = round(float(value) / 1024 /1024 /1024, 2)
    return value