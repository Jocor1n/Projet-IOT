| Titre           | Procédure d'utilisation d'enregistrement d'un device sur TTN    |
| ----------------|---------------------------------------------------------------- |
| Modifications   | 11/04/2024                                                      |
| Auteurs         | Jocelyn Corbel, Joseph Nguyen, Floriane Quéré, Candice Flammier |

# Sommaire

- [I. Présentation](#i-1)
- [II. Partie d'appel API avec REST](#ii-2)
- [III. Partie Photo et transcription au format CSV](#iii-3)
- [IV. Méthode d'utilisation](#iv-4)


## I. Présentation 

Cette procédure présente comment utiliser le code qui permet de prendre une photo d'une étiquette d'un device et de retranscrire au fortmat CSV les informations de celui-ci. Puis, il permet d'enregistrer le device défini dans le fichier CSV sur le network server (NS) TTN.
Le NS utilisé ici, est un serveur TTS construit et fourni par Sylvain Montagny. Cependant, la requête utilisé pour enregistrer le device peut être utilisé sur un NS publique : TTN. 
Ce code ce construit en 2 grande partie qui seront présentées ci-dessous. La première est la prise d'une photo de l'étiquette à l'aide d'un smartphone et sa transcription au format CSV. La seconde est la récupération des informations dans le fichier CSV et l'enregistrement du device sur TTS sur à l'aide de l'api REST.

**PREREQUIS :** 
- Utilitaire pour executer du code python (minimum version 3.8) 
- Network Server TTS ou TTN 
- le smartphone et le pc éxecutant le code doivent être sur le même réseau internet
- installation de différents package (à voir dans le II)
- Un compte Azure
- Git d'installé
- Installation de l'application IP Webcam
  
## II. Partie photo et transcription au format CSV 

#### Création de l'environnement virtuel :
- Ouvrez votre terminal.
Placez-vous dans le répertoire de votre projet où vous souhaitez créer l'environnement virtuel.

Utilisez la commande suivante pour créer l'environnement virtuel :
```shell
python -m venv <nom_de_l'environnement>
```
Remplacez <nom_de_l'environnement> par le nom que vous souhaitez donner à votre environnement virtuel. Par exemple, vous pouvez utiliser env comme nom d'environnement.

Une fois la commande exécutée, un nouveau répertoire sera créé dans votre projet avec le nom de l'environnement virtuel que vous avez spécifié.

Pour activer l'environnement virtuel, utilisez la commande appropriée en fonction de votre système d'exploitation :

Sur Windows :
```shell
<nom_de_l'environnement>\Scripts\activate
```
Sur macOS et Linux :
```shell
source <nom_de_l'environnement>/bin/activate
```
Ensuite vous pouvez télécharger et installer les dépendances requises, exécutez la commande suivante dans votre terminal :

```shell
pip install -r requirements.txt
```
#### Clone du projet Git

Vous pouvez cloner le projet Git en utilisant la commande :

```shell
git init
git clone https://github.com/Jocor1n/Projet-IOT.git 
```

Ou avec SSH :

```shell
git init
git clone git@github.com:Jocor1n/Projet-IOT.git
```

#### Application :
Il faut que votre ordinateur et votre téléphone soit sur le même réseau Internet, si ce n'est pas le cas, mettez votre ordinateur en point d'accès sans fil mobile et connecter votre téléphone sur ce même réseau.
Sur votre téléphone, installer l'application IP Webcam.
Une fois lancée, cliquer sur démarrer le serveur, récupérer l'IP et le port utilisé pour plus tard.

#### Azure : 

Connectez-vous sur votre compte Azure. Dans la barre de recherche, recherchez : Vision par ordinateur. Une fois sélectionnée, créer une vision par ordinateur. Remplissez tout d'abord, les détails du projet en choisissant un abonnement et un groupe de ressources. Puis choisir les détails de l'instance avec une région et un nom. Pour le niveau tarifaire, dans notre cas, on va utiliser la version gratuite où vous pouvez faire 20 appels par minute et 5 mille appels par mois avec cette API. Ce qui est grandement suffisant. 
Vous devriez avoir apparaître la région et surtout la clé API, nécessaire au fonctionnement de notre code. Comme ceci :

![image](https://github.com/Jocor1n/Projet-IOT/assets/75179590/183065f5-2254-4f83-8958-85cd0c1bc6a9)

En savoir plus sur les conditions générales d'utilisation d'Azure AI Vision : https://azure.microsoft.com/fr-fr/products/ai-services/ai-vision

#### Créer un fichier .env et rajouter ces variables :
```shell
API_KEY=VOTRE_API_KEY
auth_token=VOTRE_AUTH_TOKEN_TTN
ip_serv_TTN =IP_SERVEUR_TTN
ip_serv_webcam=IP_WEBCAM_TELEPHONE:PORT
image_directory=REPERTOIRE_POUR_ENREGISTRER_LES_IMAGES
csv_file_path=REPERTOIRE_FICHIER_CSV
devices_csv_file_path=REPERTOIRE_FICHIER_DEVICE_CSV
app_name=NOM_APPLICATION_TTN
```

## III. Partie envoi des données CSV sur TTN avec REST 

**Documentation sur les [API TTN](https://www.thethingsindustries.com/docs/api/):**
- Utilisation des requêtes REST POST et PUT pour envoyer les données CSV vers TTN :
  - [POST Create device](https://www.thethingsindustries.com/docs/api/reference/http/routes/#applications{end_device.ids.application_ids.application_id}devices-post)
  - [PUT Register device into NS, AS, Name Server](https://www.thethingsindustries.com/docs/api/reference/http/routes/#applications{end_device.ids.application_ids.application_id}devices{end_device.ids.device_id}-put)
- Utilisation des requêtes REST GET pour récupérer les données de TTN :
  - [GET devices](https://www.thethingsindustries.com/docs/api/reference/http/routes/#applications{application_ids.application_id}devices-get)

Le fichier Register_device.py permet d'enregistrer un device LoraWAN sur un Network Server en utilisant l'API TTN (The Things Network).  Il comprend des fonctions pour créer l'appareil, l'enregistrer sur le name server, l'application server et le serveur de join (network server).
L'enregistrement du device sur le name server est une étape importante du processus d'enregistrement d'appareils sur TTN. Il permet au network server (join server) et à l'application server d'identifier le device et de communiquer avec lui.
Le script comprend également une fonction pour ajouter le périphérique à TTN, qui vérifie si le périphérique existe déjà et le crée si ce n'est pas le cas.

Ce script utilise la bibliothèque requests pour effectuer des requêtes HTTP à l'API TTN et la bibliothèque json pour sérialiser les données. Il utilise également des variables d'environnement pour stocker des informations sensibles telles que le nom de l'application, le jeton d'authentification et diverses clés.

Il définit plusieurs fonctions pour créer des dictionnaires contenant les informations nécessaires à l'enregistrement de l'appareil sur le réseau TTN. Ces dictionnaires sont ensuite utilisés comme données pour les requêtes HTTP.
La fonction add_device_to_TTN est la fonction principale qui relie le tout. Elle prend plusieurs paramètres tels que l'adresse IP du serveur, l'adresse de l'appareil, l'EUI de l'appareil et diverses clés. Elle crée ensuite les dictionnaires nécessaires et effectue les requêtes HTTP pour enregistrer l'appareil sur le réseau TTN.

Enfin, le script inclut également une gestion des erreurs pour vérifier si l'appareil existe déjà et pour imprimer la réponse des requêtes API.

**Éléments enregitrés sur le TTS pour OTAA et/ou ABP via CSV :**
  
* DevEUI : il s'agit d'un identifiant qui rend chaque objet normalement programmé en usine unique. Il n'est pas possible de modifier ce paramètre théoriquement
* AppKey : il s'agit d'un secret partagé entre le périphérique et le réseau, qui sert à dériver les clés de session. Ce paramètre est sujet à modification.
* DevAddr (Device Address) : une adresse logique de 32 bits utilisée pour repérer l'objet dans le réseau, présente dans chaque trame.
* NetSKey (Network Session Key) : clé de chiffrement AES-128 partagée entre l’objet et le serveur de l'opérateur,
* AppSKey (Application Session Key) : clé de chiffrement AES-128 partagée entre l’objet et l'utilisateur (via l'application).
* APP EUI : Identifiant d'application global dans l'espace d'adressage IEEE EUI64 qui identifie le serveur de jointure lors de l'activation par voie hertzienne.

## IV. Méthode d'utilisation 

- Pour enregistrer un device, il faut avoir l'application IP Webcam d'ouvert avec le serveur démarré. Une fois démarré, vous pouvez exécuter le programme principal sur l'environnement virtuel :
  
```shell
Image_recognition_csv.py
```

Ensuite 3 commandes sont disponibles : 

* ALT + s : Enregistrer un device en ayant la photo en temps réel sur le téléphone.
![téléchargement](https://github.com/Jocor1n/Projet-IOT/assets/75179590/80d47099-0fad-465f-88b7-c6243cabfc37)
* ALT + r : Lire le fichier csv
Exemple :
```shell
Device ID: 0182XXXX
Device EUI: A840XXXXXXXXXXXX
Application EUI: 8000XXXXXXXXXXXX
Application Key: 6D18XXXXXXXXXXXXXXXXXXXXXXXXXXXX
Network Session Key 563DXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Application Session Key 8616XXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
* ALT + a : Envoyer les données du fichier csv sur TTS, une gestion des duplicatas est activée
* ALT + v : Synchroniser toutes les images du répertoire des images
* ALT + g : Enregistrer les devices d'une application dans un csv
