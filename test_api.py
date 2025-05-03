import requests

# Remplace cette URL par la tienne
url = "https://nombre-mystere.onrender.com"

# Envoie une tentative de nombre (modifie si tu veux tester autre chose)
data = {"nombre": 50}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Réponse du serveur :", response.json())
else:
    print("Erreur serveur :", response.status_code)
