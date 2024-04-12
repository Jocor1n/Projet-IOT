import cv2
import keyboard
import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
import time
import csv
import re
import original
import datetime

from dotenv import load_dotenv

load_dotenv()  

#Region et API Azure
region = 'westeurope'
key = os.getenv('API_KEY')
ip_serv = os.getenv('ip_serv_TTN')
ip_serv_webcam = os.getenv('ip_serv_webcam')

#Identifiants API Azure
credentials = CognitiveServicesCredentials(key)
client = ComputerVisionClient(
    endpoint="https://" + region + ".api.cognitive.microsoft.com/",
    credentials=credentials
)

# Adresse IP de la webcam
url = f"http://{ip_serv_webcam}/video"

# Capture vidéo
cap = cv2.VideoCapture(url)

# Répertoire d'installation pour enregistrer les images et le fichier csv
installation_directory = os.getenv('image_directory')
csv_file_path = os.getenv('csv_file_path')

# Vérifier si le répertoire existe, sinon le créer
if not os.path.exists(installation_directory):
    os.makedirs(installation_directory)

# Fonction pour extraire le texte de l'image et le stocker dans un fichier CSV
def extract_text_and_save_to_csv(image_path, csv_file_path):
    # Use Read API to read text in image
    with open(image_path, mode="rb") as image_data:
        read_op = client.read_in_stream(image_data, raw=True)

        # Get the async operation ID so we can check for the results
        operation_location = read_op.headers["Operation-Location"]
        operation_id = operation_location.split("/")[-1]

        # Wait for the asynchronous operation to complete
        while True:
            read_results = client.get_read_result(operation_id)
            if read_results.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
                break
            time.sleep(1)

        # If the operation was successfully, process the text line by line
        if read_results.status == OperationStatusCodes.succeeded:
            text = ""
            for page in read_results.analyze_result.read_results:
                for line in page.lines:
                    text += line.text + "\n"
            print(text)

    # Expression régulière pour extraire les informations spécifiques
    pattern = r"DEV ADDR:\s*([A-F0-9]+)\s*DEV EUI:\s*([A-F0-9]+)\s*APP EUI:\s*([A-F0-9]+)\s*APP KEY:\s*([A-F0-9]+)\s*APPSKEY:\s*([A-F0-9]+)\s*NETSKEY:\s*([A-F0-9]+)"

    # Recherche des correspondances dans la chaîne de caractères
    correspondances = re.search(pattern, text)

    # Vérifier si le fichier CSV existe
    file_exists = os.path.isfile(csv_file_path)

    # Si des correspondances sont trouvées, les enregistrer dans un fichier CSV
    if correspondances:
        dev_addr = correspondances.group(1)
        dev_eui = correspondances.group(2)
        app_eui = correspondances.group(3)
        app_key = correspondances.group(4)
        appskey = correspondances.group(5)
        netskey = correspondances.group(6)
        # Si le fichier existe, ajouter les informations à la suite
        if file_exists:
            with open(csv_file_path, 'a', newline='') as csvfile:  # Ouvrir en mode append ('a')
                fieldnames = ['DEV ADDR', 'DEV EUI', 'APP EUI', 'APP KEY', 'APPSKEY', 'NETSKEY']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
                # Vérifier si le fichier est vide (s'il n'a pas encore d'en-tête)
                if os.stat(csv_file_path).st_size == 0:
                    writer.writeheader()  # Écrire l'en-tête uniquement si le fichier est vide
        
                writer.writerow({'DEV ADDR': dev_addr,'DEV EUI': dev_eui, 'APP EUI': app_eui, 'APP KEY': app_key, 'APPSKEY': appskey, 'NETSKEY': netskey})
        
            print(f"Les informations ont été ajoutées à '{csv_file_path}'")
        else:
            # Si le fichier n'existe pas, le créer et écrire les informations
            with open(csv_file_path, 'w', newline='') as csvfile:
                fieldnames = ['DEV ADDR', 'DEV EUI', 'APP EUI', 'APP KEY', 'APPSKEY', 'NETSKEY']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'DEV ADDR': dev_addr, 'DEV EUI': dev_eui, 'APP EUI': app_eui, 'APP KEY': app_key, 'APPSKEY': appskey, 'NETSKEY': netskey})
        
            print(f"Le fichier '{csv_file_path}' a été créé et les informations ont été écrites dedans.")            
    else:
        print("Aucune information trouvée.")

