#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
from functools import reduce
import requests
import json
#https://unipept.ugent.be/apidocs/taxonomy

def get_taxname(tax_id, tax_level):
    tags = {"S": "species_name", "G": "genus_name", "F": "family_name", "O":'order_name', "C": "class_name"}
    tax_level_tag = tags[tax_level]
    
    if str(tax_id) == "nan":
        tax_id = 1
    
    path = 'http://api.unipept.ugent.be/api/v1/taxonomy.json?input[]=' + str(int(tax_id)) + '&extra=true&names=true'
    complete_tax = requests.get(path).text

    # Check if the list returned by json.loads() is not empty (this fixed the get_abundance (1) error)
    tax_list = json.loads(complete_tax)
    if len(tax_list) > 0:
        name = tax_list[0][tax_level_tag]
    else:
        name = str(int(tax_id))

    return name

def get_abundance_values(names,paths):
    dfs = []
    for name,path in zip(names,paths):
        data = pd.read_csv(path, index_col=False, sep=';').iloc[:,1:]

        total = sum(data['reads_in_cluster'])
        rel_abundance=[]

        for index,row in data.iterrows():
            rel_abundance.append(row['reads_in_cluster'] / total)
            
        data['rel_abundance'] = rel_abundance
        dfs.append(pd.DataFrame({'taxid': data['taxid'], 'rel_abundance': rel_abundance}))
        data.to_csv("" + name + "_nanoclust_out.txt")

    return dfs

def merge_abundance(dfs,tax_level):
    df_final = reduce(lambda left,right: pd.merge(left,right,on='taxid',how='outer').fillna(0), dfs)
    df_final["taxid"] = [get_taxname(row["taxid"], tax_level) for index, row in df_final.iterrows()]
    df_final_grp = df_final.groupby(["taxid"], as_index=False).sum()
    return df_final_grp

def get_abundance(names,paths,tax_level):
    if(not isinstance(paths, list)):
        paths = [paths]
        names = [names]

    dfs = get_abundance_values(names,paths)
    df_final_grp = merge_abundance(dfs, tax_level)
    df_final_grp.to_csv("rel_abundance_"+ names[0] + "_" + tax_level + ".csv", index = False)

paths = "$table"
names = "$barcode"

get_abundance(names,paths, "G")
get_abundance(names,paths, "S")
get_abundance(names,paths, "O")
get_abundance(names,paths, "F")
