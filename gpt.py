import openai


def meeting_note_generation(id,testo):

    ita = "in italiano"
    eng = "in inglese"
    language = eng

    prompt = "Scrivi una business meeting note più compelta possibile ed " + language + " per il meeting che ti fornirò a fine di questo prompt." \
             "Assicurati di includere TUTTE e SOLE le sezioni 'Meeting Title:','Location:','Date:','Attendees:','Agenda items discussed:','Summary:', 'Notes:'." \
             "E' importante che i titoli dei parahrafi siano solo quelli indicati, non aggingere altri caratteri."\
             "il luogo e la data che ti invierò devi separarli e metterli in 2 campi appositi, i partecipanti mettili in un elenco puntato ( tutti quelli prima di  ogni ':'). " \
             "Se capisci il nome dei partecipanti scrivilo nell'apposita sezione, invece nella sezione degli item fai un elenco PUNTATO, non farlo numerato (nel fare l' elenco non devi aggiugnere un numero iniziale ad ogni riga, basta scrivere solo item 1:)."\
             "dilungati di più nel summary, fallo discorsivo,"\
             "l'obiettivo è fornire una meeting note chiara e completa." \
             "NON includere una formula di chiusura, mi serve esclusivamente la meeting note, quando hai finito di scriverla fermati. Ti mando una row presa da un dataset di meetings, " \
             "in cui troverai la conversazione trascritta:\n\n" "luogo e ora: " + id + "\ntesto: " + testo

    # Chiamata all'API di OpenAI utilizzando il prompt
    risposta = openai.ChatCompletion.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=1,
        max_tokens=2500
    )

    # Estrae la risposta dall'output
    meeting_note = risposta.choices[0].message.content
    return meeting_note

    # Salvataggio dell'output in un file di testo
    with open("output/meeting_note.txt", "w") as file:
        file.write(meeting_note)

    print("Meeting note generata e salvata nel file 'meeting_note.txt'")
    return meeting_note

openai.api_key = 'insert your apikey'