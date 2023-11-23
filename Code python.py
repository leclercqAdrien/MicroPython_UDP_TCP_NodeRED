import network
import usocket as socket
from machine import Pin
import utime

# Définir les paramètres du réseau
tcp_port = 1882
udp_port = 1881
server_ip = '192.168.2.110'
wifi_ssid = 'WiFi-2.4-1235'
wifi_password = '0AE81F9309'

# Configurer la LED sur la broche GPIO 2
led_pin = 2
led = Pin(led_pin, Pin.OUT)

# Se connecter au réseau Wi-Fi
def do_connect():
    Wconnect = network.WLAN(network.STA_IF)
    Wconnect.active(False)
    if not Wconnect.isconnected():
        print('Connecting to network...')
        Wconnect.active(True)
        Wconnect.connect(wifi_ssid, wifi_password)
        attempt = 0
        max_attempts = 10
        while not Wconnect.isconnected() and attempt < max_attempts:
            print (attempt)
            utime.sleep(1)  # Attendre 1 seconde avant chaque nouvelle tentative
            attempt += 1
        if Wconnect.isconnected():
            print('Connected!')
            led.off()
        else:
            print('Failed to connect to the network.')
            while 1:
                led.on()
    print('Network config:', Wconnect.ifconfig())

# Fonction pour envoyer des données sur une socket TCP
def send_tcp_data(data):
    try:
        s = socket.socket()
        addr = socket.getaddrinfo(server_ip, tcp_port)[0][-1]
        print(addr)
        s.connect(addr)
        s.sendall(str(data).encode())
        s.close()
    except Exception as e:
        print("Erreur lors de l'envoi des données TCP :", e)

# Fonction pour envoyer des données sur une socket UDP
def send_udp_data(data):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addr = socket.getaddrinfo(server_ip, udp_port)[0][-1]
        s.sendto(str(data).encode(), addr)
        s.close()
    except Exception as e:
        print("Erreur lors de l'envoi des données UDP :", e)

# Boucle principale d'envoi de données
def main_loop():
    data_to_send = 0

    while True:
        led.value(0)  # Allume la LED pour indiquer l'envoi de données

        # Envoi des données sur la socket TCP
        send_tcp_data(data_to_send)

        # Envoi des données sur la socket UDP
        send_udp_data(data_to_send)

        led.value(1)  # Éteint la LED
        utime.sleep(1)  # Ajoutez un délai en fonction de votre fréquence d'envoi
        data_to_send += 1

# Point d'entrée du programme
led.on()
do_connect()
main_loop()
