import fiona
import os

directory = 'dane'

for woj in os.listdir(directory):
	f = os.path.join(directory, woj)
	for kod in os.listdir(f):
		g = os.path.join(f, kod)
		for plik in os.listdir(g):
			h = os.path.join(g, plik)
			if not '.shp' in os.listdir(g):
				if 'dzial' in plik and '.gml' in plik:
					try:
						with fiona.open(h, 'r') as source:
							# Otwórz plik SHP do zapisu
							with fiona.open(g+'\\'+os.path.splitext(plik)[0]+'.shp', 'w', driver='ESRI Shapefile', schema=source.schema) as dest:
								for feature in source:
									dest.write(feature)
					except fiona.errors.UnsupportedGeometryTypeError as e:
							# Ignoruj błąd i kontynuuj przetwarzanie
						print(f"Ignorowanie błędu w  woj {woj} pliku {h}: {e}")
						continue
					except fiona.errors.DriverError as e:
					# Ignoruj błąd i kontynuuj przetwarzanie
						print(f"Ignorowanie błędu w woj {woj}  w pliku {h}: {e}")
						continue
			if not '.shp' in os.listdir(g):
				if 'budy' in plik and '.gml' in plik:
					try:
						with fiona.open(h, 'r') as source:
							# Otwórz plik SHP do zapisu
							with fiona.open(g+'\\'+os.path.splitext(plik)[0]+'.shp', 'w', driver='ESRI Shapefile', schema=source.schema) as dest:
								for feature in source:
									dest.write(feature)
					except fiona.errors.UnsupportedGeometryTypeError as e:
							# Ignoruj błąd i kontynuuj przetwarzanie
						print(f"Ignorowanie błędu w woj {woj}  w pliku {h}: {e}")
						continue
					except fiona.errors.DriverError as e:
						# Ignoruj błąd i kontynuuj przetwarzanie
						print(f"Ignorowanie błędu w woj {woj}  w pliku {h}: {e}")
						continue

        
	        


# # Ścieżka do pliku GML wejściowego
# input_gml = 'dane\\dolnoslaskie\\0201_wfs_egib\\0201_dzialki_egib_wfs_gml.gml'

# # Ścieżka do pliku SHP wyjściowego
# output_shp = 'dane\\dolnoslaskie\\0201_wfs_egib\\0201_dzialki.shp'

# # Otwórz plik GML
# with fiona.open(input_gml, 'r') as source:
#     # Otwórz plik SHP do zapisu
#     with fiona.open(output_shp, 'w', driver='ESRI Shapefile', schema=source.schema) as dest:
#         # Skopiuj obiekty z pliku GML do pliku SHP
#         for feature in source:
#             dest.write(feature)
