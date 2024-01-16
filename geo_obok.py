import pandas as pd
import geopandas as gpd
from tqdm import tqdm
import os


if __name__=="__main__":

   directory = 'D:\inzynierka\dane_admin'
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

   '''
   geo_df_woj.set_index('ID:ID', inplace=True)
   geo_df_pow.set_index('ID:ID', inplace=True)
   geo_df_gmin.set_index('ID:ID', inplace=True)
   geo_df_obreb.set_index('ID:ID', inplace=True)
   geo_df_jedn.set_index('ID:ID', inplace=True)
   '''
    # Iterujemy po oryginalnych DataFrame'ach, aby znaleźć sąsiadów
   for jednostka, prefix in zip([geo_df_woj, geo_df_pow, geo_df_gmin, geo_df_obreb, geo_df_jedn],['woj','pow','gmin','obreb','jedn']):
        # Załóżmy, że masz DataFrame o nazwie df zawierający kolumny 'id' i 'geometria'
        # Tworzenie GeoDataFrame z df
        gdf = gpd.GeoDataFrame(jednostka, geometry='geometry')

        # Tworzenie kopii DataFrame
        gdf_copy = gdf.copy()

        # Dodanie kolumny do oryginalnego DataFrame z informacją o sąsiedztwie
        gdf['sasiedztwo_id'] = gdf.apply(lambda row: gdf_copy[gdf_copy['geometry'].touches(row['geometry'])]['ID:ID'].tolist() if gdf_copy['geometry'].touches(row['geometry']).any() else None, axis=1)

        # Rozbijanie listy identyfikatorów sąsiedztwa na osobne wiersze
        gdf_exploded = gdf.explode('sasiedztwo_id')

        # Usuwanie wierszy z pustymi wartościami w kolumnie 'sasiedztwo_id'
        gdf_exploded = gdf_exploded.dropna(subset=['sasiedztwo_id'])

        gdf_exploded[':TYPE']='JEST_OBOK'
        # Wyświetlenie wyniku
                        
        gdf_exploded.rename(columns={"ID:ID": ":START_ID", "sasiedztwo_id": ":END_ID"}, inplace=True)
        gdf_exploded.to_csv(f'D:\\inzynierka\\wynik\\rel_geo_{prefix}_obok.csv', index=False, columns=[':START_ID',':END_ID', ':TYPE'])
        del gdf
        del gdf_exploded


      