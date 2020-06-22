# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 12:21:02 2019

@author: User
"""

import pandas as pd
from pandas import ExcelFile, ExcelWriter
from fuzzywuzzy import fuzz, process

raw_data = pd.read_excel("raw_address_ex.xlsx")
broker_data = pd.read_excel("broker_data.xlsx")

# removing redundant columns
raw_data = raw_data.iloc[:,:8]
# Substituting NaN values
mod_data_1 = raw_data.fillna("")
mod_data_1['full_address'] = mod_data_1['Address1'].astype(str) + ", " +  mod_data_1['Address2'].astype(str)  + \
 ", " + mod_data_1['City'].astype(str) + ", " + mod_data_1['State'].astype(str) + \
 ", " + mod_data_1['PostalCode'].astype(str)

# removing redundant columns from brokers
brokers = broker_data.drop(broker_data.columns[[2,3,4,5,6,7,8,9,10,11,18,19]], axis=1)
mod_brokers_1 = brokers.fillna("")
brokers.info()
mod_brokers_1['full_address'] = mod_brokers_1['Physical Street Address Line 1'].astype(str) + \
 ", " +  mod_brokers_1['Physical City'].astype(str)  + ", " + mod_brokers_1['Physical State Abbreviation'].astype(str) + \
 ", " + mod_brokers_1['Physical Zip (All)'].astype(str)
 
addresses = []
for index, row in mod_data_1.iterrows():
    raw_address = ap1.parse_address(row['full_address'])
    print "Address is: {0} {1} {2} {3} {4} {5} {6}. Unmatched: {7}".format(raw_address.city,
                       raw_address.house_number, raw_address.street_prefix, raw_address.street, raw_address.street_suffix, 
                       raw_address.state, raw_address.zip, raw_address.unmatched)
    addresses.append(raw_address)
 