import pandas as pd
import geopandas as gpd
import numpy as np
from tqdm import tqdm
import os

if __name__=="__main__":
   
   directory = 'dane'
   

   for i in range(0,16,2):
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


            if 'idBudynku' in budynki.columns:
                budynki.rename(columns = {'idBudynku':'ID_BUDYNKU'}, inplace = True)
                if 'ID_BUDYNKU' in budynki.columns:
                    budynki_final = pd.concat([budynki_final, budynki[['ID_BUDYNKU', 'geometry']]], ignore_index=True)
                else:
                   continue                  
            else:
                if 'ID_BUDYNKU' in budynki.columns:
                    budynki_final = pd.concat([budynki_final, budynki[['ID_BUDYNKU', 'geometry']]], ignore_index=True)

                else:
                   continue




      print('lolo')

      budynki_final[':TYPE']='HAS_GEOMETRY'
      budynki_final.rename(columns = {'ID_BUDYNKU':':START_ID'}, inplace = True)
      '''usuniecie tych wierszy co maja puste id'''
      budynki_final.dropna(subset=[':START_ID'], inplace=True)
      '''usuniecie duplikatow id'''
      budynki_final.drop_duplicates(subset=[':START_ID'], inplace=True)
      budynki_final[':END_ID']='geo.'+budynki_final[':START_ID']

      budynki_final.to_csv(f'wynik\\rel_geo_budynki{i}.csv', columns=[':START_ID', ':END_ID',':TYPE'], index=False)

      del budynki_final


   
