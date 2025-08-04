import csv

input_path = "merged_clips_updated.tsv"
output_path = "merged_clips_updated_c.tsv"

# Columns: usually ["path", "sentence"]
with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8", newline="") as fout:
    reader = csv.DictReader(fin, delimiter="\t")
    writer = csv.DictWriter(fout, fieldnames=reader.fieldnames, delimiter="\t")
    writer.writeheader()

    for row in reader:
        # Clean punctuation
        row["sentence"] = row["sentence"].replace("，", "").replace("。", "").replace("!", "").replace("？", "")
        writer.writerow(row)
