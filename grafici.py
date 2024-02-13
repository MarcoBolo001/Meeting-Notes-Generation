import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from metriche import calculate_cosine_similarity, normalize_text, calculate_bleu, calculate_rouge_n, calculate_meteor_score
import re

# Definizione delle funzioni normalize_text e calculate_cosine_similarity come fornito in precedenza


# Leggi i primi 10 elementi della seconda colonna dai file CSV
csv1 = pd.read_csv("dataset/train_modificato.csv").iloc[:20, 1]
csv2 = pd.read_csv("output/csv/meeting_notes.csv").iloc[:20, 1]

# Calcola la similarità coseno per ogni coppia di testi
similarities = []
bleu_scores = []
rouge_scores = []
meteor_scores=[]
for text1, text2 in zip(csv1, csv2):

    norm_text1=normalize_text(text1)
    norm_text2=normalize_text(text2)
    similarity = calculate_cosine_similarity(norm_text1, norm_text2)
    similarities.append(similarity)

    bleu_score = calculate_bleu(norm_text1, norm_text2)
    bleu_scores.append(bleu_score)

    rouge_score = calculate_rouge_n(norm_text1, norm_text2, n=1)  # ROUGE-1
    rouge_scores.append(rouge_score)
 # Calcola METEOR
    meteor_score = calculate_meteor_score(norm_text1, norm_text2)
    meteor_scores.append(meteor_score)

# Visualizza i risultati in un grafico a barre
plt.figure(figsize=(20, 6))
plt.bar(range(1, 21), similarities, color='skyblue')
plt.axhline(y=np.mean(similarities), color='r', linestyle='-', label='Media')
plt.axhline(y=np.mean(similarities)+np.std(similarities), color='b', linestyle='-', label='Media')
plt.axhline(y=np.mean(similarities)-np.std(similarities), color='g', linestyle='-', label='Media')
plt.xlabel('Meeting Notes')
plt.ylabel('Cosine Similarity')
plt.xticks(range(1, 21))
plt.show()

# Visualizza i punteggi BLEU in un grafico
plt.figure(figsize=(20, 6))
#plt.subplot(1, 2, 1)
plt.bar(range(1, 21), bleu_scores, color='orange')
plt.axhline(y=np.mean(bleu_scores), color='r', linestyle='-', label='Media')
plt.axhline(y=np.mean(bleu_scores)+np.std(bleu_scores), color='b', linestyle='-', label='Media')
plt.axhline(y=np.mean(bleu_scores)-np.std(bleu_scores), color='g', linestyle='-', label='Media')
plt.xlabel('Meeting Notes')
plt.ylabel('BLEU Score')
plt.xticks(range(1, 21))

plt.show()


# Visualizza i punteggi ROUGE-1 F1 in un grafico
plt.figure(figsize=(20, 6))
plt.bar(range(1, 21), rouge_scores, color='lightgreen')
plt.axhline(y=np.mean(rouge_scores), color='r', linestyle='-', label='Media')
plt.axhline(y=np.mean(rouge_scores)+np.std(rouge_scores), color='b', linestyle='-', label='Media')
plt.axhline(y=np.mean(rouge_scores)-np.std(rouge_scores), color='g', linestyle='-', label='Media')
plt.xlabel('Meeting Notes')
plt.ylabel(' ROUGE-1 F1 Score')
plt.xticks(range(1, 21))
plt.show()

plt.figure(figsize=(20, 6))
plt.bar(range(1, 21), meteor_scores, color='lightpink')
plt.axhline(y=np.mean(meteor_scores), color='r', linestyle='-', label='Media')
plt.axhline(y=np.mean(meteor_scores)+np.std(meteor_scores), color='b', linestyle='-', label='Media')
plt.axhline(y=np.mean(meteor_scores)-np.std(meteor_scores), color='g', linestyle='-', label='Media')
plt.xlabel('Meeting Notes')
plt.ylabel('METEOR Score')
plt.xticks(range(1, 21))

plt.show()