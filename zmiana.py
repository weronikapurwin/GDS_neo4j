import pandas as pd
import os

path = "C:\\Users\\weron\\.Neo4jDesktop\\relate-data\\dbmss\\dbms-19c53786-afd0-4ddc-aefa-168d71b41b77\\import"
for i in os.listdir(path):
    print(i)
    if "geo" in i:
        plik = pd.read_csv(path+"\\"+i)
        print(i)
        plik[':LABEL']='Geometria'
        plik.to_csv(f"D:\inzynierka\wynik\{i}",index=False)