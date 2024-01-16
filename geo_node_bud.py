import pandas as pd
import geopandas as gpd
import numpy as np
from tqdm import tqdm
import os

if __name__=="__main__":
   
   directory = 'D:\inzynierka\dane'
   

   for i in range(10,12,2):
      budynki_final = pd.DataFrame()

      for wojew in tqdm(os.listdir(directory)[i:i+2]):
         f = os.path.join(directory, wojew)
         for kod in tqdm(os.listdir(f)):
            g = os.path.join(f, kod)
            print(g)
            for plik in os.listdir(g):
               h = os.path.join(g, plik)
               if 'bud' in plik and '.shp' in plik:
                  budynki = gpd.read_file(h)

               else:
                  continue
               
            '''zamiana numpy nan na nulle pythonowe'''
            budynki = budynki.replace({np.nan: None})

            # Remove rows with invalid geometries
            budynki = budynki[budynki['geometry'].is_valid]

            budynki.set_crs(epsg=2180, inplace=True)

            geom_bud = [x.geom_type for x in budynki.geometry]
            budynki['type'] = geom_bud


            if 'idBudynku' in budynki.columns:
                budynki.rename(columns = {'idBudynku':'ID_BUDYNKU'}, inplace = True)
                if 'ID_BUDYNKU' in budynki.columns:
                    budynki_final = pd.concat([budynki_final, budynki[['ID_BUDYNKU', 'geometry', 'type']]], ignore_index=True)
                else:
                   continue                  
            else:
                if 'ID_BUDYNKU' in budynki.columns:
                    budynki_final = pd.concat([budynki_final, budynki[['ID_BUDYNKU', 'geometry', 'type']]], ignore_index=True)

                else:
                   continue




      print('lolo')

      budynki_final[':LABEL']='Geometry'
      budynki_final.rename(columns = {'ID_BUDYNKU':'ID:ID'}, inplace = True)
      budynki_final['format'] = 'WKT'
      '''usuniecie tych wierszy co maja puste id'''
      print(budynki_final.columns)
      budynki_final.dropna(subset=['ID:ID'], inplace=True)
      '''usuniecie duplikatow id'''
      budynki_final.drop_duplicates(subset=['ID:ID'], inplace=True)
      budynki_final['ID:ID']='geo.'+budynki_final['ID:ID']

      budynki_final.to_csv(f'wynik\\geo_budynki{i}.csv', columns=['ID:ID', 'format','type', 'geometry', ':LABEL'], index=False)

      del budynki_final


   
