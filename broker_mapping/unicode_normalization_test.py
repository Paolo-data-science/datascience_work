# -*- coding: utf-8 -*-
"""
Created on Fri May 10 14:23:40 2019

@author: User
"""


import unicodedata
import re


test =["Caja Nacl De Ahorro Y Seguro  (Argentina)",
       "6 SHENTON WAY #28-08,",
       "FELIX PARRA 39,COL. SAN JOSE",
       "4-2 Otemachi 1-chome, Chiyoda-ku,",
       "Compagnie Europeene D'Assu Industrielles  (Belgium",
       "Clarkson Puckle Group Ltd.   (Cde 779)",
       "Skandia Forsakringsaktiebolaget (Hk Br)  (H Kong)",
       ".nollys House,",
       "Societe Anonyme Francaise De Reassu  (France)",
       "Hansa Marine Ins Co (UK) Ltd",
       "Köln"
       ]

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

for item in test:
    _str = normalizeString(unicode(item, 'utf8'))
    print _str
