from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge
from nltk.translate.meteor_score import meteor_score as nltk_meteor_score
import nltk
import re
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('wordnet')

def normalize_text(text):
    # Rimozione dei caratteri non corretti
    cleaned_text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Normalizzazione della stringa
    normalized_text = cleaned_text.lower().strip()

    # Rimozione dei caratteri di nuova riga e formattazione su una riga singola
    normalized_text = normalized_text.replace('\n', '')
    normalized_text = normalized_text.replace('\r', '')
    normalized_text = normalized_text.replace('\t', '')
    normalized_text = ' '.join(normalized_text.split())

    return normalized_text


def calculate_meteor_score(reference, candidate):
    # Tokenizza i testi
    tokenized_reference = word_tokenize(reference)
    tokenized_candidate = word_tokenize(candidate)

    # Calcola il punteggio METEOR usando la funzione di NLTK, evitando il conflitto di nomi
    score = nltk_meteor_score([tokenized_reference], tokenized_candidate)
    return score


def calculate_bleu(reference, candidate):
    reference = [reference.split()]  # La funzione sentence_bleu si aspetta una lista di liste come riferimenti
    candidate = candidate.split()
    score = sentence_bleu(reference, candidate, weights=(0.25, 0.25, 0.25, 0.25))  # Pesature uniformi
    return score

# Calcola il punteggio ROUGE
def calculate_rouge(reference, candidate):
    rouge = Rouge()
    scores = rouge.get_scores(candidate, reference)
    return scores[0]  # Ritorna il primo punteggio ROUGE

# Calcola il punteggio ROUGE-N
def calculate_rouge_n(reference, candidate, n=1):
    if n == 1:
        metric = 'rouge-1'
    elif n == 2:
        metric = 'rouge-2'
    else:
        raise ValueError("Supporto solo per ROUGE-1 e ROUGE-2")

    rouge = Rouge(metrics=[metric])
    scores = rouge.get_scores(candidate, reference)
    return scores[0][metric]['f']  # F1-score

class CustomVectorizer(TfidfVectorizer):
    def build_preprocessor(self):
        return lambda x: x


def calculate_cosine_similarity(text1, text2):
    """
       Calcola la similarità coseno tra due testi utilizzando la rappresentazione vettoriale TF-IDF.

       Args:
           text1 (str): Il primo testo da confrontare.
           text2 (str): Il secondo testo da confrontare.

       Returns:
           float: Il valore di similarità coseno tra i due testi.

       """

    # Creazione di un vettore di funzionalità TF-IDF per i testi
    vectorizer = CustomVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    # Calcolo della similarità coseno tra i vettori dei testi
    cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])

    return cosine_sim[0][0]