# Fonction pour enregistrer l'image lorsque la combinaison de touches 'ctrl' + 's' est pressée
def save_image(e):
    if e.event_type == 'down' and e.name == 's' and keyboard.is_pressed('alt'):
        image_path = os.path.join(installation_directory, "image.png")
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        image_path = os.path.join(installation_directory, f"image_{timestamp}.png")
        cv2.imwrite(image_path, frame)
        print(f"Image enregistrée sous {image_path}")
        extract_text_and_save_to_csv(image_path, csv_file_path)  # Appeler la fonction pour extraire le texte de l'image après avoir enregistré l'image

def read_lines_csv(e):
    if e.event_type == 'down' and e.name == 'r' and keyboard.is_pressed('alt'):
        # Initialize a list to store device data
        device_data_list = []
        
        # Open the CSV file and read the data
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Extract data from the current row
                device_id = row['DEV ADDR']
                device_eui = row['DEV EUI']
                application_eui = row['APP EUI']
                application_key = row['APP KEY']
                network_session_key = row['NETSKEY']
                application_session_key = row['APPSKEY']
                
                # Store the data in a dictionary
                device_data = {
                    'device_id': device_id,
                    'device_eui': device_eui,
                    'application_eui': application_eui,
                    'application_key': application_key,
                    'network_session_key': network_session_key,
                    'application_session_key': application_session_key
                }
                
                # Add the device data to the list
                device_data_list.append(device_data)
        
        # Display the extracted data (optional)
        for device_data in device_data_list:
            print("Device ID:", device_data['device_id'])
            print("Device EUI:", device_data['device_eui'])
            print("Application EUI:", device_data['application_eui'])
            print("Application Key:", device_data['application_key'])
            print("Network Session Key:", device_data['network_session_key'])  # Add a newline between each device's data
            print("Application Session Key:", device_data['application_session_key'])
            
def add_TTN(e):
    if e.event_type == 'down' and e.name == 'a' and keyboard.is_pressed('alt'):
        device_data_list = []
        
        # Open the CSV file and read the data
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Extract data from the current row
                device_id = row['DEV ADDR']
                device_eui = row['DEV EUI']
                application_eui = row['APP EUI']
                application_key = row['APP KEY']
                network_session_key = row['NETSKEY']
                application_session_key = row['APPSKEY']
                
                # Store the data in a dictionary
                device_data = {
                    'device_id': device_id,
                    'device_eui': device_eui,
                    'application_eui': application_eui,
                    'application_key': application_key,
                    'network_session_key': network_session_key,
                    'application_session_key': application_session_key
                }
                
                # Add the device data to the list
                device_data_list.append(device_data)
        
        # Display the extracted data (optional) 
        for device_data in device_data_list:
            original.add_device_to_TTN(ip_serv, device_data['device_id'], device_data['device_eui'], device_data['application_session_key'], device_data['network_session_key'],  device_data['application_key'])

def synchro_all_images_from_directory(e):
    if e.event_type == 'down' and e.name == 'v' and keyboard.is_pressed('alt'):
        for filename in os.listdir(installation_directory):
            print(filename)
            time.sleep(6)
            if filename.endswith(".png") or  filename.endswith(".jpg"):
                image_path = os.path.join(installation_directory, filename)
                extract_text_and_save_to_csv(image_path, csv_file_path)
        print(f"Synchronisation des images du dossier {installation_directory} terminée")

# Connecter l'événement clavier à la fonction pour enregistrer l'image
keyboard.on_press(save_image)
keyboard.on_press(read_lines_csv)
keyboard.on_press(add_TTN)
keyboard.on_press(synchro_all_images_from_directory)

print("ALT + s : Enregistrer un device en ayant la photo en temps réel sur le téléphone \n" +
  "ALT + r : Lire le fichier CSV \n" +
  "ALT + a : Envoyer les données du fichier CSV sur TTS, une gestion des duplicatas est activée \n" +
  "ALT + v : Synchroniser les images du dossier des images")

while True:
    # Capture d'une trame de la webcam       
    ret, frame = cap.read()

# Libérer la capture
cap.release()
cv2.destroyAllWindows()  # Fermer toutes les fenêtres OpenCV