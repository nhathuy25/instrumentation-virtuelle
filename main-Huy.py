from Fonction_laser import *

list_cameras, message = list_ports_camera()

print(message)
print("Nombre de camera detecte: ",len(list_cameras))

# Smile! You're on camera
save_image(0)