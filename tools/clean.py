import csv
import os
import librosa

input_path = "letmecook.tsv"
output_path = "letmecook_c.tsv"
i = 0
clipsdir = []

total_dur = 0

# Columns: usually ["path", "sentence"]
with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8", newline="") as fout:
    reader = csv.DictReader(fin, delimiter="\t")
    writer = csv.DictWriter(fout, fieldnames=reader.fieldnames, delimiter="\t")
    writer.writeheader()

    for row in reader:
        # Clean punctuation
        row["sentence"] = row["sentence"].replace("，", "").replace("。", "").replace("!", "").replace("？", "")
        row["path"] = row["path"].replace("\\", "/")  # Normalize path

        if not os.path.exists(row["path"]):
                        print(f"Skipping missing audio file: {row["path"]}")
                        continue
        
        if(len(row["sentence"].strip()) >= 4):  # Only write non-empty sentences
            total_dur += librosa.get_duration(filename=row["path"])
            new_name = "clip_" + str(i).zfill(6) + ".wav"
            os.rename(row["path"], os.path.join(os.path.dirname(row["path"]), new_name))
            row["path"] = new_name
            i += 1
            writer.writerow(row)
        else:
            print(f"Skipping short sentence: {row['sentence']}")
            os.remove(row["path"])

print(f"Total duration of clips: {total_dur:.2f} seconds")
