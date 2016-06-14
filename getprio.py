
# coding: utf-8


import requests
import pandas as pd
import json
import datetime
import os



print("Starting.")
start = datetime.datetime.now()

gridurl = "http://grid.prio.org/api/data/basegrid"
print("Getting grid from ", gridurl, "", end="...")
df_grid = pd.read_json(path_or_buf=gridurl)
print("done")



#make df_gy as a skeleton df for which to left-merge into
print("Making year list", end="...")
yearlist = list(range(1946, datetime.date.today().year+1))
yearlist.append(0)
df_gy = pd.DataFrame(columns=['year', 'gid'])

for year in yearlist:
    df = df_grid.copy()
    df['year'] = year
    df_gy = df_gy.append(df)
print("done")



#make df_vars containing id and name for the variables, excluding those that give API errors
varurl = "http://grid.prio.org/api/variables"
print("Getting variable list from ", varurl, "", end="...")
df_vars = pd.read_json(path_or_buf=varurl)
#keep only the id and name, we use the id for fetching the data
df_vars = df_vars[['id', 'name']]
#These throw API errors
excludelist = ["gid", "row", "col", "xcoord", "ycoord"]
df_vars = df_vars[~df_vars['name'].isin(excludelist)]
print("done")



#fetch the data from grid.prio.org/api one variable at a time
#store each variable in json file named after the variable id number in subfolder jsons

#make the jsons dir if it doesn't exist
if not os.path.isdir("./jsons"):
   os.makedirs("./jsons")

baseurl = "http://grid.prio.org/api/data/"
year_range = "?startYear=" + str(1946) + "&endYear=" + str(datetime.date.today().year)  
print("Downloading data...")

#for each variable
for i, row in df_vars.iterrows():
    url = baseurl+str(row['id'])+year_range
    print("Fetching var", row['name'], "with index ", row['id'], "at url", url, "", end="...")
    r = requests.get(url)
    obj = r.json()
    print("done", end=" ... ")

    filename="./jsons/" + str(row['id']) + ".json"
    with open(filename, 'w') as f:
        print("dumping to ", filename, end="...")
        json.dump(obj,f)
        print("done!")
apitime = datetime.datetime.now()
print("All data downloaded and stored in ./jsons/ folder, API time: ", apitime-start)



print("Starting merge.")
df_merged = df_gy
#iterate over all the saves jsons    
for filename in os.listdir('./jsons/'):
    path='./jsons/'+filename
    #load the json into obj
    with open (path, 'r') as f:
        obj = json.load(f)
    
    name = obj['variable']['name']
    df = pd.DataFrame.from_dict(obj['cells'])
    df.rename(columns={'value' : name}, inplace=True)
    print(name, path, "variables shape: ", df.shape, end="")
    df.drop_duplicates(inplace=True, subset=['gid', 'year'])
    df_merged = df_merged.merge(df, how='left', left_on=['gid', 'year'], right_on=['gid', 'year'])
    print(" merged shape: ", df_merged.shape, " done!")

print("Done!")
mergetime = datetime.datetime.now()
print("Total time :", mergetime - start)
print("API time: ", apitime - start)
print("Merge time: ", mergetime - apitime)

