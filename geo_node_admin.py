import pandas as pd
import geopandas as gpd
from tqdm import tqdm
import os


if __name__=="__main__":

   directory = 'dane_admin'
   geo_df = gpd.GeoDataFrame()
   dfrel=gpd.GeoDataFrame()

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

   
   geo_df .rename(columns = {'JPT_KOD_JE':'ID:ID'}, inplace = True)
   geo_df['format'] = 'WKT'
   geo_df[':LABEL'] = 'Geometry'
   geo_df.dropna(subset='ID:ID', inplace=True)
   geo_df['ID:ID']='geo.'+geo_df['ID:ID']

   geo_df.to_csv('wynik\\geo_admin.csv', index=False)

   #  for key in kody_powiatow.keys():
   #    '''wczytanie danych'''
   #    print('key:', key)
   #    budynki = read_budynki(key)
   #    dzialki = read_dzialki(key) 
      
   #    '''zamiana numpy nan na nulle pythonowe'''
   #    budynki = budynki.replace({np.nan: None})
   #    dzialki = dzialki.replace({np.nan: None})

   #    # Remove rows with invalid geometries
   #    budynki = budynki[budynki['geometry'].is_valid]
   #    dzialki = dzialki[dzialki['geometry'].is_valid]

   #    geom_bud = [x.geom_type for x in budynki.geometry]
   #    budynki['type'] = geom_bud
   #    geom_dz = [x.geom_type for x in dzialki.geometry]
   #    dzialki['type'] = geom_dz

   #    budynki.rename(columns = {'ID_BUDYNKU':'JPT_KOD_JE'}, inplace = True)
   #    dzialki.rename(columns = {'ID_DZIALKI':'JPT_KOD_JE'}, inplace = True)

   #    if budynki['JPT_KOD_JE'].isnull().any():
   #       print(key,'Budynki tu są puste w tym pliku')
   #    if dzialki['JPT_KOD_JE'].isnull().any():
   #       print(key,'dzialki tu są puste w tym pliku')

   #    geo_df = pd.concat([geo_df, budynki[[ 'JPT_KOD_JE', 'geometry', 'type']]], ignore_index=True)
   #    geo_df = pd.concat([geo_df, dzialki[[ 'JPT_KOD_JE', 'geometry', 'type']]], ignore_index=True)
      

   #  geo_df['format'] = 'WKT'
   #  geo_df['LABEL'] = 'Geometry'
   #  geo_df.dropna(subset='JPT_KOD_JE', inplace=True)
   #  geo_df['temp']='geo_'+geo_df.index.astype(str)
   #  print(geo_df.columns)
   #  # geo_df.set_geometry("geometry")
   #  # geom_types = [x.geom_type for x in geo_df.geometry]
   #  # geo_df['type'] = geom_types
   #  rel = geo_df[['JPT_KOD_JE', 'temp']]
   #  rel[':TYPE'] = 'HAS_GEOMETRY'
    
   #  rel.to_csv('syf\\relations.csv', index=False)
   
   #  geo_df.to_csv('syf\\geo.csv', index=False)
   #  print(geo_df[0:2])

      