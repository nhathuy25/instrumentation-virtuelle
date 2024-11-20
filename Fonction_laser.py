"""
--------------Description du programme  -------------------------
Le but de ce programme est de regrouper les fonctions qui pilotent le laser et la caméra 
et de pouvoir les exécuter en ligne de commande.
-----------------------Groupe------------------------------------
- Khoa Vu
- Huy Nguyen
- Jules Toupin
- Lina EL MEKAOUI
"""

#----------------------------section-import------------------------------- 
import os
import time
from serial import Serial
import serial.tools.list_ports
import cv2
import numpy as np

"""
Propriété fonction 
Description :
    
auteur/autrice :
    
variable d'entrée :
    
variable de sortie :
"""

# --------------- CAMERA -------------------
"""
Propriété fonction 
Description : Fonction pour connecter à la camera à partir de l'indice de la camera
    !!! depend de la fonction list_ports_camera pour obtenir l'indice      

auteur/autrice : Huy NGUYEN, Khoa VU
    
variable d'entrée : id_cam -  id(indice) de la camera
variable de sortie : 
    - Si reussi a trouver un camera: 
                camera - un objet de type VideoCapture
    - Sinon:
                None
        -> Sert a la fonction 'read_camera()' pour lire l'image de la camera
"""
def connecter_camera(id_cam):
    try:
        camera = cv2.VideoCapture(id_cam)  # Connect to the camera
        # If the camera cannot be opened, raise an exception
        if not camera.isOpened():
            raise Exception(f"Unable to open camera with ID {id_cam}")
        return camera
    except Exception as e:
        print(f"Error: {e}")
        return None

"""
Propriété fonction 
Description : Méthode pour lister les caméras disponibles
auteur/autrice : Jules Toupin    
variable d'entrée :     aucune
variable de sortie :    liste_cameras : une liste des indices des caméras disponibles,
                        message : un message qui indique si des caméras ont été trouvées ou non
"""
def list_ports_camera():
    index = 0
    arr = []
    i = 5
        # Effacer la liste déroulante
    liste_cameras = []
    while i > 0:
        # Ouvrir une capture vidéo à partir de l'index actuel
        cap = cv2.VideoCapture(index)
        # Vérifier si la capture vidéo a réussi
        if cap.read()[0]:
            # Ajouter l'index de la caméra dans le tableau
            arr.append(index)
            # Créer un nom de périphérique pour la caméra en fonction du système d'exploitation
            device = str(index)
            # Ajouter le nom de périphérique à la liste déroulante
            liste_cameras.append(device)
                                                #self.ui.camera_co_listbox.addItem(device)   ancien programme
            cap.release()
        index += 1
        i -= 1
    # Si aucune caméra n'a été trouvée, afficher un message approprié dans la liste déroulante
    if (len(arr)==0):
        return liste_cameras,"Aucune camera trouvee"
    else:
        return liste_cameras,"Cameras trouvees"

"""
Propriété fonction 
Description : Fonction pour sauvegarder l'image de la camera. Les images sauvegardées sont stockées dans un répertoire nommé '/Measures'
    
auteur/autrice : Huy NGUYEN
    
variable d'entrée :     - id_cam
variable de sortie :    - aucune
"""
# Repertoire des images sauvegardées
image_directory = "Measures/"
# Méthode pour sauvegarder l'état actuel du système
def save_image(cam_id):

    # Prendre le temps actuel (ex: 20241024_102030)
    current_time = time.strftime("%Y%m%d_%H%M%S")

    # Capture de l'image
    rgb_image = read_camera(cam_id)  # Read RGB image from the camera

    # Vérifier si l'image a été capturée correctement
    if rgb_image is not None:
        # Sauvegarder l'image en tant que fichier .png
        image_path = os.path.join(image_directory, f"acquisition_{current_time}.png")
        cv2.imwrite(image_path, rgb_image)

        print(f"Image saved at: {image_path}")
    else:
        print("Erreur: Impossible de capturer l'image")

"""
Propriété fonction 
Description : Fonction pour lire l'image de la camera

auteur/autrice : Huy NGUYEN, Khoa VU

variable d'entrée   : id_cam - (indice de la camera choisie a partir de list_ports_camera)    
variable de sortie  : 
    - Si le camera est connecte : image
    - Sinon                     : None 

"""
def read_camera(id_cam):
    # Verifier la connexion de la camera, la variable camera est un objet de type VideoCapture
    camera = connecter_camera(id_cam)
    
    # Si la camera est connectee
    if camera is not None:
        # Lire l'image du flux vidéo et la convertir en image RGB
        ret, frame = camera.read()
        if ret:
            # Convertir l'image BGR (par défaut de OpenCV) en RGB
        
            rgb_image = convert_cv_to_rgb(frame)
            # Return the RGB image
            return rgb_image  
        
        else:
            print("Error: Impossible de lire l'image de la caméra")
            return None
    # Si on ne peut pas trouver une camera
    else:
        print("Error: Aucune caméra connectée")
        return None

