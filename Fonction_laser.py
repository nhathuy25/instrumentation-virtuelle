"""
--------------Description du programme  -------------------------
Le but de ce programme est de regrouper les fonctions qui pilotent le laser et la caméra 
et de pouvoir les exécuter en ligne de commande.
-----------------------Groupe------------------------------------
- Khoa Vu
- Huy Nguyen
- Jules Toupin
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
        ser = Serial(port, 115200)
        #logger.log_port_connection(port, "successful", None)
        # print("Connexion au port : " + port + " réussie.")
    except Exception as e:
        #logger.log_port_connection(port, "failed", e)
        # print("Connexion au port : " + port + " échouée...")
        # print(e)
        return False,ser
    return True,ser


# Initialisation de la capture vidéo
def camera_VideoCapture(cam: str):
    return cv2.VideoCapture(cam)

# Connexion à une caméra
def camera_connection(cam,camera):
    try:
        camera = cv2.VideoCapture(cam)
        #logger.log_camera_connection(cam, "successful", None)
        # print("Connection to camera : " + str(cam) + " successful.")
    except Exception as e:
        #logger.log_camera_connection(cam, "failed", e)
        # print("Connection to camera : " + str(cam) + "  failed...")
        # print(e)
        return False,camera
    return True,camera

"""
        self.ui.device_co_connect.clicked.connect(self.connection_device)
        self.ui.device_co_refresh.clicked.connect(self.list_ports_device)
        self.ui.camera_co_connect.clicked.connect(self.connection_camera)
        self.ui.camera_co_refresh.clicked.connect(self.list_ports_camera)
        self.ui.device_info.clicked.connect(self.get_device_info)
        self.ui.control_button.clicked.connect(self.handle_beam)
        self.ui.clear_button.clicked.connect(self.clearing_points)
        self.ui.device_acquisition.clicked.connect(self.Acquisition)
    
        # Configuration des timers
        QTimer.singleShot(100, self.update_background)
        QTimer.singleShot(250, self.update_progress_bar)
"""  

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
def connection_device(port_str,Laser_connecte):
    # Récupération du port sélectionné dans l'interface utilisateur
    port = str(port_str)
    # Si un port est sélectionné
    if (port):
        # Tentative de connexion au port
        Laser_connecte = Laser.port_connection(port)[0]
    return Laser_connecte


"""
Propriété fonction 
Description : Méthode pour lister les caméras disponibles
auteur/autrice : Jules Toupin    
variable d'entrée : aucune
variable de sortie : liste_cameras : une liste des caméras disponibles,
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
        return liste_cameras,"No device found"
    else:
        return liste_cameras,"devices found"
    


"""
Ancien programme
# Méthode pour établir une connexion à la caméra sélectionnée dans la liste déroulante camera_co_listbox
def connection_camera(self):
    # Récupérer le nom de la caméra sélectionnée dans la liste déroulante
    self.ui.cam = str(self.ui.camera_co_listbox.currentItem().text())
    if (self.ui.cam):
        # Etablir la connexion à la caméra en utilisant le nom de la caméra
        self.ui.camera_connected = Laser.camera_connection(self.ui.cam)
"""

"""
Propriété fonction 
Description : Méthode pour établir une connexion à la caméra sélectionnée avec son nom
auteur/autrice : Jules Toupin    
variable d'entrée : nom caméra : le nom de la caméra sélectionnée avec la fonction list_ports_camera,
variable de sortie : 

"""
def connection_camera(nom_camera):
    # Récupérer le nom de la caméra sélectionnée dans la liste déroulante
    self.ui.cam = str(self.ui.camera_co_listbox.currentItem().text())
    if (self.ui.cam):
        # Etablir la connexion à la caméra en utilisant le nom de la caméra
        self.ui.camera_connected = Laser.camera_connection(self.ui.cam)
    
