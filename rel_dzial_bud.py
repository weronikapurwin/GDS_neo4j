import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import os

if __name__=="__main__":
   
   directory = 'dane'

   for i in range(8,16,2):


      relation = pd.DataFrame()

      for wojew in tqdm(os.listdir(directory)[i:i+2]):
        dzialki_final = gpd.GeoDataFrame()
        budynki_final = gpd.GeoDataFrame()
        f = os.path.join(directory, wojew)
        for kod in tqdm(os.listdir(f)):
            g = os.path.join(f, kod)
            print(g)
            for plik in os.listdir(g):
                h = os.path.join(g, plik)
                if 'dzial' in plik and '.shp' in plik:
                  dzialki = gpd.read_file(h)
                if 'bud' in plik and '.shp' in plik:
                  budynki = gpd.read_file(h)
                else:
                  continue
            '''zamiana numpy nan na nulle pythonowe'''
            dzialki = dzialki.replace({np.nan: None})
            budynki = budynki.replace({np.nan: None})

            # Remove rows with invalid geometries
            dzialki = dzialki[dzialki['geometry'].is_valid]
            budynki = budynki[budynki['geometry'].is_valid]

            dzialki.set_crs(epsg=2180, inplace=True)
            budynki.set_crs(epsg=2180, inplace=True)

            if 'idDzialki' in dzialki.columns:
               dzialki.rename(columns = {'idDzialki':'ID_DZIALKI'}, inplace = True)
               if 'ID_DZIALKI' in dzialki.columns:
                  dzialki_final = pd.concat([dzialki_final, dzialki], ignore_index=True)
               else:
                  continue
               
            if 'idBudynku' in budynki.columns:
                budynki.rename(columns = {'idBudynku':'ID_BUDYNKU'}, inplace = True)
                if 'ID_BUDYNKU' in budynki.columns:
                    budynki_final = pd.concat([budynki_final, budynki], ignore_index=True)
                else:
                   continue

            else:
                if 'ID_DZIALKI' in dzialki.columns:
                    dzialki_final = pd.concat([dzialki_final, dzialki], ignore_index=True)
                if 'ID_BUDYNKU' in budynki.columns:
                    budynki_final = pd.concat([budynki_final, budynki], ignore_index=True)
                else:
                  continue


        '''sprawdzenie na której działce znajduje się budynek i przypisanie tej informacji do tabeli'''
        budynki_dzialki_match = gpd.sjoin(budynki_final, dzialki_final, how="left", op="intersects")
        budynki_dzialki_match.dropna(subset=['ID_BUDYNKU', 'ID_DZIALKI'], inplace=True)
        budynki_dzialki_match = budynki_dzialki_match[['ID_BUDYNKU', 'ID_DZIALKI']]
        relation = pd.concat([relation, budynki_dzialki_match], ignore_index=True)
        del budynki_final
        del dzialki_final
        del dzialki
        del budynki


      print('lolo')
      relation[':TYPE']='IS_IN'
      relation.rename(columns = {'ID_BUDYNKU':':START_ID', 'ID_DZIALKI':':END_ID'}, inplace = True)
      relation.drop_duplicates(subset=[':START_ID', ':END_ID'], inplace=True)

      relation.to_csv(f'wynik\\rel_bud_dzia{i}.csv', index=False)

      del relation