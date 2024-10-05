import json
import os
from env import BASE_DIR
from rich import print

def getMessages():
    try:
        messagesPath = os.path.join(BASE_DIR, "resources", "messages.json")
    except FileNotFoundError:
        print("[bold red]Error:[/bold red] No se encontró el archivo messages.json, intenta reinstalando el programa.")
        exit()
        
    file = open(messagesPath, "r", encoding="utf-8")

    return json.load(file)