from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app)

# Le nombre mystère est tiré au sort à chaque redémarrage du serveur
nombre_mystere = random.randint(1, 100)

@app.route("/", methods=["GET"])
def index():
    return "Bienvenue sur le serveur du jeu du nombre mystère !"

@app.route("/deviner", methods=["POST"])
def deviner():
    data = request.get_json()
    if not data or "nombre" not in data:
        return jsonify({"message": "Donnée manquante."}), 400

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
    port = int(os.environ.get("PORT", 5000))  # Render fournit PORT dans les variables d'env
    app.run(host="0.0.0.0", port=port)
