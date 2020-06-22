# -*- coding: utf-8 -*-
"""
Created on Fri May 10 12:07:16 2019

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 12:26:03 2019

@author: User
"""

import pandas as pd
from pandas import ExcelFile, ExcelWriter
from fuzzywuzzy import fuzz, process
import difflib
import unicodedata
import re



#usi_brokers = pd.read_excel("D&B_brokers_copy.xlsx")
usi_brokers = pd.read_excel("DB_NormBrokers.xlsx")
usi_target = pd.read_excel("")
#usi_target = pd.read_excel("brokers_city_checked.xlsx")
usi_target.fillna("", inplace = True)


target_global_name = usi_target["Broker"].unique()[0]
brokers_data = usi_brokers.loc[usi_brokers["Global Ultimate Business Name"].str.match(target_global_name)]

#-----------------------------------------------------------------------------
usi_target['full_address'] = usi_target['Address1'].astype('unicode') + ", " +  usi_target['Address2'].astype('unicode')
#-----------------------------------------------------------------------------
mapped = usi_target.copy()
mapped.info()
#normilizing mapped cities nam

brokers_data.info()
usi_target.info()
mapped.info()


def normStrUpRemSpChAndBnsNames(s):
    #s = unicodeToAscii(s.upper().strip())
    # remove text within parentheses
    s = re.sub(r'\([^)]*\)', "", s)
    s = re.sub(r'\([^)]*', "", s)
    # remove special characters
    s = re.sub(r"([-])", r" ", s)
    s = re.sub(r"([.,!?#&])", r"", s)
    s = unicodeToAscii(s.upper().strip())
    s = re.sub(r"\sCORP($|\s)", r" ", s)
    s = re.sub(r"\sLTD($|\s)", r" ", s)
    s = re.sub(r"\sLTDA($|\s)", r" ", s)
    s = re.sub(r"\sINC($|\s)", r" ", s)
    s = re.sub(r"\sLLC($|\s)", r" ", s)
    s = re.sub(r"\sCO($|\s)", r" ", s)
    s = re.sub(r"\sINS($|\s)", r" ", s)
    s = re.sub(r"\sLIMITED($|\s)", r" ", s)                
    return s.strip()

brokers_names = usi_brokers["Global Ultimate Business Name"].unique()
brokers_names_mod = []
brokers_names_mod = [normStrUpRemSpChAndBnsNames(name) for name in brokers_names]

target_names_mod = []
target_names_mod = [normStrUpRemSpChAndBnsNames(name) for name in target_global_name]

len(brokers_names)
len(brokers_names_mod)


# Turn a Unicode string to plain ASCII, thanks to
# https://stackoverflow.com/a/518232/2809427
def unicodeToAscii(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

# Lowercase, trim, and remove non-letter characters
def normalizeString(s):
    s = unicodeToAscii(s.upper().strip())
    # remove text within parentheses
    s = re.sub(r'\([^)]*\)', "", s)
    s = re.sub(r'\([^)]*', "", s)
    # remove special characters
    s = re.sub(r"([.,!?#-])", r" ", s)
    #s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    #s = re.sub(r"\s+", r" ", s).strip()
    return s

for city in mapped.City:
    if city:
        city = normalizeString(city)

for city in mapped.City:
    if city:
        print city


# creating list of normalized city names
cities = []
for city in usi_target.City.unique():
    cities.append(normalizeString(unicode(city, 'utf8')))    
len(cities)


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

match_p = 0.0

for city in cities:
    target_city = normalizeString(unicode(usi_target.City, 'utf8'))
    targets = usi_target[target_city == city]    
    brokers = brokers_data[normalizeString(unicode(brokers_data['Physical City'], 'utf8')) == city]
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
        print "ONE BROKER MATCHED"
        print "{0}, {1}".format(brokers['Physical Street Address Line 1'].values[0], brokers['Business Name'].values[0])
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
            ratio = fuzz.token_set_ratio(target_row['full_address'], broker_row['Physical Street Address Line 1'])
            if top_ratio < ratio:
                top_ratio = ratio
                top_index = broker_index
                
        source_zip = str(brokers.loc[top_index, ['Physical Zip (All)']].values[0])
        target_zip = str(targets.loc[target_index, ['PostalCode']].values[0])
        source_name = str(brokers.loc[top_index, ['Business Name']].values[0])
        target_name = str(targets.loc[target_index, ['PartyCompanyName']].values[0])
        zip_matched = str_matched(source_zip, target_zip)
        name_matched = str_matched(source_name, target_name, threshold = 0.2999)
        address_matched = (top_ratio/100.0) > 0.6299     
        
        print "Ratio: {0} : {1} - {2}% ZIP:{3}, NAME:{4}".format(target_row['full_address'], 
                  brokers.loc[top_index, ['Physical Street Address Line 1']].values[0], top_ratio,
                  str_matched(source_zip, target_zip), str_matched(source_name, target_name, threshold = 0.333))
        mapped.loc[target_index, 'targets/brokers'] = str(len(targets)) + "/"+str(len(brokers))
        mapped.loc[target_index, 'comments'] = ""
        mapped.loc[target_index, 'broker address'] = brokers.loc[top_index, ['Physical Street Address Line 1']].values[0]
        mapped.loc[target_index, 'match ratio'] = top_ratio/100.0
        mapped.loc[target_index, 'addr match'] = address_matched
        mapped.loc[target_index, 'MATCHED?'] = address_matched
        mapped.loc[target_index, 'broker zip'] = brokers.loc[top_index, ['Physical Zip (All)']].values[0]
        mapped.loc[target_index, 'zip match'] = zip_matched
        mapped.loc[target_index, 'broker name'] = brokers.loc[top_index,['Business Name']].values[0]
        mapped.loc[target_index, 'name match'] = name_matched
        if(address_matched):
            mapped.loc[target_index, 'Duns number'] = brokers.loc[top_index, ['Duns Number']].values[0]
            mapped.loc[target_index, 'Duns name'] = brokers.loc[top_index, ['Business Name']].values[0]
            mapped.loc[target_index, 'Global Duns Number'] = brokers.loc[top_index, ['Global Ultimate Duns Number']].values[0]
            mapped.loc[target_index, 'Global Business Name'] = brokers.loc[top_index, ['Global Ultimate Business Name']].values[0]
print "================================="
match_p = round(mapped.loc[mapped["MATCHED?"]==True, "MATCHED?"].count().astype("float")/mapped["Broker"].count(), 4)
print "{0} - {1}% matched".format(target_global_name, match_p)

sheet_name = 'Auto Match-'+str(match_p)+'%'
file_name = "AutoMapped_2_"+str(target_global_name)+".xlsx"
mapped.to_excel(file_name, sheet_name=sheet_name)