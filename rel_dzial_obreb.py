import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import os

if __name__=="__main__":
   
   directory_dzial = 'dane'
   directory_obreb='dane_admin'

   # relation = pd.DataFrame()


   for i in range(0,16,2):

      relation = pd.DataFrame()


      for wojew, wojew1 in tqdm(zip(os.listdir(directory_dzial)[i:i+2],os.listdir(directory_obreb)[i:i+2])):
        dzialki_final = gpd.GeoDataFrame()
        dz = os.path.join(directory_dzial, wojew)
        ob = os.path.join(directory_obreb, wojew1)


        for plik1 in tqdm(os.listdir(ob)):

            obre = os.path.join(ob, plik1)

            '''obreby'''
            if 'obreb' in plik1 and '.shp' in plik1:

                obreb = gpd.read_file(obre)
                obreb = obreb[obreb['geometry'].is_valid]
                obreb.to_crs(epsg=2180, inplace=True)

                for kod in (os.listdir(dz)):
                    dzia = os.path.join(dz, kod)

                    for plik in os.listdir(dzia):
                        h = os.path.join(dzia, plik)

                        if 'dzial' in plik and '.shp' in plik:
                            print(obre,'\n', h)
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
                        dzialki_final = pd.concat([dzialki_final, dzialki], ignore_index=True)
                    else:
                        continue


                    if 'ID_DZIALKI' in dzialki.columns:
                        dzialki_final = pd.concat([dzialki_final, dzialki], ignore_index=True)
                    else:
                        continue


            else:
                continue
        
        dzialka_obreb = gpd.sjoin(dzialki_final, obreb, how="left", op="intersects")
        dzialka_obreb.dropna(subset=['ID_DZIALKI', 'JPT_KOD_JE'], inplace=True)
        dzialka_obreb = dzialka_obreb[['ID_DZIALKI', 'JPT_KOD_JE']]
        relation = pd.concat([relation, dzialka_obreb], ignore_index=True)

        del dzialki_final
        del dzialki




      print('lolo')

      relation[':TYPE']='IS_IN'
      relation.rename(columns = {'ID_DZIALKI':':START_ID', 'JPT_KOD_JE':':END_ID'}, inplace = True)
      relation.drop_duplicates(subset=[':START_ID', ':END_ID'], inplace=True)

      relation.to_csv(f'wynik\\rel_dzia_obreb{i}.csv', index=False)

      del relation