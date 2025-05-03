from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Valeur du nombre mystère (à chaque redémarrage du serveur, il est réinitialisé)
nombre_mystere = random.randint(1, 100)

@app.route("/")
def index():
    return "Bienvenue sur le serveur du jeu du nombre mystère !"

@app.route("/deviner", methods=["POST"])
def deviner():
    data = request.get_json()
    try:
        tentative = int(data.get("nombre"))
    except (ValueError, TypeError):
        return jsonify({"message": "Entrée invalide."}), 400

    if tentative < nombre_mystere:
        return jsonify({"resultat": "plus grand"})
    elif tentative > nombre_mystere:
        return jsonify({"resultat": "plus petit"})
    else:
        return jsonify({"resultat": "bravo"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))  # 10000 est une valeur par défaut facultative
    app.run(host="0.0.0.0", port=port)
# Déploiement Render - test commit
# Forcer un nouveau commit pour Render
# tetetetetett