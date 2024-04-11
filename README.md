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

Cette procédure présente comment utiliser le code qui permet de prendre une photo d'une étiquette d'un device et de retranscrire au fortmat CSV les informations de celui-ci. Puis, il permet d'enregistrer le device défini dans le fcihier CSV sur le network server (NS) TTN.
Le NS utilisé ici, est un serveur TTS construit et fourni par Sylvain Montagny. Cependant, la requête utilisé pour enregistrer le device peut être utilisé sur un NS publique : TTN. 
Ce code ce construit en 2 grande partie qui seront présentées ci-dessous. La première et la prise d'une photo de l'étiquette à l'aide d'un smartphone et sa transcription au format CSV. La seconde est la récupération des informations dans le fichier CSV et l'enregistrement du device sur TTS sur à l'aide de l'api REST.

**PREREQUIS :** 
- Utilitaire pour executer du code python (minimum version 3.8) 
- Network Server TTS ou TTN 
- le smartphone et le pc éxecutant le code doivent être sur le même réseau internet
- installation de différents package (à voir dans le II)
- application ? 

## II. Partie photo et transcription au format CSV 
=> Présenter ce qui est utilisé pour lire les photos ? 

### a. Mise en place 
- application
- package à installer
- autres ?

### b. Fonctionnement 
- comment ça fonctionne (dans les grandes lignes) ?
- ....

## III. Partie envoi des données CSV sur TTN avec REST 
- explication brève du code
- présentation des éléments enregidtré sur le TTS
- autres ? 

## IV. Méthode d'utilisation 

- décrire la méthode pour enregistrer un devide 

