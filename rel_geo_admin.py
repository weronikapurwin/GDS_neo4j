import pandas as pd
import geopandas as gpd
from tqdm import tqdm
import os


if __name__=="__main__":

   directory = 'dane_admin'
   geo_df = gpd.GeoDataFrame()

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

      geom_woj = [x.geom_type for x in woj.geometry]
      woj['type'] = geom_woj
      geom_pow = [x.geom_type for x in pow.geometry]
      pow['type'] = geom_pow
      geom_gmin = [x.geom_type for x in gmin.geometry]
      gmin['type'] = geom_gmin
      geom_jedn = [x.geom_type for x in jedn.geometry]
      jedn['type'] = geom_jedn
      geom_obreb = [x.geom_type for x in obreb.geometry]
      obreb['type'] = geom_obreb

      geo_df = pd.concat([geo_df, woj[['JPT_KOD_JE', 'geometry', 'type']]], ignore_index=True)
      geo_df = pd.concat([geo_df, pow[['JPT_KOD_JE', 'geometry', 'type']]], ignore_index=True)
      geo_df = pd.concat([geo_df, gmin[['JPT_KOD_JE', 'geometry', 'type']]], ignore_index=True)
      geo_df = pd.concat([geo_df, jedn[['JPT_KOD_JE', 'geometry', 'type']]], ignore_index=True)
      geo_df = pd.concat([geo_df, obreb[['JPT_KOD_JE', 'geometry', 'type']]], ignore_index=True)

   
   geo_df.rename(columns = {'JPT_KOD_JE':':START_ID'}, inplace = True)
   geo_df[':TYPE'] = 'HAS_GEOMETRY'
   geo_df.dropna(subset=':START_ID', inplace=True)
   geo_df[':END_ID']='geo.'+geo_df[':START_ID']

   geo_df.to_csv('wynik\\rel_geo_admin.csv', columns=[':START_ID', ':END_ID', ':TYPE'], index=False)


      