"""
# Propriété fonction
# Description      : Méthode pour convertir une image OpenCV en RGB.
            Verifier si l'image est en RGB ou BGR et convertir en RGB si nécessaire.
# Auteur/autrice   : Lina EL MEKAOUI
# Variable d'entrée :   frame 
# Variable de sortie :  rgb_image 

"""
def convert_cv_to_rgb(frame):
    # Vérifie si l'image n'est pas en RGB ( est en format standard OpenCV)
    # Vérifie que l'image contient trois canaux de couleur et compare la moyenne du premier canal et du dernier canal 
    # (le premier canal est moins élevé en moyenne en genéral l'image est en BGR)
    if frame.shape[2] == 3 and frame[..., 0].mean() < frame[..., 2].mean(): 
        # Convertit en RGB 
        print("Image est en BGR")
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return rgb_image
    else:
        print("Image est en RGB")
        return frame
    
"""
Propriété fonction 
Description : Affichage le video de la camera sur une fenetre (Appuyer sur 'q' pour quitter la fenêtre)

auteur/autrice : Huy NGUYEN, Jules Toupin

variable d'entrée   : id_cam - (indice de la camera choisie a partir de list_ports_camera)    
variable de sortie  : None

"""
def display_camera_feed(id_cam=0): # l'indice de camera est mis par defaut a 0
    # Initialiser la camera de type cv2.VideoCapture avec l'indice de la camera
    camera = connecter_camera(id_cam)

    # Loop pour lire les images de la camera
    while True:
        # Capture frame-by-frame
        ret, frame = camera.read()
        
        # Si la frame (image) n'est pas lue, ret serais False
        if not ret:
            print("Erreur: Impossible de lire l'image de la caméra.")
            break

        # Display the frame
        cv2.imshow('Camera Feed', frame)

        # Appuyer sur 'q' pour quitter la fenêtre
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # En fin de boucle, relâcher la camera et fermer les fenêtres
    camera.release()
    cv2.destroyAllWindows()

# --------------- LASER -------------------
"""
Propriété fonction 
Description : Création d'une connexion série    
auteur/autrice : Jules Toupin    
variable d'entrée : aucune    
variable de sortie : un objet de type Serial
"""
def create_serial():
    return Serial()


"""
Propriété fonction 
Description : Connexion à un port série    
auteur/autrice : Jules Toupin    
variable d'entrée : port : le port à connecter, ser : l'objet de type Serial que l'on veut connecter au port    
variable de sortie : un booléen qui valide la connexion ou non et l'objet de type Serial
"""
# Connexion à un port série
def port_connection(port,ser):
    try:
        ser = Serial(port, 115200)
        #logger.log_port_connection(port, "successful", None)
        # print("Connexion au port : " + port + " réussie.")
    except Exception as e:
        #logger.log_port_connection(port, "failed", e)
        # print("Connexion au port : " + port + " échouée...")
        # print(e)
        return False,ser
    return True,ser

"""
Propriété fonction 
Description : Méthode pour obtenir les informations sur le dispositif  
auteur/autrice : Jules Toupin    
variable d'entrée : Laser_connecte : un booléen qui valide la connexion ou non;
                  Laser_ser : l'objet de type Serial connecté au dispositif    
variable de sortie : aucune idée de ce que ces 4 variables retournées sont
"""
def get_device_info(Laser_connecte,Laser_ser):
    # Si le contrôleur est connecté
        if Laser_connecte == 0:
            # Envoie de commandes au port série pour obtenir les informations
            Laser_ser.write('GetDevInfo,Controller,0,Name\n'.encode())
            name = Laser_ser.readline().decode('ascii','replace')
            # print(name)
            Laser_ser.write('GetDevInfo,Controller,0,Version\n'.encode())
            vers = Laser_ser.readline().decode('ascii','replace')
            # print(vers)
            Laser_ser.write('GetDevInfo,SensorHead,0,Name\n'.encode())
            nameSH = Laser_ser.readline().decode('ascii','replace')
            # print(nameSH)
            Laser_ser.write('GetDevInfo,SensorHead,0,Version\n'.encode())
            versSH = Laser_ser.readline().decode('ascii','replace')
            # print(versSH)
            # Mise à jour de l'interface utilisateur avec les informations obtenues
            #self.ui.device_info_l.setText("\nControler:\n"+ name + vers +"Laser:\n"+ nameSH + versSH)
            #logger.log_device_info(name, vers, nameSH, versSH)
            return name,vers,nameSH,versSH

    
"""
Propriété fonction 
Description : Méthode pour lister les ports disponibles pour le dispositif
auteur/autrice : Jules Toupin    
variable d'entrée : aucune
variable de sortie : liste_ports : une liste des ports disponibles,
                     message : un message qui indique si des ports ont été trouvés ou non
"""
def list_ports_device():
    # Récupération des ports série disponibles
    ports = serial.tools.list_ports.comports()
    
    # Effacement de la liste des ports
    liste_ports = []
    # Si des ports sont disponibles
    if (len(ports) != 0):
        devices = []
        # Pour chaque port disponible, ajout à la liste des ports de l'interface utilisateur
        for p in ports:
            liste_ports.append(p.device)
        return liste_ports,"devices found"
    else:
        return liste_ports,"No device found"

