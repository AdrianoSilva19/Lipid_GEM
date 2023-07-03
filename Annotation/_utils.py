from typing import List,Dict
import re
from cobra import Model,Metabolite
from neo4j import GraphDatabase

from database_access_manager import DatabaseAccessManager



def set_metabolite_annotation_in_model(session:GraphDatabase.driver,dictionary_results:Dict,model:Model)->Model:
    """Function to anotate lipid metabolites in a user chossen model

    :param session: driver linkage to database
    :type session: GraphDatabase.driver
    :param dictionary_results: Python Dictionary with Lipid metabolites IDs from the BOIMMG the database
    :type dictionary_results: Dict
    :param model: GSM model to be annotated
    :type model: Model
    :return: Gsm model with defined Lipids annotated
    :rtype: Model
    """
    for metabolite_ids,boimmg_ids in dictionary_results.items():
        lipid_maps_ids=[]
        swiss_lipids_ids=[]
        for boimmg_id in boimmg_ids:
            result=session.run("match(c:Compound)where id(c)=$boimmg_id return c.lipidmaps_id,c.swiss_lipids_id as ids", boimmg_id=boimmg_id)
            data= result.data()
            for node in data:
                node_lipid_maps_id = node.get("c.lipidmaps_id")
                if node_lipid_maps_id != None:
                    lipid_maps_ids.append(node_lipid_maps_id)
                
                node_swiss_lipids_id = node.get("ids")
                if node_swiss_lipids_id!= None:
                    swiss_lipids_ids.append(node_swiss_lipids_id)
        
        for metabolite in model.metabolites:
            if metabolite.id == metabolite_ids:    
                if len(lipid_maps_ids) != 0:
                    for values in lipid_maps_ids:
                        metabolite.annotation["lipidmaps"] = values
                if len(swiss_lipids_ids) != 0:
                    for values in swiss_lipids_ids:  
                        metabolite.annotation["slm"] = values 

    return model

def transform_boimmg_id_in_annotation_id(dictionary_results:Dict)->Dict:
    driver = DatabaseAccessManager(conf_file_path="my_database.conf").connect()
    session = driver.session()
    annotation_dict = {}
    for metabolite_ids,boimmg_ids in dictionary_results.items():
        lipid_maps_ids=[]
        swiss_lipids_ids=[]
        for boimmg_id in boimmg_ids:
            result=session.run("match(c:Compound)where id(c)=$boimmg_id return c.lipidmaps_id,c.swiss_lipids_id as ids", boimmg_id=boimmg_id)
            data= result.data()
            for node in data:
                node_lipid_maps_id = node.get("c.lipidmaps_id")
                if node_lipid_maps_id != None:
                    lipid_maps_ids.append(node_lipid_maps_id)
                
                node_swiss_lipids_id = node.get("ids")
                if node_swiss_lipids_id!= None:
                    swiss_lipids_ids.append(node_swiss_lipids_id)
        annotation_dict[metabolite_ids]=[lipid_maps_ids,swiss_lipids_ids]
    return annotation_dict