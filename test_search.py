
import requests

# Exemple de documents PDF extraits (contenus simulés)
documents = [
    
    "Cette fiche décrit du matériel réseau utilisé pour un projet de câblage.",
    "La liste des fournitures scolaires pour la rentrée 2024 est ici.",
    "Compte rendu de la réunion du département informatique.",
    "Stage de 2 mois",
    "Stage chez elno"
]

# Requête de recherche simulée
query = "stage entreprise informatique"

# Envoi vers le backend Flask
url = "http://localhost:5000/search"
response = requests.post(url, json={
    "query": query,
    "documents": documents
})

# Affichage des résultats
if response.status_code == 200:
    result = response.json()
    print("🔍 Requête :", query)
    print("✅ Meilleur document trouvé :")
    print("   ➤", result["best_match"])
    print("📊 Score de similarité :", round(result["score"], 4))
else:
    print("❌ Erreur :", response.status_code, response.text)
