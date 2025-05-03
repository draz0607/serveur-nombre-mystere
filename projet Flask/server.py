from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

scores = []

@app.route("/")
def home():
    return "Serveur Flask opérationnel !"

@app.route("/add_score", methods=["POST"])
def add_score():
    data = request.get_json()
    pseudo = data.get("pseudo")
    essais = data.get("essais")
    temps = data.get("temps")
    
    if pseudo and essais is not None and temps is not None:
        scores.append({"pseudo": pseudo, "essais": essais, "temps": temps})
        return jsonify({"status": "ok", "message": "Score enregistré"}), 200
    return jsonify({"status": "error", "message": "Données incomplètes"}), 400

@app.route("/get_scores", methods=["GET"])
def get_scores():
    return jsonify(scores)

if __name__ == "__main__":
    app.run(debug=True)