"""
    # Méthode pour sauvegarder l'état actuel du système
    def save_image(self):
        global n

        if self.ui.camera_connected:
            if not os.path.exists(image_directory+"mesure"+str(n)):
                os.makedirs(image_directory+"mesure"+str(n))

            # Capture de l'image
            pixmap = self.read_camera()

            # Convertir QPixmap en QImage
            q_image = pixmap.toImage()

            # Utiliser QPainter pour dessiner la croix rouge
            painter = QPainter(q_image)
            painter.setPen(QColor(Qt.red))
            
            # Taille de la croix
            cross_size = 10
            
            # Calcul des coordonnées du milieu de l'image
            mid_x = q_image.width() // 2
            mid_y = q_image.height() // 2

            # Dessiner la croix rouge
            painter.drawLine(mid_x - cross_size, mid_y, mid_x + cross_size, mid_y)
            painter.drawLine(mid_x, mid_y - cross_size, mid_x, mid_y + cross_size)

            # Fin de l'édition de l'image
            painter.end()

            # Sauvegarde de l'image
            q_image.save(image_directory +"/mesure"+str(n)+"/"+ "acquisition n°" + str(n) + ".png")
            n += 1

            # Log
            #logger.log_camera_save(self.ui.camera_connected, image_directory, n)
    
    def Acquisition(self):
        print("Acquisition")
        #logger.log_camera_acquisition()
        self.save_image()
        Vu=self.get_VuMetre(pourcentage=1)        
        # print("Vu = "+str(Vu))

    # Méthode pour lire le flux vidéo de la caméra connectée
    def read_camera(self):
        if (self.ui.camera_connected):
            # Créer un objet de capture vidéo à partir de l'index de la caméra
            camera = Laser.camera_VideoCapture(int(self.ui.cam))
            #print("La camera read 1 {} camera read 0 {}".format(camera.read()[0],camera.read()))
            # Lire l'image du flux vidéo et la convertir en image RGB
            cv2image = cv2.cvtColor(camera.read()[1], cv2.COLOR_BGR2RGB)
            # Redimensionner l'image en 400 x 315 pixels
            img = cv2.resize(cv2image, (400, 315))
            # Convertir l'image en format QPixmap pour affichage dans l'interface utilisateur
            return self.convert_cv_qt(img)
        else:
            return None 

    # Méthode pour convertir une image OpenCV en un format compatible avec l'affichage dans l'interface utilisateur
    def convert_cv_qt(self, cv_img):
        # Convertir l'image en RGB
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        # Récupérer les dimensions de l'image
        h, w, ch = rgb_image.shape
        # Calculer le nombre de bytes par ligne de l'image
        bytes_per_line = ch * w
        # Convertir l'image en format QImage
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        # Redimensionner l'image pour l'affichage
        p = convert_to_Qt_format.scaled(400, 315, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    # Méthode pour mettre à jour l'image de fond de l'interface utilisateur
    def update_background(self):
        if (self.ui.camera_connected): # Si la caméra est connectée
            self.ui.camera_return.setPixmap(self.read_camera()) # Mettre à jour l'image de la caméra
        else:
            self.ui.camera_return.setStyleSheet("background-color: black;") # Sinon, mettre un fond noir
        QTimer.singleShot(100, self.update_background) # Programmer une nouvelle exécution de la fonction après 100 ms

    # Méthode pour gérer l'état du faisceau laser
    def handle_beam(self):
        if self.ui.controller_connected: # Si le laser est connecté
            Laser.ser.write('Get,SensorHead,0,Laser\n'.encode()) # Envoyer une commande pour récupérer l'état du faisceau laser
            actif = Laser.ser.readline().decode('ascii','replace') # Lire la réponse du laser
            if(actif == "0\n"): # Si le faisceau est éteint
                self.ui.control_button.setText("Off") # Mettre à jour le texte du bouton
                self.ui.control_pan.setStyleSheet("background-color: lime;") # Mettre à jour la couleur de fond de la zone de contrôle
                Laser.ser.write('Set,SensorHead,0,Laser,1\n'.encode()) # Envoyer une commande pour allumer le faisceau laser
                #logger.log_laser_connect()
            if(actif== "1\n"): # Si le faisceau est allumé
                self.ui.control_button.setText("On") # Mettre à jour le texte du bouton
                self.ui.control_pan.setStyleSheet("background-color: pink;") # Mettre à jour la couleur de fond de la zone de contrôle
                Laser.ser.write('Set,SensorHead,0,Laser,0\n'.encode()) # Envoyer une commande pour éteindre le faisceau laser
                #logger.log_laser_disconnect()
        # else:
        #     print("ControlFrame.handle_beam: No controller connected...") # Afficher un message d'erreur si le laser n'est pas connecté
        #logger.log_controller_state(self.ui.controller_connected)

    # Méthode pour mettre à jour la barre de progression de la puissance du laser
    def update_progress_bar(self):
        if self.ui.controller_connected: # Si le laser est connecté
            Laser.ser.write('Get,SignalLevel,0,Value\n'.encode()) # Envoie une commande pour récupérer la puissance du laser
            actif = Laser.ser.readline().decode('ascii','replace') # Lire la réponse du laser
            #print("retour laser = " + actif)
            self.ui.signal_bar.setValue(int(float(actif)/775*100)) # Mettre à jour la barre de progression et convertir la valeur en pourcentage
        QTimer.singleShot(250, self.update_progress_bar)# Programmer une nouvelle exécution de la fonction après 250 ms
     #Récupère les coordonnées de la souris (x et y)

    def get_VuMetre(self,pourcentage=1):
        if self.ui.controller_connected: # Si le laser est connecté
            Laser.ser.write('Get,SignalLevel,0,Value\n'.encode()) # Envoie une commande pour récupérer la puissance du laser
            actif = Laser.ser.readline().decode('ascii','replace') # Lire la réponse du laser
            if pourcentage==1:
                #logger.log_viewmeter_acquisition(int(float(actif)/775*100))
                return(int(float(actif)/775*100)) # Renvoie le valeur du VU metre en pourcentage
            else:
                return actif # Renvoie le valeur du VU metre
        # else:
        #     print("ControlFrame.get_VuMetre: No controller connected...")
        #logger.log_controller_state(self.ui.controller_connected)

    #La def pour clear:
    def clearing_points (self):
        self.ui.camera_return.vider()


# Vérifier que ce fichier est le fichier principal qui est exécuté
if __name__ == "__main__":
    # Créer une instance de QApplication
    app = QtWidgets.QApplication(sys.argv)
    # Créer une instance de la classe Main
    MainWindow = Main()
    # Afficher la fenêtre principale
    MainWindow.show()
    # Lancer la boucle principale de l'application jusqu'à sa fermeture
    sys.exit(app.exec_())
"""