import requests
from sentence_transformers import SentenceTransformer, util
import torch
from flask import Flask, request, jsonify

app = Flask(__name__)

# Chargement du modèle de recherche sémantique
print("Chargement du modèle SentenceTransformer...")
search_model = SentenceTransformer('all-MiniLM-L6-v2')

# === Résumé avec Mistral (via Ollama) ===
@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Texte vide"}), 400

    prompt = f"Résume le texte suivant en français de façon concise :\n\n{text}"

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )
        result = response.json()
        summary = result.get("response", "").strip()
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# === Recherche sémantique ===
@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    query = data.get("query")
    documents = data.get("documents")  # liste de textes

    if not query or not documents:
        return jsonify({"error": "Requête ou documents manquants"}), 400

    try:
        query_embedding = search_model.encode(query, convert_to_tensor=True)
        doc_embeddings = search_model.encode(documents, convert_to_tensor=True)

        similarities = util.cos_sim(query_embedding, doc_embeddings)[0]
        best_idx = int(torch.argmax(similarities))
        best_score = float(similarities[best_idx])

        return jsonify({
            "best_match": documents[best_idx],
            "score": best_score
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
