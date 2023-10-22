import geopandas as gpd
import pandas as pd
import os
from tqdm import tqdm


if __name__=="__main__":
   directory = 'dane_admin'

   '''tworze puste dataframe ktore beda sie uzupelnialy danymi do koncowego zapisu do csv'''
   geo_df1 = gpd.GeoDataFrame()
   geo_df2 = gpd.GeoDataFrame()
   geo_df3 = gpd.GeoDataFrame()
   geo_df4 = gpd.GeoDataFrame()

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

      '''operacje sprawdzajace ktory obreb jest w danej jednostce i przypisanie tych informacji do jednego dataframeu'''
      obreb_jedn = gpd.sjoin(obreb, jedn, how="left", op="within")
      obreb_jedn.dropna(subset=['JPT_KOD_JE_left', 'JPT_KOD_JE_right'], inplace=True)
      obreb_jedn = obreb_jedn[['JPT_KOD_JE_left', 'JPT_KOD_JE_right']]
      obreb_jedn.rename(columns = {'JPT_KOD_JE_left':':START_ID', 'JPT_KOD_JE_right':':END_ID'}, inplace = True)
      obreb_jedn[':TYPE']='IS_IN'
      geo_df1 = pd.concat([geo_df1, obreb_jedn], ignore_index=True)

      jedn_gmin = gpd.sjoin(jedn, gmin, how="left", op="within")
      jedn_gmin.dropna(subset=['JPT_KOD_JE_left', 'JPT_KOD_JE_right'], inplace=True)
      jedn_gmin = jedn_gmin[['JPT_KOD_JE_left', 'JPT_KOD_JE_right']]
      jedn_gmin.rename(columns = {'JPT_KOD_JE_left':':START_ID', 'JPT_KOD_JE_right':':END_ID'}, inplace = True)
      jedn_gmin[':TYPE']='IS_IN'
      geo_df2 = pd.concat([geo_df2, jedn_gmin], ignore_index=True)

      gmin_pow = gpd.sjoin(gmin, pow, how="left", op="within")
      gmin_pow.dropna(subset=['JPT_KOD_JE_left', 'JPT_KOD_JE_right'], inplace=True)
      gmin_pow = gmin_pow[['JPT_KOD_JE_left', 'JPT_KOD_JE_right']]
      gmin_pow.rename(columns = {'JPT_KOD_JE_left':':START_ID', 'JPT_KOD_JE_right':':END_ID'}, inplace = True)
      gmin_pow[':TYPE']='IS_IN'
      geo_df3 = pd.concat([geo_df3, gmin_pow], ignore_index=True)


      pow_woj = gpd.sjoin(pow, woj, how="left", op="within")
      pow_woj.dropna(subset=['JPT_KOD_JE_left', 'JPT_KOD_JE_right'], inplace=True)
      pow_woj = pow_woj[['JPT_KOD_JE_left', 'JPT_KOD_JE_right']]
      pow_woj.rename(columns = {'JPT_KOD_JE_left':':START_ID', 'JPT_KOD_JE_right':':END_ID'}, inplace = True)
      pow_woj[':TYPE']='IS_IN'
      geo_df4 = pd.concat([geo_df4, pow_woj], ignore_index=True)

   '''zapis relacji do plikow csv'''   
   geo_df1.to_csv(f'wynik\\rel_obreb_jedn.csv', index=False)
   geo_df2.to_csv(f'wynik\\rel_jedn_gmin.csv', index=False)
   geo_df3.to_csv(f'wynik\\rel_gmin_pow.csv', index=False)
   geo_df4.to_csv(f'wynik\\rel_pow_woj.csv', index=False)