"""
Propriété fonction 
Description : Méthode pour établir une connexion avec le dispositif
auteur/autrice : Jules Toupin    
variable d'entrée : port_str : le port sélectionné dans l'interface utilisateur,
                    Laser_connecte : un booléen qui valide la connexion ou non
variable de sortie : laser_connecte : un booléen qui valide la connexion ou non

Update 24/10/2024: Huy a supprimé 'Laser.' 
                'Laser_connecte = Laser.port_connection(port)[0]' -> 'Laser_connecte = port_connection(port)[0]'
"""
def connection_device(port_str):
    # Récupération du port sélectionné dans l'interface utilisateur
    port = str(port_str)
    # Si un port est sélectionné
    if (port):
        # Tentative de connexion au port
        Laser_connecte = port_connection(port)[0]
    return Laser_connecte

"""
Propriété fonction 
Description : Méthode pour gérer l'état du faisceau laser
auteur/autrice : Jules Toupin    
variable d'entrée : Laser_connecte : un booléen qui valide la connexion ou non,
                    Laser_ser : l'objet de type Serial connecté au dispositif
variable de sortie : etat_laser : un str qui indique l'état du laser
"""
def handle_beam(Laser_connecte,Laser_ser):
    etat_laser = "inconnue"
    if Laser_connecte == 1: # Si le laser est connecté
        Laser_ser.write('Get,SensorHead,0,Laser\n'.encode()) # Envoyer une commande pour récupérer l'état du faisceau laser
        actif = Laser_ser.readline().decode('ascii','replace') # Lire la réponse du laser
        if(actif == "0\n"): # Si le faisceau est éteint
            """
            ancien programme gui
            text_bouton = "Off" # Mettre à jour le texte du bouton
            self.ui.control_button.setText("Off") # Mettre à jour le texte du bouton
            self.ui.control_pan.setStyleSheet("background-color: lime;") # Mettre à jour la couleur de fond de la zone de contrôle
            """
            Laser_ser.write('Set,SensorHead,0,Laser,1\n'.encode()) # Envoyer une commande pour allumer le faisceau laser
            etat_laser = "On"
            #logger.log_laser_connect()
        if(actif== "1\n"): # Si le faisceau est allumé
            """
            ancien programme gui
            self.ui.control_button.setText("On") # Mettre à jour le texte du bouton
            self.ui.control_pan.setStyleSheet("background-color: pink;") # Mettre à jour la couleur de fond de la zone de contrôle
            """
            Laser_ser.write('Set,SensorHead,0,Laser,0\n'.encode()) # Envoyer une commande pour éteindre le faisceau laser
            etat_laser = "Off"
            #logger.log_laser_disconnect()
    # else:
    #     print("ControlFrame.handle_beam: No controller connected...") # Afficher un message d'erreur si le laser n'est pas connecté
    #logger.log_controller_state(self.ui.controller_connected)
    return etat_laser

"""
Propriété fonction 
Description : Méthode pour récupérer la puissance du laser
auteur/autrice : Jules Toupin    
variable d'entrée : Laser_connecte : un booléen qui valide la connexion ou non,
                    Laser_ser : l'objet de type Serial connecté au dispositif
variable de sortie : actif : puissance du laser, voir ancien programme pour voir comment le gérer 
"""
def update_progress_bar(Laser_connecte,Laser_ser):
    if Laser_connecte == 1: # Si le laser est connecté
        Laser_ser.write('Get,SignalLevel,0,Value\n'.encode()) # Envoie une commande pour récupérer la puissance du laser
        actif = Laser_ser.readline().decode('ascii','replace') # Lire la réponse du laser
        #print("retour laser = " + actif)
        return actif 

"""
Propriété fonction 
Description : Méthode pour récupérer la puissance du laser
auteur/autrice : Jules Toupin    
variable d'entrée : Laser_connecte : un booléen qui valide la connexion ou non,
                    Laser_ser : l'objet de type Serial connecté au dispositif
variable de sortie : valeur du vue mètre 
"""
def get_VuMetre(Laser_connecte,Laser_ser,pourcentage=1):
    if Laser_connecte == 1: # Si le laser est connecté
        Laser_ser.write('Get,SignalLevel,0,Value\n'.encode()) # Envoie une commande pour récupérer la puissance du laser
        actif = Laser_ser.readline().decode('ascii','replace') # Lire la réponse du laser
        if pourcentage==1:
            #logger.log_viewmeter_acquisition(int(float(actif)/775*100))
            return(int(float(actif)/775*100)) # Renvoie le valeur du VU metre en pourcentage
        else:
            return actif # Renvoie le valeur du VU metre
    # else:
    #     print("ControlFrame.get_VuMetre: No controller connected...")
    #logger.log_controller_state(self.ui.controller_connected)


# Vérifier que ce fichier est le fichier principal qui est exécuté
if __name__ == "__main__":

    # Liste des caméras disponibles
    list_cameras, message = list_ports_camera()

    print(message)
    print("Nombre de camera detecte: ",len(list_cameras))

    # Smile! You're on the camera
    save_image(0)