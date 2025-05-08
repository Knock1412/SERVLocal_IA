import fitz  # PyMuPDF
import requests
import os

def extract_text_from_pdf(pdf_path):
    print("📂 Fichier demandé :", pdf_path)
    print("📁 Fichiers dans le dossier :", os.listdir("."))

    # Vérifie que le fichier existe vraiment
    if not os.path.isfile(pdf_path):
        print(f"❌ Le fichier '{pdf_path}' n'existe pas dans ce dossier.")
        return ""

    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def summarize_text(text):
    url = "http://localhost:5000/summarize"
    response = requests.post(url, json={"text": text})
    if response.status_code == 200:
        return response.json()["summary"]
    else:
        print("❌ Erreur HTTP :", response.status_code, response.text)
        return None

if __name__ == "__main__":
    chemin_pdf = "LettreELNO.pdf"  # ← Assure-toi que le nom est exact et que le fichier est bien dans ce dossier

    texte = extract_text_from_pdf(chemin_pdf)

    if texte.strip():
        resume = summarize_text(texte)
        print("\n📝 Résumé généré :\n")
        print(resume)
    else:
        print("⚠️ Aucun texte détecté ou fichier introuvable.")