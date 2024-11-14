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
        ser = Serial(port, 9600)
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
