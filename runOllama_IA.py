
import subprocess
import time
import os
import sys

def lancer_ollama():
    print("🚀 Lancement de Mistral via Ollama...")
    subprocess.Popen(["start", "cmd", "/k", "ollama run mistral"], shell=True)

def lancer_main_py():
    print("🧠 Lancement du serveur Flask (main.py)...")
    script_path = os.path.join(os.getcwd(), "main.py")
    subprocess.Popen(["start", "cmd", "/k", f"python {script_path}"], shell=True)

if __name__ == "__main__":
    lancer_ollama()
    time.sleep(5)  # Laisse le temps à Ollama de se lancer
    lancer_main_py()
