import pandas as pd
import geopandas as gpd
from tqdm import tqdm
import os
from itertools import product

if __name__=="__main__":

   directory = 'D:\\inzynierka\\dane_admin'
   geo_df_woj = gpd.GeoDataFrame()
   geo_df_pow = gpd.GeoDataFrame()
   geo_df_gmin = gpd.GeoDataFrame()
   geo_df_jedn = gpd.GeoDataFrame()
   geo_df_obreb = gpd.GeoDataFrame()

   '''petla idaca po katalogu z danymi'''
   for wojew in tqdm(os.listdir(directory)):
      f = os.path.join(directory, wojew)
      '''podkatalogi'''
      for plik in tqdm(os.listdir(f)):
         h = os.path.join(f, plik)

         '''wojewodztwo'''
         if 'woj' in plik and '.shp' in plik:
            woj = gpd.read_file(h)

         '''powiaty'''
         if 'pow' in plik and '.shp' in plik:
            pow = gpd.read_file(h)

         '''gminy'''
         if 'gmin' in plik and '.shp' in plik:
            gmin = gpd.read_file(h)

         '''jednostki'''
         if 'jedn' in plik and '.shp' in plik:
            jedn = gpd.read_file(h)

         '''obreby'''
         if 'obreb' in plik and '.shp' in plik:
            obreb = gpd.read_file(h)

      '''sprawdzenie czy geometria jest poprawna'''
      obreb = obreb[obreb['geometry'].is_valid]
      jedn = jedn[jedn['geometry'].is_valid]
      gmin = gmin[gmin['geometry'].is_valid]
      pow = pow[pow['geometry'].is_valid]
      woj = woj[woj['geometry'].is_valid]

      '''ustawienie ukladu wspolrzednych'''
      jedn.to_crs(epsg=2180, inplace=True)
      obreb.to_crs(epsg=2180, inplace=True)
      gmin.to_crs(epsg=2180, inplace=True)
      pow.to_crs(epsg=2180, inplace=True)
      woj.to_crs(epsg=2180, inplace=True)

      geo_df_woj=pd.concat([geo_df_woj, woj], ignore_index=True) 
      geo_df_pow=pd.concat([geo_df_pow, pow], ignore_index=True) 
      geo_df_gmin=pd.concat([geo_df_gmin, gmin], ignore_index=True)
      geo_df_obreb=pd.concat([geo_df_obreb, obreb], ignore_index=True)
      geo_df_jedn=pd.concat([geo_df_jedn, jedn], ignore_index=True)


   
   geo_df_woj.rename(columns = {'JPT_KOD_JE':'ID:ID'}, inplace = True)
   geo_df_woj['ID:ID']='geo.'+geo_df_woj['ID:ID']

   geo_df_pow.rename(columns = {'JPT_KOD_JE':'ID:ID'}, inplace = True)
   geo_df_pow['ID:ID']='geo.'+geo_df_pow['ID:ID']

   geo_df_gmin.rename(columns = {'JPT_KOD_JE':'ID:ID'}, inplace = True)
   geo_df_gmin['ID:ID']='geo.'+geo_df_gmin['ID:ID']

   geo_df_obreb.rename(columns = {'JPT_KOD_JE':'ID:ID'}, inplace = True)
   geo_df_obreb['ID:ID']='geo.'+geo_df_obreb['ID:ID']

   geo_df_jedn.rename(columns = {'JPT_KOD_JE':'ID:ID'}, inplace = True)
   geo_df_jedn['ID:ID']='geo.'+geo_df_jedn['ID:ID']

   # Inicjalizacja pustego DataFrame dla wyników
   result_df = gpd.GeoDataFrame()

    # Iteracja po poziomach administracyjnych
   k=0
   for i in [geo_df_jedn, geo_df_obreb, geo_df_gmin, geo_df_pow]:
        for j in [geo_df_obreb, geo_df_gmin, geo_df_pow, geo_df_woj][k:]:

            # Spatial Join
            spatial_join = gpd.sjoin(i, j, how='inner', op='intersects')
            result_df=pd.concat([result_df, spatial_join], ignore_index=True)
    
        k+=1

   result_df[':TYPE']='WEWNATRZ'
   result_df.rename(columns = {'ID:ID_left':':START_ID', 'ID:ID_right':':END_ID'}, inplace = True)
    # Zapis wyniku do pliku CSV
   result_df.to_csv('D:/inzynierka/wynik/rel_admin_zawiera.csv', index=False, columns=[':START_ID',':END_ID',':TYPE'])


   


      