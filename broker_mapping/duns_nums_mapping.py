# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 15:39:54 2019

@author: User
"""

import pandas as pd
from pandas import ExcelFile, ExcelWriter
from fuzzywuzzy import fuzz, process
import difflib

usi_brokers = pd.read_excel("Usi_Inc_data.xlsx")
usi_target = pd.read_excel("usi_target.xlsx")
mapped = usi_target.copy()
mapped.fillna("", inplace = True)

usi_brokers.info()
usi_target.info()
mapped.info()

cities = usi_target.City.unique()
len(cities)

#usi_source[usi_source.City.str.upper() == 'HOUSTON']['Address1'].to_numpy()
#usi_brokers[usi_brokers['Physical City'].str.upper() == 'HOUSTON']['Physical Street Address Line 1']



#type(houston_brokers.loc[42, ['Physical Street Address Line 1']].values[0])

def str_matched(source_str, target_str, threshold = 0.8999):
    '''
    Comparing any two strings with difflib if ratio > threshold return False
    '''
    if not isinstance(source_str, basestring):
        print "not a string value for source"
        return False
    if not isinstance(target_str, basestring):
        print "not a string value for target"
        return False
    ratio_ = difflib.SequenceMatcher(None, source_str, target_str).ratio()
    #print "Ratio for threshold {0} : {1}".format(threshold, ratio_)
    return  ratio_ > threshold

city_mapped = mapped.loc[mapped['City'].str.upper() == 'CHARLOTTE']
city_target = usi_target[usi_target.City.str.upper() == 'CHARLOTTE']
city_brokers = usi_brokers[usi_brokers['Physical City'].str.upper() == 'CHARLOTTE']



for target_index, target_row in city_target.iterrows():
    top_ratio = 0
    top_index = 0
    for broker_index, broker_row in city_brokers.iterrows():
        ratio = fuzz.token_set_ratio(target_row['Address1'], broker_row['Physical Street Address Line 1'])
        if top_ratio < ratio:
            top_ratio = ratio
            top_index = broker_index
    #variables
    source_zip = str(city_brokers.loc[top_index, ['Physical Zip (All)']].values[0])
    target_zip = str(city_target.loc[target_index, ['PostalCode']].values[0])
    source_name = str(city_brokers.loc[top_index, ['Business Name']].values[0])
    target_name = str(city_target.loc[target_index, ['PartyCompanyName']].values[0])
    zip_matched = str_matched(source_zip, target_zip)
    name_matched = str_matched(source_name, target_name, threshold = 0.2999)
    address_matched = (top_ratio/100.0) > 0.6299
    
    print "Ratio: {0} : {1} - {2}% ZIP:{3}, NAME:{4}".format(target_row['Address1'], 
              city_brokers.loc[top_index, ['Physical Street Address Line 1']].values[0], top_ratio,
              zip_matched, name_matched)
    # filling in mapped data
    city_mapped.loc[target_index, 'targets/brokers'] = str(len(city_target)) + "/"+str(len(city_brokers))
    city_mapped.loc[target_index, 'comments'] = "ONE BROKER MATCHED"
    city_mapped.loc[target_index, 'broker address'] = city_brokers.loc[top_index, ['Physical Street Address Line 1']].values[0]
    city_mapped.loc[target_index, 'match ratio'] = top_ratio/100.0
    city_mapped.loc[target_index, 'addr match'] = address_matched
    city_mapped.loc[target_index, 'MATCHED?'] = address_matched
    city_mapped.loc[target_index, 'broker zip'] = city_brokers.loc[top_index, ['Physical Zip (All)']].values[0]
    city_mapped.loc[target_index, 'zip match'] = zip_matched
    city_mapped.loc[target_index, 'broker name'] = city_brokers.loc[top_index,['Business Name']].values[0]
    city_mapped.loc[target_index, 'name match'] = name_matched
    if(address_matched):
        city_mapped.loc[target_index, 'Duns number'] = city_brokers.loc[top_index, ['Duns Number']].values[0]
        city_mapped.loc[target_index, 'Duns name'] = city_brokers.loc[top_index, ['Business Name']].values[0]
        city_mapped.loc[target_index, 'Global Duns Number'] = city_brokers.loc[top_index, ['Global Ultimate Duns Number']].values[0]
        city_mapped.loc[target_index, 'Global Business Name'] = city_brokers.loc[top_index, ['Global Ultimate Business Name']].values[0]


city_mapped.to_excel("City_mapped.xlsx", sheet_name='Auto Match')

#-----------------------------------------------------------------------------
for city in cities:
    targets = usi_target[usi_target.City.str.upper() == str(city).upper()]
    brokers = usi_brokers[usi_brokers['Physical City'].str.upper() == str(city).upper()]
    mapped.loc[mapped['City'].str.upper() == str(city).upper(), "targets/brokers"] = str(len(targets)) + "/"+str(len(brokers))
    print "--------------------------------------------------"
    print "{0} - Targets: {1}; Brokers: {2}".format(city, len(targets), len(brokers))
    if(len(brokers) == 0):
        print "NO BROKER DATA AVAILABLE"
        mapped.loc[mapped['City'].str.upper() == str(city).upper(), 'targets/brokers'] = str(len(targets)) + "/"+str(len(brokers))
        mapped.loc[mapped['City'].str.upper() == str(city).upper(), 'comments'] = "NO BROKER DATA AVAILABLE"
        mapped.loc[mapped['City'].str.upper() == str(city).upper(), 'MATCHED?'] = False
        continue
    if((len(brokers) == 1) & (len(targets) == 1)):
        mapped.loc[mapped['City'].str.upper() == str(city).upper(), 'targets/brokers'] = str(len(targets)) + "/"+str(len(brokers))
        mapped.loc[mapped['City'].str.upper() == str(city).upper(), 'comments'] = "ONE BROKER MATCHED"
        mapped.loc[mapped['City'].str.upper() == str(city).upper(), 'broker address'] = brokers['Physical Street Address Line 1'].values[0]
        mapped.loc[mapped['City'].str.upper() == str(city).upper(), 'broker zip'] = brokers['Physical Zip (All)'].values[0]
        #mapped.loc[mapped['City'].str.upper() == str(city).upper(), 'zip match'] = str_matched(brokers['Physical Zip (All)'].values[0], targets['PostalCode'].values[0])
        mapped.loc[mapped['City'].str.upper() == str(city).upper(), 'broker name'] = brokers['Business Name'].values[0]
        #mapped.loc[mapped['City'].str.upper() == str(city).upper(), 'name match'] = str_matched(brokers['Business Name'].values[0], ['PartyCompanyName'].values[0])
        mapped.loc[mapped['City'].str.upper() == str(city).upper(), 'Duns number'] = brokers['Duns Number'].values[0]
        mapped.loc[mapped['City'].str.upper() == str(city).upper(), 'Duns name'] = brokers['Business Name'].values[0]
        mapped.loc[mapped['City'].str.upper() == str(city).upper(), 'Global Duns Number'] = brokers['Global Ultimate Duns Number'].values[0]
        mapped.loc[mapped['City'].str.upper() == str(city).upper(), 'Global Business Name'] = brokers['Global Ultimate Business Name'].values[0]
        mapped.loc[mapped['City'].str.upper() == str(city).upper(), 'MATCHED?'] = True
        continue
    for target_index, target_row in targets.iterrows():
        top_ratio = 0
        top_index = 0
        for broker_index, broker_row in brokers.iterrows():
            ratio = fuzz.token_set_ratio(target_row['Address1'], broker_row['Physical Street Address Line 1'])
            if top_ratio < ratio:
                top_ratio = ratio
                top_index = broker_index
        source_zip = str(brokers.loc[top_index, ['Physical Zip (All)']].values[0])
        target_zip = str(targets.loc[target_index, ['PostalCode']].values[0])
        source_name = str(brokers.loc[top_index, ['Business Name']].values[0])
        target_name = str(targets.loc[target_index, ['PartyCompanyName']].values[0])
        print "Ratio: {0} : {1} - {2}% ZIP:{3}, NAME:{4}".format(target_row['Address1'], 
                  brokers.loc[top_index, ['Physical Street Address Line 1']].values[0], top_ratio,
                  str_matched(source_zip, target_zip), str_matched(source_name, target_name, threshold = 0.333))
        mapped.loc[target_index, 'targets/brokers'] = str(len(targets)) + "/"+str(len(brokers))
        mapped.loc[target_index, 'comments'] = "ONE BROKER MATCHED"
        mapped.loc[target_index, 'broker address'] = brokers.loc[top_index, ['Physical Street Address Line 1']].values[0]
        mapped.loc[target_index, 'match ratio'] = top_ratio/100.0
        address_matched = (top_ratio/100.0) > 0.6299
        mapped.loc[target_index, 'addr match'] = address_matched
        mapped.loc[target_index, 'MATCHED?'] = address_matched
        mapped.loc[target_index, 'broker zip'] = brokers[top_index, ['Physical Zip (All)']].values[0]
        #mapped.loc[mapped['City'].str.upper() == str(city).upper(), 'zip match'] = str_matched(brokers['Physical Zip (All)'].values[0], targets['PostalCode'].values[0])
        mapped.loc[target_index, 'broker name'] = brokers[top_index,['Business Name']].values[0]
        #mapped.loc[mapped['City'].str.upper() == str(city).upper(), 'name match'] = str_matched(brokers['Business Name'].values[0], ['PartyCompanyName'].values[0])
        if(address_matched):
            mapped.loc[target_index, 'Duns number'] = brokers[top_index, ['Duns Number']].values[0]
            mapped.loc[target_index, 'Duns name'] = brokers[top_index, ['Business Name']].values[0]
            mapped.loc[target_index, 'Global Duns Number'] = brokers[top_index, ['Global Ultimate Duns Number']].values[0]
            mapped.loc[target_index, 'Global Business Name'] = brokers[top_index, ['Global Ultimate Business Name']].values[0]
        
        
#-----------------------------------------------------------------------------
