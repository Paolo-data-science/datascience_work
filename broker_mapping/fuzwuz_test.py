# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 13:23:32 2019

@author: User
"""

import pandas as pd
from pandas import ExcelFile, ExcelWriter
from fuzzywuzzy import fuzz, process

broker_data = ["26 Century Blvd Ste 101", "11 Washington Pl", "15305 Dallas Pkwy # 1100", 
               "1 World Financial Ctr", "Conco Corp Cent Five of H Te Cencourse Corpora", "233 S Wacker Dr Ste 2000","1001 Lakeside Ave E # 1600",
"525 Market St Ste 3400", "18101 Von Karman Ave"]
len(broker_data)
raw_data = ["11 NORTH WATER ST. SUITE 19290",
"15305 N. DALLAS PARKWAY SUITE 1100",
"ONE WORLD FINANCIAL CENTER 3RD FLOOR",
"CONCOURSE CORPORATE CTR. FIVE 18TH FL.",
"233 SOUTH WACKER DRIVE SUITE 200",
"200 PUBLIC SQUARE STE 3760",
"525 MARKET ST. SUITE 3400",
"18101 VON KARMAN AVENUE",
"26 CENTURY BOULEVARD"]
len(raw_data)


for item in raw_data:
    top_ratio = 0
    top_index = 0
    for index in xrange(len(broker_data)):
        ratio = fuzz.ratio(item, broker_data[index])
        if top_ratio < ratio:
            top_ratio = ratio
            top_index = index
    print "Ratio: {0} : {1} - {2}%".format(item, broker_data[top_index], top_ratio)


for item in raw_data:
    top_ratio = 0
    top_index = 0
    for index in xrange(len(broker_data)):
        ratio = fuzz.partial_ratio(item, broker_data[index])
        if top_ratio < ratio:
            top_ratio = ratio
            top_index = index
    print "Partial Ratio: {0} : {1} - {2}%".format(item, broker_data[top_index], top_ratio)
    
    
for item in raw_data:
    top_ratio = 0
    top_index = 0
    for index in xrange(len(broker_data)):
        ratio = fuzz.token_sort_ratio(item, broker_data[index])
        if top_ratio < ratio:
            top_ratio = ratio
            top_index = index
    print "Token Sort Ratio: {0} : {1} - {2}%".format(item, broker_data[top_index], top_ratio)
 
    
for item in raw_data:
    top_ratio = 0
    top_index = 0
    for index in xrange(len(broker_data)):
        ratio = fuzz.token_set_ratio(item, broker_data[index])
        if top_ratio < ratio:
            top_ratio = ratio
            top_index = index
    print "Token Set Ratio: {0} : {1} - {2}%".format(item, broker_data[top_index], top_ratio)
    
    
for item in raw_data:
    top_ratio = 0
    top_index = 0
    for index in xrange(len(broker_data)):
        ratio = fuzz.QRatio(item, broker_data[index])
        if top_ratio < ratio:
            top_ratio = ratio
            top_index = index
    print "QRatio: {0} : {1} - {2}%".format(item, broker_data[top_index], top_ratio)
    
for item in raw_data:
    top_ratio = 0
    top_index = 0
    for index in xrange(len(broker_data)):
        ratio = fuzz.partial_token_sort_ratio(item, broker_data[index])
        if top_ratio < ratio:
            top_ratio = ratio
            top_index = index
    print "Partial Token Sort Ratio: {0} : {1} - {2}%".format(item, broker_data[top_index], top_ratio)

# NOT BAD!!!
for item in raw_data:
    top_ratio = 0
    top_index = 0
    for index in xrange(len(broker_data)):
        ratio = fuzz.UQRatio(item, broker_data[index])
        if top_ratio < ratio:
            top_ratio = ratio
            top_index = index
    print "UQRatio: {0} : {1} - {2}%".format(item, broker_data[top_index], top_ratio)

for item in raw_data:
    top_ratio = 0
    top_index = 0
    for index in xrange(len(broker_data)):
        ratio = fuzz.UWRatio(item, broker_data[index])
        if top_ratio < ratio:
            top_ratio = ratio
            top_index = index
    print "UWRatio: {0} : {1} - {2}%".format(item, broker_data[top_index], top_ratio)

for item in raw_data:
    top_ratio = 0
    top_index = 0
    for index in xrange(len(broker_data)):
        ratio = fuzz.WRatio(item, broker_data[index])
        if top_ratio < ratio:
            top_ratio = ratio
            top_index = index
    print "WRatio: {0} : {1} - {2}%".format(item, broker_data[top_index], top_ratio)

for item in raw_data:
    top_ratio = 0
    top_index = 0
    for index in xrange(len(broker_data)):
        ratio = fuzz.WRa(item, broker_data[index])
        if top_ratio < ratio:
            top_ratio = ratio
            top_index = index
    print "WRatio: {0} : {1} - {2}%".format(item, broker_data[top_index], top_ratio)

    

    