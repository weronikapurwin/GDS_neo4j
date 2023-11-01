import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import os

if __name__=="__main__":
   
   directory = 'dane'

   # relation = pd.DataFrame()
   # obreb = read_file('obreb')

   for i in range(6,8,2):

      dzialki_final = pd.DataFrame()
      for wojew in tqdm(os.listdir(directory)[i:i+2]):
         f = os.path.join(directory, wojew)
         for kod in tqdm(os.listdir(f)):
            g = os.path.join(f, kod)
            print(g)
            for plik in os.listdir(g):
               h = os.path.join(g, plik)
               if 'dzial' in plik and '.shp' in plik:
                  dzialki = gpd.read_file(h)
               else:
                  continue
            '''zamiana numpy nan na nulle pythonowe'''
            dzialki = dzialki.replace({np.nan: None})

            # Remove rows with invalid geometries
            dzialki = dzialki[dzialki['geometry'].is_valid]
            # obreb = obreb[obreb['geometry'].is_valid]

            dzialki.set_crs(epsg=2180, inplace=True)
            # obreb.to_crs(epsg=2180, inplace=True)

            # dzialka_obreb = gpd.sjoin(dzialki, obreb, how="left", op="intersects")
            # dzialka_obreb.dropna(subset=['ID_DZIALKI', 'JPT_KOD_JE'], inplace=True)
            # dzialka_obreb = dzialka_obreb[['ID_DZIALKI', 'JPT_KOD_JE']]
            # relation = pd.concat([relation, dzialka_obreb], ignore_index=True)
            if 'idDzialki' in dzialki.columns:
               dzialki.rename(columns = {'idDzialki':'ID_DZIALKI'}, inplace = True)
               if 'ID_DZIALKI' in dzialki.columns:
                  dzialki_final = pd.concat([dzialki_final, dzialki], ignore_index=True)
               else:
                  continue

            else:
               if 'ID_DZIALKI' in dzialki.columns:
                  dzialki_final = pd.concat([dzialki_final, dzialki], ignore_index=True)
               else:
                  continue


            '''sprawdzenie na której działce znajduje się budynek i przypisanie tej informacji do tabeli'''
            # budynki_dzialki_match = gpd.sjoin(budynki, dzialki, how="left", op="intersects")
            # budynki_dzialki_match.dropna(subset=['ID_BUDYNKU', 'ID_DZIALKI'], inplace=True)
            # budynki_dzialki_match = budynki_dzialki_match[['ID_BUDYNKU', 'ID_DZIALKI']]


      print('lolo')
      # relation['typ']='IS_IN'
      # relation.to_csv('csvki\\rel_dzial_obreb.csv', index=False)

      dzialki_final[':LABEL']='Dzialka'
      dzialki_final.rename(columns = {'ID_DZIALKI':'ID_DZIALKI:ID'}, inplace = True)
      dzialki_final.dropna(subset=['ID_DZIALKI:ID'], inplace=True)
      dzialki_final.drop_duplicates(subset=['ID_DZIALKI:ID'], inplace=True)

      dzialki_final.to_csv(f'wynik\\dzialki{i}.csv', columns=['ID_DZIALKI:ID', 'NUMER_DZIA', 'NUMER_OBRE', 'NUMER_JEDN', 'NAZWA_OBRE', 'NAZWA_GMIN', ':LABEL'], index=False)

      del dzialki_final