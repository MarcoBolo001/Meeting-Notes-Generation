import pandas as pd
from gpt import meeting_note_generation
from pdf import pdf_generation

# Carica i dati dal file CSV
dataset = pd.read_csv("dataset/test.csv")
# Prepara un DataFrame vuoto per le meeting notes
meeting_notes_df = pd.DataFrame(columns=['ID', 'MeetingNote'])

# Itera sui primi 20 elementi del dataset
for i in range(20):
    id = dataset.iloc[i, 0]
    testo = dataset.iloc[i, 1]
    # Genera la meeting note
    meeting_note = meeting_note_generation(id, testo)

    # Aggiungi la meeting note al DataFrame
    meeting_notes_df = meeting_notes_df.append({'ID': id, 'MeetingNote': meeting_note}, ignore_index=True)

    # Salva la meeting note in un file txt
    txt_file_name = f"output/txt/meeting_note_{id}.txt"
    with open(txt_file_name, 'w') as txt_file:
        txt_file.write(meeting_note)

    # Genera il PDF a partire dal file txt delle meeting note
    pdf_data = pdf_generation(txt_file_name)

    # Salva i dati PDF in un nuovo file PDF
    pdf_file_name = f"output/pdf/meeting_note_{id}.pdf"
    with open(pdf_file_name, "wb") as pdf_file:
        pdf_file.write(pdf_data)

    print(f"Meeting note e PDF per l'ID {id} generati e salvati.")


meeting_notes_df.to_csv("output/csv/meeting_notes.csv", index=False)