import fitz  # PyMuPDF
import requests

def extract_text_from_pdf(pdf_path):
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
        print("Erreur :", response.status_code, response.text)
        return None

if __name__ == "__main__":
    chemin_pdf = "LettreELNO.pdf"  # ← fichier renommé sans espace
    texte = extract_text_from_pdf(chemin_pdf)
    if texte.strip():
        resume = summarize_text(texte)
        print("\n📝 Résumé généré :\n")
        print(resume)
    else:
        print("❌ Aucun texte détecté dans le PDF.")
