import csv

# ===== 設定 =====
INPUT_TSV = "train.tsv"   # 你的原始資料
OUTPUT_TSV = "new_" + INPUT_TSV  # 輸出的檔案
ADD_NAN_TOKEN = True  # True 表示使用 <|nan|> 作為台語語言 token，False 則直接用 <|zh|>

# Whisper 翻譯格式標籤
START = "<|startoftranscript|>"
LANG_TAIGI = "<|nan|>" if ADD_NAN_TOKEN else "<|zh|>"
TASK = "<|translate|>"
LANG_CHINESE = "<|zh|>"

with open(INPUT_TSV, "r", encoding="utf-8") as fin, \
     open(OUTPUT_TSV, "w", encoding="utf-8", newline="") as fout:

    reader = csv.DictReader(fin, delimiter="\t")
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(fout, fieldnames=fieldnames, delimiter="\t")
    writer.writeheader()

    for row in reader:
        original_text = row["sentence"] if "sentence" in fieldnames else row["text"]

        # 在句子前加上翻譯模式標籤
        row["sentence"] = f"{START}{LANG_TAIGI}{TASK}{LANG_CHINESE} {original_text}"

        writer.writerow(row)

print(f"✅ 已輸出格式化的 TSV：{OUTPUT_TSV}")