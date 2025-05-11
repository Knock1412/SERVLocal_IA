
import fitz  # PyMuPDF
import requests
import os

def extract_text_from_pdf(pdf_path):
    print("📂 Fichier demandé :", pdf_path)
    print("📁 Fichiers dans le dossier :", os.listdir("."))

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

def ask_question(context, question):
    url = "http://localhost:5000/ask"
    response = requests.post(url, json={"context": context, "question": question})
    if response.status_code == 200:
        return response.json().get("answer", "(pas de réponse)")
    else:
        print("❌ Erreur HTTP :", response.status_code, response.text)
        return None

if __name__ == "__main__":
    chemin_pdf = "LettreELNO.pdf"

    texte = extract_text_from_pdf(chemin_pdf)

    if texte.strip():
        resume = summarize_text(texte)
        print("\n📝 Résumé généré :\n")
        print(resume)

        while True:
            question = input("\n❓ Pose une question sur le document (ou tape 'exit' pour quitter) :\n> ")
            if question.lower() == "exit":
                break
            reponse = ask_question(texte, question)
            print("\n✅ Réponse IA :\n", reponse)

    else:
        print("⚠️ Aucun texte détecté ou fichier introuvable.")
