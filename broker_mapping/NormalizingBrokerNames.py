# -*- coding: utf-8 -*-
"""
Created on Mon May 13 12:27:10 2019

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May 10 18:00:45 2019

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
import difflib, unicodedata, re
import datetime

usi_brokers = pd.read_excel("D&B_brokers_copy.xlsx")
# Dropping rows where city is missing
usi_brokers = usi_brokers.dropna(subset=["Norm City"])
# Check
len(usi_brokers.loc[usi_brokers["Norm City"].isna() == True])

def unicodeToAscii(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def normString(s):
    s = unicodeToAscii(s.strip())
    # remove text within parentheses
    s = re.sub(r'\([^)]*\)', "", s)
    s = re.sub(r'\([^)]*', "", s)
    return s

def normStrUpperRemoveSpecChars(s):
    s = unicodeToAscii(s.upper().strip())
    # remove text within parentheses
    s = re.sub(r'\([^)]*\)', "", s)
    s = re.sub(r'\([^)]*', "", s)
    # remove special characters
    #s = re.sub(r"([-])", r" ", s)
    s = re.sub(r"([.,!?#&])", r"", s)
    return s


usi_brokers["Norm Broker Name"] = ""
usi_brokers["Norm City"] = ""

usi_brokers["Physical City"].tail()

usi_brokers.info()

usi_brokers["Norm City", "Global Ultimate Business Name"].tail()

for broker_index, broker_row in usi_brokers.iterrows():
    usi_brokers.loc[broker_index, "Norm Broker Name"] = normString(usi_brokers.loc[broker_index, "Global Ultimate Business Name"])   

for broker_index, broker_row in usi_brokers.iterrows():
    usi_brokers.loc[broker_index, "Norm City"] = normStrUpperRemoveSpecChars(usi_brokers.loc[broker_index, "Physical City"])
   
   
usi_brokers.to_excel("DB_NormBrokers.xlsx", "Normalized brokers")
    