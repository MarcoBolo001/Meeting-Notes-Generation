import requests


def transcribe_mp3_speechmatics(mp3_filepath, user_id, auth_token):
    # Endpoint per caricare il file e iniziare la trascrizione
    upload_url = f"https://api.speechmatics.com/v2/users/{user_id}/jobs/"

    # Configurazione per la trascrizione, includendo la diarization
    config = {
        "type": "transcription",
        "transcription_config": {
            "language": "en",
            "diarization": "speaker"
        }
    }

    # Headers per la richiesta
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    # File da inviare
    files = {
        "data_file": open(mp3_filepath, "rb"),
        "config": ("config.json", json.dumps(config), "application/json")
    }

    # Invia la richiesta POST per caricare il file e iniziare la trascrizione
    response = requests.post(upload_url, headers=headers, files=files)

    if response.status_code == 200:
        job_id = response.json()["id"]
        print(f"Job ID: {job_id}")

        # Endpoint per controllare lo stato del lavoro
        check_status_url = f"https://api.speechmatics.com/v2/users/{user_id}/jobs/{job_id}/"

        # Attendi che la trascrizione sia completata e recupera i risultati
        while True:
            status_response = requests.get(check_status_url, headers=headers)
            if status_response.status_code == 200:
                job_status = status_response.json()["job"]["status"]
                print(f"Job Status: {job_status}")
                if job_status == "completed":
                    # Recupera e stampa la trascrizione
                    transcription = status_response.json()["job"]["transcription"]
                    print(transcription)
                    break
                elif job_status == "failed":
                    print("Trascrizione fallita.")
                    break
            time.sleep(10)  # Attendi 10 secondi prima di controllare nuovamente lo stato
    else:
        print("Errore nell'invio del file per la trascrizione.")


# Utilizzo della funzione
transcribe_mp3_speechmatics("path/to/your/mp3file.mp3", "your_user_id", "your_auth_token")
