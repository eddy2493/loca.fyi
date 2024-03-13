#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 12:36:41 2024

@author: gnms
"""


# Lookup BFS Number on Google

import requests
from immoscout24api import ImmoScout24API
from gwrutil import GwrUtil
import json
import pandas as pd
import os
from datetime import datetime

is24api = ImmoScout24API()
gwr = GwrUtil()

bfs_zuerich = 261
bfs_olten = 2581
bfs_pieterlen = 392
bfs_num = bfs_pieterlen

### Download Listings from immoscout as <date>_<municipality>_listings.json
listings = []
for plz in gwr.getPLZList(bfs_num):
    listings.extend(is24api.get_listings(plz))

today = datetime.now().strftime("%Y%m%d")
with open(today+"_"+gwr.getGemeindeName(bfs_num)+'_listings.json', 'w') as f:
    json.dump(listings, f)

### Downloads information from bfs about Entrances, Buildings, and Appartements in the folder <municipality>
gwr.download(bfs_num)



