from neo import Neo4jDB
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

def read_budynki(kod):
   path_budynek = f'C:\\Users\\weron\\Desktop\\studia\\GDS_neo4j\\dane\\{kod}_wfs_egib\\{kod}_budynki.shp'
   budynki = gpd.read_file(path_budynek)
   return budynki

def read_dzialki(kod):
   path_dzialka = f'C:\\Users\\weron\\Desktop\\studia\\GDS_neo4j\\dane\\{kod}_wfs_egib\\{kod}_dzialki.shp'
   dzialki = gpd.read_file(path_dzialka)
   return dzialki

def read_file(key='woj'):
   slownik = {'woj': 'A01_Granice_wojewodztw', 'pow': 'A02_Granice_powiatow', 'gmin': 'A03_Granice_gmin', 'jedn': 'A05_Granice_jednostek_ewidencyjnych', 'obreb': 'A06_Granice_obrebow_ewidencyjnych'}
   path = f'C:\\Users\\weron\\Desktop\\studia\\GDS_neo4j\\dane\\26_GraniceAdministracyjne\\{slownik[key]}.shp'
   return gpd.read_file(path)

if __name__=="__main__":
   '''wojewodztwo świętokrzyskie - {kod - nazwa}'''
   kody_powiatow = {2601: 'buski', 2602: 'jędrzejowski', 2603: 'kazimierski', 2604: 'Kielce', 
                    2661: 'kielecki', 2605: 'konecki', 2606: 'opatowski', 2607: 'ostowiecki',
                    2608: 'pińczowski', 2609: 'sandomierski', 2610: 'skarżyski', 2611: 'starachowicki',
                    2612: 'staszowski', 2613: 'włoszczowski'}
   
   # '''wojewodztwo'''
   # woj = read_file('woj')
   # woj = woj.to_wkt()
   # neo = Neo4jDB()
   # neo.insert_wojewodztwa(data=woj.to_dict('records'))
   # neo.close()

   # '''powiaty'''
   # pow = read_file('pow')
   # pow = pow.to_wkt()
   # neo = Neo4jDB()
   # neo.insert_powiaty(data=pow.to_dict('records'))
   # neo.close()

   # '''gminy'''
   # gmin = read_file('gmin')
   # gmin = gmin.to_wkt()
   # neo = Neo4jDB()
   # neo.insert_gminy(data=gmin.to_dict('records'))
   # neo.close()

   # '''jednostki'''
   # jedn = read_file('jedn')
   # jedn = jedn.to_wkt()
   # neo = Neo4jDB()
   # neo.insert_jednostki_ewidencyjne(data=jedn.to_dict('records'))
   # neo.close()

   # '''obreby'''
   # jedn = read_file('obreb')
   # jedn = jedn.to_wkt()
   # neo = Neo4jDB()
   # neo.insert_obreby_ewidencyjne(data=jedn.to_dict('records'))
   # neo.close()


   '''dzialka i budynek w tej petli sie dzieje'''
   for key in kody_powiatow.keys():
      '''wczytanie danych'''
      print('key:', key)
      budynki = read_budynki(key)
      dzialki = read_dzialki(key) 
      
      '''zamiana numpy nan na nulle pythonowe'''
      budynki = budynki.replace({np.nan: None})
      dzialki = dzialki.replace({np.nan: None})

      '''sprawdzenie na której działce znajduje się budynek i przypisanie tej informacji do tabeli'''
      budynki_dzialki_match = gpd.sjoin(budynki, dzialki, how="left", op="within")
      budynki_dzialki_match.dropna(subset=['ID_BUDYNKU', 'ID_DZIALKI'], inplace=True)

      '''zamiana geometrii na typ wkt'''
      # budynki = budynki.to_wkt()
      # dzialki = dzialki.to_wkt()
      
      '''połączenie do bazy'''
      neo = Neo4jDB()
      # neo.clear()
      '''zamiana data frame na słowniki'''
      # budynki = budynki.to_dict('records')
      # dzialki = dzialki.to_dict('records')
      budynki_dzialki_match = budynki_dzialki_match[['ID_BUDYNKU','ID_DZIALKI']]
      budynki_dzialki_match = budynki_dzialki_match.to_dict('records')

      '''dodane dzialek i budynkow do bazy'''
      # print('dodanie dzialek')
      # neo.insert_dzialki(data=dzialki)
      # print('dodanie budynkow')
      # neo.insert_budynki(data=budynki)
      # print('done inserting data')

      '''stworzenie relacji budynek -['IS_IN']-> dzialka'''
      tqdm(neo.match_dzialka_budynek(data=budynki_dzialki_match))

      neo.close()
   
