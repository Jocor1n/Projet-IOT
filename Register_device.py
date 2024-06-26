# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 09:10:37 2024

@author: user
"""

import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()  

join_eui = "0000000000000000"
dev_description = "device-description"
app_name = os.getenv('app_name')

auth_token = os.getenv('auth_token')

headers = {
    "Accept" : "application/json",
    "Authorization" : f"Bearer {auth_token}",
    "Accept" : "application/json"
    }

###########################################################
################## ENREGISTREMENT DEVICE ##################
###########################################################

def to_create_device(ip_serv, dev_name, dev_addr, device_id, dev_eui, join_eui, app_name, apps_key, nets_key):
    
    create_device = { # Dictionnaire contenant les informations nécessaires pour créer un device
       "end_device":{ # Dictionnaire imbriqué contenant les informations sur le device
          "name": f"{dev_name}",
          "description":f"{dev_description}",
          "ids":{
             "device_id":f"{device_id}",
             "dev_eui":f"{dev_eui}",
             "join_eui":f"{join_eui}",
             "device_address":f"{dev_addr}",
             "application_ids":{
                "application_id":"{app_name}"
             }
          },
          "lorawan_version":"1.0.3",
          "lorawan_phy_version":"1.0.3-a",
          "frequency_plan": "EU_863_870",
          "activation_mode": "OTAA", #ou ABP si on veut utiliser ABP
          "join_server_address": f"{ip_serv}",
          "network_server_address":f"{ip_serv}",
          "application_server_address":f"{ip_serv}",
            # "keys": {
            #    "apps_key": f"{apps_key}",
            #    "nwk_key": f"{nets_key}"
            # }, # Pas besoin de cette partie car OTAA et non ABP
          "version_ids":{ # Contient les informations relatives aux versions utilisée par le device
             "frequency_plan_id": "EU_863_870",
             "lorawan_version": "MAC_V1_0_3",
             "regional_parameters_version": "RP001_REV_A",
             "band_id": "EU_863_870"
          },
       },
       "field_mask": { # Spécifie quels champs de l'appareil doivent être mis à jour (via les une liste de chemin d'accès) dans les requêtes API et que les autres champs ne sont pas accidentellement modifiés.
          "paths": [
             "ids.device_id",
             "ids.dev_eui",
             "ids.join_eui",
             "ids.application_ids.application_id",
             "lorawan_version",
             "lorawan_phy_version",
             "activation_mode",
             "frequency_plan_id",
             "frequency_plan",
             "version_ids.frequency_plan_id",
             "version_ids.lorawan_version",
             "version_ids.regional_parameters_version","version_ids.band_id",
             # "keys.apps_key",
             # "keys.ntw_key", # Pas besoin de cette partie car OTAA et non ABP
             "join_server_address",
             "network_server_address",
             "application_server_address"
          ]
       }
    }
    return create_device

# Dictionnaire contenant les informations nécessaires pour enregistrer le device sur le name server.
  
def to_register_name_server(device_id, dev_addr, dev_eui, join_eui, app_name):

    register_name_server = { # Dictionnaire imbriqué contenant les informations sur le device
        "end_device": {
          "supports_join": True, # Indique que le device est en mesure d'effectuer une procédure de join, il supporte le mode OTAA.
          "lorawan_version": "MAC_V1_0_3",
          "ids": {
              "device_id": f"{device_id}",
              "dev_eui": f"{dev_eui}",
              "join_eui": f"{join_eui}",
              "device_address": f"{dev_addr}",
              "application_ids": {
                "application_id": f"{app_name}"
              }
          },
          "frequency_plan_id": "EU_863_870_TTN",
          "version_ids": { # Contient les informations relatives aux versions utilisée par le device (ici la bande fréquence fréquence utilisée)
              "band_id": "EU_863_870"
          },
          "lorawan_phy_version": "PHY_V1_0_3_REV_A",
          "mac_settings": {
              # "class_c_timeout": "60s", # A adapter si on utilise un device de classe B ou C. Le device adoptera, par défaut, un comportement de classe A.
              "supports_32_bit_f_cnt": True # Indique que le device prend en charge l'utilisation de compteurs de trames 32 bits (2 types : 16 bits et 32 bits). Ces compteurs permettent de détecter si des trames ont été perdues ou dupliquées pendant la transmission. Utile lors de l'échange de nombreuses trames. /!\ TOUS les périphériques LoRaWAN NE PRENNENT PAS en charge les compteurs de trames 32 bits.
          }
        },
        "field_mask": { # Spécifie quels champs de l'appareil doivent être mis à jour (via les une liste de chemin d'accès) dans les requêtes API et que les autres champs ne sont pas accidentellement modifiés.
          "paths": [
              "supports_join",
              "lorawan_version",
              "ids.device_id",
              "ids.dev_eui",
              "ids.join_eui",
              "ids.application_ids.application_id",
              "frequency_plan_id",
              "version_ids.band_id",
              "lorawan_phy_version",
              # "mac_settings.class_c_timeout",
              "mac_settings.supports_32_bit_f_cnt"
          ]
        }
    }
    return register_name_server

def to_register_app_server(device_id, dev_addr, dev_eui, join_eui, app_name):

# Dictionnaire contenant les informations nécessaires pour enregistrer notre device sur l'application server
    register_application_server = {
       "end_device": { # Dictionnaire imbriqué contenant les informations sur le device
       "ids": {
          "device_id": f"{device_id}",
           "dev_eui": f"{dev_eui}",
          "join_eui": f"{join_eui}",
          "device_address": f"{dev_addr}",
          "application_ids": {
             "application_id": f"{app_name}"
          }
          #"keys": {
          #   "apps_key": f"{apps_key}",
          #   "nwk_key": f"{nets_key}"
          #} #pas besoin de cette partie car OTAA et non requis pour l'enregistrement d'un appareil auprès d'un serveur d'application
          },
          "application_server_address":"FORMATTER_REPOSITORY"
        },
        "field_mask": { # Spécifie quels champs de l'appareil doivent être mis à jour (via les une liste de chemin d'accès) dans les requêtes API et que les autres champs ne sont pas accidentellement modifiés.
          "paths": [
             "ids.device_id",
             "ids.dev_eui",
             "ids.join_eui",
             "ids.application_ids.application_id"
             # "application_server_address"
          ]
       }
    }
    return register_application_server

# Dictionnaire contenant les informations nécessaires pour enregistrer notre device sur le server de join (network server)
def to_register_join_server(device_id, dev_eui, join_eui, app_name, ip_serv, app_key):
    
    register_join_server = {
        "end_device": { # Dictionnaire imbriqué contenant les informations sur le device
          "ids": {
              "device_id": f"{device_id}",
              "dev_eui": f"{dev_eui}",
              "join_eui": f"{join_eui}",
              "application_ids": {
                "application_id": f"{app_name}"
              }
          },
          "network_server_address": f"{ip_serv}",
          "application_server_address": f"{ip_serv}",
          "root_keys": { # Contient la clé racine du device (application key)
              "app_key": {
                  "key": f"{app_key}"
              }
          }
        },
        "field_mask": { # Spécifie quels champs de l'appareil doivent être mis à jour (via les une liste de chemin d'accès) dans les requêtes API et que les autres champs ne sont pas accidentellement modifiés.
          "paths": [
              "network_server_address",
              "application_server_address",
              "root_keys.app_key.key",
              "ids.device_id",
              "ids.dev_eui",
              "ids.join_eui",
              "ids.application_ids.application_id"
          ]
        }
    }
    return register_join_server

##################################################
################## REQUÊTES API ##################
##################################################

def add_device_to_TTN(ip_serv, dev_addr, dev_eui, apps_key, nets_key, app_key):
    
    dev_name = f"{app_name}-{dev_addr}"
    device_id = f"{dev_addr.lower()}"
    
    create_device = to_create_device(ip_serv, dev_name, dev_addr, device_id, dev_eui, join_eui, app_name, apps_key, nets_key)
    register_name_server = to_register_name_server(device_id, dev_addr, dev_eui, join_eui, app_name)
    register_application_server = to_register_app_server(device_id, dev_addr, dev_eui, join_eui, app_name)
    register_join_server = to_register_join_server(device_id, dev_eui, join_eui, app_name, ip_serv, app_key)
    
    api_url=f"http://{ip_serv}/api/v3/applications/{app_name}/devices"
    
    response2 = requests.get(api_url, headers=headers)
    
    def add_to_TTN():
        # Requête POST pour créer un device en prenant en paramètres le dictionnaire 
        response = requests.post(f"http://{ip_serv}/api/v3/applications/{app_name}/devices", data=json.dumps(create_device), headers=headers)
        print("RESPONSE DEVICE CREATE")
        print(response.text)
        
        # Requête PUT pour enregistrer le device sur le name server
        response = requests.put(f"http://{ip_serv}/api/v3/ns/applications/{app_name}/devices/{device_id}", data=json.dumps(register_name_server), headers=headers)
        print("REGISTER NAME SERVER")
        print(response.text)
        
        # Requête PUT pour enregistrer le device sur l'application server
        response = requests.put(f"http://{ip_serv}/api/v3/as/applications/{app_name}/devices/{device_id}", data=json.dumps(register_application_server), headers=headers)
        print("REGISTER APPLICATION SERVER")
        print(response.text)
        
        # Requête PUT pour enregistrer le device sur le network server
        response = requests.put(f"http://{ip_serv}/api/v3/js/applications/{app_name}/devices/{device_id}", data=json.dumps(register_join_server), headers=headers)
        print("REGISTER JOIN SERVER")
        print(response.text)
    
    # Vérifie si la réponse a été réussie.
    if response2.status_code == 200:
        device_info = response2.json()
    
        # Vérifie si la clé 'end_devices' est présente dans la réponse.
        if 'end_devices' in device_info:
            device_ids = [device['ids']['device_id'] for device in device_info['end_devices']]
    
            if device_id in device_ids:
                print(f"The device ID : {dev_addr.lower()} already exists.")
            else: 
               add_to_TTN()
        else:
           # Signifie qu'il n'y a aucun device de créé
           add_to_TTN()
    else:
        print("Failed to retrieve device information. Status code:", response2.status_code)
        

# Requête GET pour avoir la liste des devices d'une appli dans un csv
def get_devices_TTN(ip_serv, app_name,):
    api_url=f"http://{ip_serv}/api/v3/applications/{app_name}/devices"
    response = requests.get(api_url, headers=headers)
    return response.json()
