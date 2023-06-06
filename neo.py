from neo4j import GraphDatabase
from py2neo import Graph
from py2neo.bulk import create_nodes, create_relationships
from tqdm import tqdm
import numpy as np

def query(method):
    def wrapper(*args, **kwargs):
        self = args[0]
        with self.driver.session() as session:
            session.execute_write(lambda tx: method(self, tx, **kwargs))
    return wrapper

class Neo4jDB:
    def __init__(self, uri='bolt://localhost:7687', username="neo4j", password="password"):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        self.driver_py2neo = Graph(uri, auth=(username, password))
        # self.tx = Graph.begin()
        self.driver.verify_connectivity()

    def close(self):
        self.driver.close()
    
    def clear(self):
        return self.driver_py2neo.delete_all()

    def insert_budynki(self, data):
        data_neo = []
        for temp in tqdm(data):
            node = ({"id": temp['ID_BUDYNKU'], "geometry": temp['geometry'], "rodzaj": temp['RODZAJ']})
            data_neo.append(node)
            if(len(data_neo) == 10000):
                create_nodes(self.driver_py2neo.auto(), data_neo, labels={"Budynek"})
                data_neo = []
        create_nodes(self.driver_py2neo.auto(), data_neo, labels={"Budynek"})

    def insert_dzialki(self, data):
        data_neo = []
        for temp in tqdm(data):
            node = ({"id": temp['ID_DZIALKI'], "geometry": temp['geometry'], "nr_dzialki": temp['NUMER_DZIA'], "nr_obrebu": temp['NUMER_OBRE'], "nr_jednostki": temp['NUMER_JEDN'], "obreb": temp['NAZWA_OBRE'], "gmina": temp['NAZWA_GMIN']})
            data_neo.append(node)
            if(len(data_neo) == 10000):
                create_nodes(self.driver_py2neo.auto(), data_neo, labels={"Dzialka"})
                data_neo = []
        create_nodes(self.driver_py2neo.auto(), data_neo, labels={"Dzialka"})

    def insert_jednostki_ewidencyjne(self, data):
        data_neo = []
        for temp in tqdm(data):
            node = ({"id": temp['JPT_KOD_JE'], "geometry": temp['geometry'], "nazwa": temp['JPT_NAZWA_']})
            data_neo.append(node)
            if(len(data_neo) == 10000):
                create_nodes(self.driver_py2neo.auto(), data_neo, labels={"Jednostka_Ewidencyjna"})
                data_neo = []
        create_nodes(self.driver_py2neo.auto(), data_neo, labels={"Jednostka_Ewidencyjna"})

    def insert_obreby_ewidencyjne(self, data):
        data_neo = []
        for temp in tqdm(data):
            node = ({"id": temp['JPT_KOD_JE'], "geometry": temp['geometry'], "nazwa": temp['JPT_NAZWA_']})
            data_neo.append(node)
            if(len(data_neo) == 10000):
                create_nodes(self.driver_py2neo.auto(), data_neo, labels={"Obreb_Ewidencyjny"})
                data_neo = []
        create_nodes(self.driver_py2neo.auto(), data_neo, labels={"Obreb_Ewidencyjny"})

    def insert_gminy(self, data):
        data_neo = []
        for temp in tqdm(data):
            node = ({"id": temp['JPT_KOD_JE'], "geometry": temp['geometry'], "nazwa": temp['JPT_NAZWA_'], "regon": temp['REGON']})
            data_neo.append(node)
            if(len(data_neo) == 10000):
                create_nodes(self.driver_py2neo.auto(), data_neo, labels={"Gmina"})
                data_neo = []
        create_nodes(self.driver_py2neo.auto(), data_neo, labels={"Gmina"})

    def insert_powiaty(self, data):
        data_neo = []
        for temp in tqdm(data):
            node = ({"id": temp['JPT_KOD_JE'], "geometry": temp['geometry'], "nazwa": temp['JPT_NAZWA_'], "regon": temp['REGON']})
            data_neo.append(node)
            if(len(data_neo) == 10000):
                create_nodes(self.driver_py2neo.auto(), data_neo, labels={"Powiat"})
                data_neo = []
        create_nodes(self.driver_py2neo.auto(), data_neo, labels={"Powiat"})

    def insert_wojewodztwa(self, data):
        data_neo = []
        for temp in tqdm(data):
            node = ({"id": temp['JPT_KOD_JE'], "geometry": temp['geometry'], "nazwa": temp['JPT_NAZWA_'], "regon": temp['REGON']})
            data_neo.append(node)
            if(len(data_neo) == 10000):
                create_nodes(self.driver_py2neo.auto(), data_neo, labels={"Wojewodztwo"})
                data_neo = []
        create_nodes(self.driver_py2neo.auto(), data_neo, labels={"Wojewodztwo"})

    @query
    def match_dzialka_budynek(self, tx, data):
        for temp in tqdm(data):
            tx.run("""MATCH (b:Budynek {id: $c1}), (d:Dzialka {id: $c2})
            MERGE (b)-[:IS_IN]->(d)""", 
            c1=temp['ID_BUDYNKU'], c2=temp['ID_DZIALKI'])

    '''to działa wolno :c a byłam z tego taka dumna'''
    # def match_dzialka_budynek(self, data):
    #     data_neo = []
    #     for temp in tqdm(data):
    #         budynek = temp['ID_BUDYNKU']
    #         dzialka = temp['ID_DZIALKI']
    #         if budynek and dzialka:
    #             data_neo.append((budynek, {}, dzialka))
    #         if(len(data_neo) == 100):
    #             create_relationships(self.driver_py2neo.auto(), data=data_neo, rel_type="IS_IN", start_node_key=("Budynek", "id"), end_node_key=("Dzialka", "id"))
    #             data_neo=[]
    #     create_relationships(self.driver_py2neo.auto(), data=data_neo, rel_type="IS_IN", start_node_key=("Budynek", "id"), end_node_key=("Dzialka", "id"))

  
            

        

 