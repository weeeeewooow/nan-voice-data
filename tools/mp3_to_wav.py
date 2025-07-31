import os
import wave
import contextlib
import csv
from pydub import AudioSegment

CLIPS_DIR = "merged_clips"
TSV_PATH = "merged_clips.tsv"
UPDATED_TSV_PATH = "merged_clips_updated.tsv"
DELETE_MP3 = True  # Set to False if you want to keep .mp3 files

def get_duration(wav_path):
    with contextlib.closing(wave.open(wav_path, 'r')) as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        return round(frames / float(rate), 3)

# Step 1: Convert all .mp3 to .wav
print("Converting MP3 to WAV...")
for fname in os.listdir(CLIPS_DIR):
    if not os.path.exists(os.path.join(CLIPS_DIR, fname)):
        print(f"Skipping missing audio file: {fname}")
    if fname.endswith(".mp3"):
        mp3_path = os.path.join(CLIPS_DIR, fname)
        if not os.path.exists(mp3_path):
            print(f"Skipping missing audio file: {fname}")

        wav_name = fname.replace(".mp3", ".wav")
        wav_path = os.path.join(CLIPS_DIR, wav_name)

        if os.path.exists(os.path.join(CLIPS_DIR, fname)):
            print(f"Skipping existing audio file: {wav_path}")

        audio = AudioSegment.from_mp3(mp3_path)
        audio.export(wav_path, format="wav")

        if DELETE_MP3:
            os.remove(mp3_path)
        print(f"Converted: {fname} -> {wav_name}")

print("All MP3 files converted to WAV.")

# Step 2: Update TSV file
print("\nUpdating TSV file...")
with open(TSV_PATH, 'r', encoding='utf-8') as tsv_in, \
     open(UPDATED_TSV_PATH, 'w', encoding='utf-8', newline='') as tsv_out:
    
    reader = csv.DictReader(tsv_in, delimiter='\t')
    writer = csv.DictWriter(tsv_out, delimiter='\t', fieldnames=['path', 'sentence'])
    writer.writeheader()

    for row in reader:
        path = row['path']
        if path.endswith('.mp3'):
            new_path = path.replace('.mp3', '.wav')
            row['path'] = new_path
            wav_path = new_path if os.path.isabs(new_path) else os.path.join(CLIPS_DIR, os.path.basename(new_path))
            if not os.path.exists(wav_path):
                print(f"Missing converted file: {wav_path}")
        writer.writerow(row)

print(f"✅ Done! Updated TSV saved as {UPDATED_TSV_PATH}")