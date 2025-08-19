import os
import csv

CLIPS_DIR = "extraclipsfortraining" 
OUTPUT_TSV = "letmecook.tsv"


with open(OUTPUT_TSV, 'w', newline='', encoding='utf-8') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    writer.writerow(['path','sentence'])  # Header

    for fname in sorted(os.listdir(CLIPS_DIR)):
        if fname.endswith('.wav'):
            wav_path = os.path.join(CLIPS_DIR, fname)
            txt_path = wav_path.replace('.wav', '.txt')
            if os.path.exists(txt_path):
                with open(txt_path, 'r', encoding='utf-8') as f:
                    text = f.read().strip()
                os.remove(txt_path)
                writer.writerow([wav_path, text])
