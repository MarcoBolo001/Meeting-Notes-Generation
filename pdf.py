import http.client
import base64
import json

import openai
import jwt


def pdf_generation(file_path):
    """
        Genera un pdf utilizzando le API di pdfgenerationapi e quelle di openAi.

        Args:
            not required

        Returns:
            nothing, it just saves the file into "./output"

        """
    conn = http.client.HTTPSConnection("us1.pdfgeneratorapi.com")

    # id value del template
    id_value = "id del template"
    # Nomi delle sezioni come delimitatori, assicurati che corrispondano esattamente a quelli nel file
    section_names = [
        "Meeting Title:",
        "Location:",
        "Date:",
        "Attendees:",
        "Agenda items discussed:",
        "Summary:",
        "Notes:"
    ]


    sections_content = {}

    section_names_lower = [section.lower() for section in section_names]

    # Leggi il contenuto del file
    with open(file_path, 'r') as file:
        content = file.read().lower()  # Converti tutto il contenuto in minuscolo

    # Inizializza le variabili per il tracking delle sezioni
    current_section = None
    content_start = 0

    # Itera attraverso ogni carattere nel contenuto
    for i in range(len(content)):
        # Per ogni titolo di sezione, verifica se il segmento corrente del testo corrisponde
        for section in section_names_lower:
            section_end = i + len(section)
            if content[i:section_end] == section:
                if current_section:
                    # Salva il contenuto della sezione precedente
                    sections_content[current_section] = content[content_start:i].strip()
                current_section = section_names[
                    section_names_lower.index(section)]  # Usa il titolo originale della sezione
                content_start = section_end  # Imposta l'inizio del contenuto per la sezione corrente

    # Assicurati di catturare il contenuto dell'ultima sezione
    if current_section:
        sections_content[current_section] = content[content_start:].strip()

    # Assumendo che `sections_content` sia già stato popolato come prima
    agenda_content = sections_content.get("Agenda items discussed:", "")

    # Suddividi il contenuto in base ai trattini che indicano nuovi item
    items = agenda_content.split('-')

    # Ricostruisci il contenuto, inserendo una riga vuota tra gli item e un trattino all'inizio di ogni item
    new_agenda_content = ""
    for item in items:
        item = item.strip()  # Rimuove gli spazi bianchi iniziali e finali da ogni item
        if item:  # Ignora le stringhe vuote che possono risultare dalla split
            new_agenda_content += "- " + item + "\n\n"

    # Rimuovi l'ultima riga vuota aggiunta in eccesso
    new_agenda_content = new_agenda_content.strip()

    payload = {            #payload del template
        "id": id_value,
        "description": sections_content.get("Meeting Title:", "Contenuto non trovato"),
        "location": sections_content.get("Location:", "Contenuto non trovato"),
        "date": sections_content.get("Date:", "Contenuto non trovato"),
        "attendees": sections_content.get("Attendees:", "Contenuto non trovato"),
        "summary": sections_content.get("Summary:", "Contenuto non trovato"),
        "items": new_agenda_content,
        "notes": sections_content.get("Notes:", "Contenuto non trovato")
    }

    payload_json = json.dumps(payload)

    # parte relativa alla generazione del token JWT
    secret_key = "insert your secret key"     #inserire il segreto

    # Definisci il payload del JWT
    authentication_payload = {
        "iss": "insert your apikey", #inserire apikei
        "sub": "insert your email",
        "exp": 83738594538954783
    }

    # Genera il token JWT
    token = jwt.encode(authentication_payload, secret_key, algorithm='HS256')

    headers = {
        'content-type': "application/json",
        'Authorization': "Bearer " + token,
        "alg": "HS256",
        "typ": "JWT"
    }

    # chiamata post alle api di pdfgenerationapi
                                                      #template id
    conn.request("POST", "/api/v3/templates/956191/output?name=My%20document&format=pdf&output=base64",
                 payload_json, headers)
    res = conn.getresponse()
    # stampo solo se ci sono errori nella risposta
    if res.status >= 400:
        print("Errore nella richiesta:")
        print("Codice di stato:", res.status)
        print("Messaggio di errore:", res.read().decode("utf-8"))

    else:
        data = res.read()
        response_json = json.loads(data.decode('utf-8'))
        pdf_base64 = response_json['response']
        pdf_data = base64.b64decode(pdf_base64)

        return pdf_data


#pdf_generation()

