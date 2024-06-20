import pandas as pd
import numpy as np
import requests
import json
import time
import datetime

dir = "Data/"
arrData = pd.read_csv(dir+"arrData.csv", sep=';')

try:
    priceDataDF=pd.read_csv(dir+"priceData.csv", sep=';')
except:
    priceDataDF=pd.DataFrame()

for index,row in arrData.iterrows():
    print(row["portName"])
    if "Tümü" not in row["portName"]:
        portCode=row["portCode"]
        i=0
        while i<=2:
            try:
                headers = {"Content-Type": "application/json; charset=utf-8", "Referer":"https://www.flypgs.com/","Origin":"https://www.flypgs.com","Host":"www.flypgs.com"}
                Body_Data={
                    "depPort": f"{row['depPortCode']}",
                    "arrPort": f"{row['portCode']}",
                    "flightDate": f"{datetime.datetime.now().strftime('%Y-%m-%d')}",
                    "currency": "TRY"
                }
                response=requests.post("https://www.flypgs.com/apint/cheapfare/flight-calender-prices",headers=headers, json = Body_Data,verify=False)
                data=pd.json_normalize(response.json()["cheapFareFlightCalenderModelList"],"days",["depPort","arrPort","month"],record_prefix="")
                priceDataDF = pd.concat([priceDataDF, data])
                print(f"{portCode} OK")
                break
            except:
                i=i+1
                time.sleep(20)

priceDataDF=priceDataDF.drop_duplicates()
priceDataDF.reset_index(inplace=True)
priceDataDF.drop("index",axis=1,inplace=True)
#PriceData Export
priceDataDF.to_csv(dir+"priceData.csv",index=False,sep=";")