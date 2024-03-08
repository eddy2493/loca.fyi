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

is24api = ImmoScout24API()
gwr = GwrUtil()

bfs_zuerich = 261
bfs_olten = 2581


listings = []
for plz in gwr.getPLZList(bfs_zuerich):
    listings.extend(is24api.get_listings(plz))

with open('all_listings.json', 'w') as f:
    json.dump(listings, f)