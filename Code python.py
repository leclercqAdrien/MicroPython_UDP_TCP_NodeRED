import network  # Importer la bibliothèque réseau
import usocket as socket  # Importer le module socket sous le nom usocket
from machine import Pin  # Importer la classe Pin de la bibliothèque machine
import utime  # Importer la bibliothèque utime pour la gestion du temps

# Définir les paramètres du réseau
tcp_port = 1882  # Port TCP utilisé pour la communication
udp_port = 1881  # Port UDP utilisé pour la communication
server_ip = '192.168.2.110'  # Adresse IP du serveur auquel envoyer les données
wifi_ssid = 'WiFi-2.4-1235'  # Nom du réseau Wi-Fi
wifi_password = '0AE81F9309'  # Mot de passe du réseau Wi-Fi

# Configurer la LED sur la broche GPIO 2
led_pin = 2  # Numéro de la broche GPIO à laquelle la LED est connectée
led = Pin(led_pin, Pin.OUT)  # Configurer la broche GPIO en mode de sortie pour la LED

# Se connecter au réseau Wi-Fi
def do_connect():
    Wconnect = network.WLAN(network.STA_IF)  # Créer une instance de la classe WLAN en mode client
    Wconnect.active(False)  # Désactiver le module Wi-Fi au début
    if not Wconnect.isconnected():  # Si le module n'est pas déjà connecté
        print('Connexion au réseau...')
        Wconnect.active(True)  # Activer le module Wi-Fi
        Wconnect.connect(wifi_ssid, wifi_password)  # Se connecter au réseau Wi-Fi
        attempt = 0
        max_attempts = 10
        while not Wconnect.isconnected() and attempt < max_attempts:
            print(attempt)
            utime.sleep(1)  # Attendre 1 seconde avant chaque nouvelle tentative
            attempt += 1
        if Wconnect.isconnected():
            print('Connecté !')
            led.off()  # Éteindre la LED pour indiquer une connexion réussie
        else:
            print('Échec de la connexion au réseau.')
            while 1:
                led.on()  # Allumer la LED en cas d'échec de connexion
    print('Configuration du réseau:', Wconnect.ifconfig())  # Afficher la configuration réseau après la connexion

# Fonction pour envoyer des données sur une socket TCP
def send_tcp_data(data):
    try:
        s = socket.socket()  # Créer une nouvelle instance de socket
        addr = socket.getaddrinfo(server_ip, tcp_port)[0][-1]  # Obtenir les informations d'adresse
        print(addr)
        s.connect(addr)  # Établir une connexion avec le serveur
        s.sendall(str(data).encode())  # Envoyer les données encodées en UTF-8
        s.close()  # Fermer la connexion après l'envoi
    except Exception as e:
        print("Erreur lors de l'envoi des données TCP :", e)  # Afficher une erreur en cas de problème

# Fonction pour envoyer des données sur une socket UDP
def send_udp_data(data):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Créer une instance de socket UDP
        addr = socket.getaddrinfo(server_ip, udp_port)[0][-1]  # Obtenir les informations d'adresse
        s.sendto(str(data).encode(), addr)  # Envoyer les données encodées en UTF-8 à l'adresse spécifiée
        s.close()  # Fermer la connexion après l'envoi
    except Exception as e:
        print("Erreur lors de l'envoi des données UDP :", e)  # Afficher une erreur en cas de problème

# Boucle principale d'envoi de données
def main_loop():
    data_to_send = 0  # Initialiser la variable des données à envoyer

    while True:

        # Envoi des données sur la socket TCP
        send_tcp_data(data_to_send)

        # Envoi des données sur la socket UDP
        send_udp_data(data_to_send)

        utime.sleep(1)  # Ajoutez un délai en fonction de votre fréquence d'envoi
        data_to_send += 1  # Incrémenter les données à envoyer

# Point d'entrée du programme
led.on()  # Allumer la LED au début de l'exécution
do_connect()  # Appeler la fonction de connexion Wi-Fi
main_loop()  # Entrer dans la boucle principale d'envoi de données