import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import os

if __name__=="__main__":
   
   directory = 'dane'

   '''dzialka i budynek w tej petli sie dzieje'''

   rodzaje = {
      'm':'mieszkalny',
      'g':'produkcyjnyUslugowyIGospodarczy',
      't':'transportuILacznosci',
      'k':'oswiatyNaukiIKulturyOrazSport',
      'z':'szpitalaIInneBudynkiOpiekiZdrowotnej',
      'b':'biurowy',
      'h':'handlowoUslugowy',
      'p':'przemyslowy',
      's':'zbiornikSilosIBudynekMagazynowy',
      'i':'budynekNiemieszkalny'}
   

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
                    budynki_final = pd.concat([budynki_final, budynki], ignore_index=True)
                else:
                   del budynki
                   

            else:
                if 'ID_BUDYNKU' in budynki.columns:
                    budynki_final = pd.concat([budynki_final, budynki], ignore_index=True)
                else:
                   del budynki

      print('lolo')

      budynki_final[':LABEL']='Budynek'
      budynki_final.rename(columns = {'ID_BUDYNKU':'ID_BUDYNKU:ID'}, inplace = True)
      '''zamiana wartosci rodzaju na pelna nazwe'''
      budynki_final.replace({"RODZAJ": rodzaje},inplace=True)
      '''usuniecie rekordow bez id'''
      budynki_final.dropna(subset=['ID_BUDYNKU:ID'], inplace=True)
      budynki_final.drop_duplicates(subset=['ID_BUDYNKU:ID'], inplace=True)

      budynki_final.to_csv(f'wynik\\budynki{i}.csv', columns=['ID_BUDYNKU:ID', 'RODZAJ', ':LABEL'], index=False)

      del budynki_final


   
