import pandas as pd
import geopandas as gpd
import numpy as np
from tqdm import tqdm
import os

if __name__=="__main__":
   
   directory = 'dane'
   

   for i in range(0,16,2):
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

            dzialki.set_crs(epsg=2180, inplace=True)



            if 'idDzialki' in dzialki.columns:
               dzialki.rename(columns = {'idDzialki':'ID_DZIALKI'}, inplace = True)
               if 'ID_DZIALKI' in dzialki.columns:
                  dzialki_final = pd.concat([dzialki_final, dzialki[['ID_DZIALKI', 'geometry']]], ignore_index=True)
               else:
                  continue

            else:
               if 'ID_DZIALKI' in dzialki.columns:
                  dzialki_final = pd.concat([dzialki_final, dzialki[['ID_DZIALKI', 'geometry']]], ignore_index=True)
               else:
                  continue



      print('lolo')


      dzialki_final.rename(columns = {'ID_DZIALKI':':START_ID'}, inplace = True)
      '''usuniecie rekordow bez id'''
      dzialki_final[':TYPE']='HAS_GEOMETRY'
      '''usuniecie tych wierszy co maja puste id'''
      dzialki_final.dropna(subset=[':START_ID'], inplace=True)
      '''usuniecie duplikatow id'''
      dzialki_final.drop_duplicates(subset=[':START_ID'], inplace=True)
      dzialki_final[':END_ID']='geo.'+dzialki_final[':START_ID']

      dzialki_final.to_csv(f'wynik\\rel_geo_dzialki{i}.csv', columns=[':START_ID', ':END_ID',':TYPE'], index=False)

      del dzialki_final


   
