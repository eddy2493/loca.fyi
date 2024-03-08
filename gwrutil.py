#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 06:37:46 2024

@author: gnms
"""
import requests as re
import pandas as pd
import warnings
import zipfile
import os

class GwrUtil:
    def __init__(self, gemeindestand_path="Gemeindestand.xlsx", ortschaftenverz_path='AMTOVZ_CSV_LV95.csv'):
        self.MADD_URL = "https://public.madd.bfs.admin.ch/"
        warnings.simplefilter("ignore")
        self.gemeinde_df = pd.read_excel(gemeindestand_path, engine="openpyxl")
        self.ortschaften_df = pd.read_csv(ortschaftenverz_path, sep=";")
        self.ortschaften_df.rename(columns={'BFS-Nr': 'BFS_Nr'}, inplace=True)
        
    def getCantonCode(self, bfs_nummer):
        try:
            return self.gemeinde_df.loc[self.gemeinde_df['BFS Gde-nummer']==bfs_nummer, 'Kanton'].values[0]
        except:
            print("Could not return Canton")
    
    def getGemeindeName(self, bfs_nummer):
        try:
            return self.gemeinde_df.loc[self.gemeinde_df['BFS Gde-nummer']==bfs_nummer, 'Gemeindename'].values[0]
        except:
            print("Could not return Gemeindename")
    
    def getPLZList(self, bfs_nummer):
        try: 
            return self.ortschaften_df.query('BFS_Nr==@bfs_nummer')['PLZ'].to_list()
        except:
            print("Could not return PLZ list")
            
    def download(self, bfs_nummer, dest_folder):
        if not os.path.isdir(dest_folder):
            canton_code = self.getCantonCode(bfs_nummer).lower()
            response = re.get(self.MADD_URL+canton_code+'.zip')
            with open(canton_code+'.zip', 'wb') as f:
                f.write(response.content)
            with zipfile.ZipFile(canton_code+'.zip', 'r') as zip_ref:
                zip_ref.extractall(dest_folder)
            os.remove(canton_code+'.zip')
            
            items = os.listdir(dest_folder)
            for item in items:
                if item.endswith(".pdf"):
                    os.remove(os.path.join(dest_folder, item))
            os.remove(os.path.join(dest_folder, "data.sqlite"))
            os.remove(os.path.join(dest_folder, "kodes_codes_codici.csv"))
            