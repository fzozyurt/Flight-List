import pandas as pd
import numpy as np
import requests
import json
import time

dir = "Data/"
depData=pd.read_csv(dir+"depData.csv", sep=';')
#arrData = pd.read_csv(dir+"arrData.csv", sep=';')
arrData=pd.DataFrame()

# Get DepData
response = requests.get("https://www.flypgs.com/portmatrix/departure?lang=tr",verify=False)
data=pd.json_normalize(response.json()["data"],"portMatrixPorts",["countryName","countryCode"],record_prefix="")
data.drop(["filter",
"portMatrixId",
"portMatrix",
"languageId",
"sort",
"id",
"createdDate",
"modifiedDate",
"status"],axis=1,inplace=True)
data.to_csv(dir+"depData.csv",index=False,sep=";")

# Get ArrData
for index,row in data.iterrows():
    print(row["portName"])
    if "Tümü" not in row["portName"]:
        portCode=row["portCode"]
        i=0
        while i<=2:
            try:
                response = requests.get(f"https://www.flypgs.com/portmatrix/arrival?lang=tr&depcode={portCode}",verify=False)
                arrData_sub=pd.json_normalize(response.json()["data"],"portMatrixPorts",["countryName","countryCode"],record_prefix="")
                arrData_sub.drop(["filter",
                "portMatrixId",
                "portMatrix",
                "languageId",
                "sort",
                "id",
                "createdDate",
                "modifiedDate",
                "status"],axis=1,inplace=True)
                arrData_sub["depPortCode"]=portCode
                print(f"{portCode} OK")
                arrData = pd.concat([arrData, arrData_sub])
                print(f"{portCode} Merged")
                break
            except:
                i=i+1
                time.sleep(20)
                
#arrData Export
arrData.to_csv(dir+"arrData.csv",index=False,sep=";")