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
   geo_df5 = gpd.GeoDataFrame()

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
      obreb.dropna(subset=['JPT_KOD_JE'], inplace=True)
      obreb.rename(columns = {'JPT_KOD_JE':'ID:ID', 'JPT_NAZWA_':'NAME'}, inplace = True)
      obreb[':LABEL']='Obreb Ewidencyjny'
      geo_df1 = pd.concat([geo_df1, obreb], ignore_index=True)

      jedn.dropna(subset=['JPT_KOD_JE'], inplace=True)
      jedn.rename(columns = {'JPT_KOD_JE':'ID:ID', 'JPT_NAZWA_':'NAME'}, inplace = True)
      jedn[':LABEL']='Jednostka Ewidencyjna'
      geo_df2 = pd.concat([geo_df2, jedn], ignore_index=True)

      gmin.dropna(subset=['JPT_KOD_JE'], inplace=True)
      gmin.rename(columns = {'JPT_KOD_JE':'ID:ID', 'JPT_NAZWA_':'NAME'}, inplace = True)
      gmin[':LABEL']='Gmina'
      geo_df3 = pd.concat([geo_df3, gmin], ignore_index=True)

      pow.dropna(subset=['JPT_KOD_JE'], inplace=True)
      pow.rename(columns = {'JPT_KOD_JE':'ID:ID', 'JPT_NAZWA_':'NAME'}, inplace = True)
      pow[':LABEL']='Powiat'
      geo_df4 = pd.concat([geo_df4, pow], ignore_index=True)

      woj.dropna(subset=['JPT_KOD_JE'], inplace=True)
      woj.rename(columns = {'JPT_KOD_JE':'ID:ID', 'JPT_NAZWA_':'NAME'}, inplace = True)
      woj[':LABEL']='Wojewodztwo'
      geo_df5 = pd.concat([geo_df5, woj], ignore_index=True)

   '''zapis relacji do plikow csv'''   
   geo_df1.to_csv(f'wynik\\obreb.csv', columns=['ID:ID', 'NAME', ':LABEL'], index=False, encoding='UTF-8')
   geo_df2.to_csv(f'wynik\\jedn.csv', columns=['ID:ID', 'NAME', ':LABEL'], index=False, encoding='UTF-8')
   geo_df3.to_csv(f'wynik\\gmin.csv', columns=['ID:ID', 'NAME', ':LABEL'], index=False, encoding='UTF-8')
   geo_df4.to_csv(f'wynik\\pow.csv', columns=['ID:ID', 'NAME', ':LABEL'], index=False, encoding='UTF-8')
   geo_df5.to_csv(f'wynik\\woj.csv', columns=['ID:ID', 'NAME', ':LABEL'], index=False, encoding='UTF-8')