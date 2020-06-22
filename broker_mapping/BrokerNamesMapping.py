# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 13:25:41 2019

@author: User
"""

import pandas as pd
from pandas import ExcelFile, ExcelWriter
from fuzzywuzzy import fuzz, process
import difflib

usi_target = pd.read_excel("Arth_J_Gall.xlsx")
usi_brokers = pd.read_excel("D&B_brokers_copy.xlsx")
usi_target.fillna("", inplace = True)

usi_target.info()

target_global_name = usi_target["Broker"].str.unique()[0]
brokers_data = usi_brokers.loc[usi_brokers["Global Ultimate Business Name"].str.match(target_global_name)]

brokers_data.info()

cities = usi_target.City.unique()
for city in cities:
    print "============================"
    print "City: "+str(city)
    targets = usi_target[usi_target.City.str.upper() == str(city).upper()]
    brokers = brokers_data[brokers_data['Physical City'].str.upper() == str(city).upper()]
    if(len(brokers) < 1):
        print "NO BROKERS FOR CITY: "+str(city)
        continue
    for target_index, target_row in targets.iterrows():
        top_ratio = 0
        top_index = 0
        for broker_index, broker_row in brokers.iterrows():
            ratio = fuzz.ratio(target_row['PartyCompanyName'], broker_row['Business Name'])
            if top_ratio < ratio:
                top_ratio = ratio
                top_index = broker_index
        print "Ratio: {0} : {1} - {2}%".format(target_row['PartyCompanyName'], brokers.loc[top_index, ['Business Name']].values[0], top_ratio)

for city in cities:
    print "============================"
    print "City: "+str(city)
    targets = usi_target[usi_target.City.str.upper() == str(city).upper()]
    brokers = brokers_data[brokers_data['Physical City'].str.upper() == str(city).upper()]
    if(len(brokers) < 1):
        print "NO BROKERS FOR CITY: "+str(city)
        continue
    for target_index, target_row in targets.iterrows():
        top_ratio = 0
        top_index = 0
        for broker_index, broker_row in brokers.iterrows():
            ratio = fuzz.partial_ratio(target_row['PartyCompanyName'], broker_row['Business Name'])
            if top_ratio < ratio:
                top_ratio = ratio
                top_index = broker_index
        print "Partial Ratio: {0} : {1} - {2}%".format(target_row['PartyCompanyName'], brokers.loc[top_index, ['Business Name']].values[0], top_ratio)

for city in cities:
    print "============================"
    print "City: "+str(city)
    targets = usi_target[usi_target.City.str.upper() == str(city).upper()]
    brokers = brokers_data[brokers_data['Physical City'].str.upper() == str(city).upper()]
    if(len(brokers) < 1):
        print "NO BROKERS FOR CITY: "+str(city)
        continue
    for target_index, target_row in targets.iterrows():
        top_ratio = 0
        top_index = 0
        for broker_index, broker_row in brokers.iterrows():
            ratio = fuzz.QRatio(target_row['PartyCompanyName'], broker_row['Business Name'])
            if top_ratio < ratio:
                top_ratio = ratio
                top_index = broker_index
        print "Partial Ratio: {0} : {1} - {2}%".format(target_row['PartyCompanyName'], brokers.loc[top_index, ['Business Name']].values[0], top_ratio)

