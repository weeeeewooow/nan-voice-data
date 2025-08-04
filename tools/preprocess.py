import os
# os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments" # Removed this line
import numpy as np
import pandas as pd
import librosa
from datasets import Dataset
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq

processor = AutoProcessor.from_pretrained("Jobaula/whisper-medium-nan-tw-common-voice")
model = AutoModelForSpeechSeq2Seq.from_pretrained("Jobaula/whisper-medium-nan-tw-common-voice")

#Jobaula/whisper-medium-nan-tw-common-voice
# 加入 forced_decoder_ids，鎖定語言與任務
model.config.forced_decoder_ids = processor.get_decoder_prompt_ids(
    task="transcribe"
)


# 9. 定義 preprocess 函數（加入檔案存在檢查）
def preprocess(batch):
    
    processor = AutoProcessor.from_pretrained("Jobaula/whisper-medium-nan-tw-common-voice")
    audio_path = batch["audio"]
    audio, _ = librosa.load(audio_path, sr=16000)

    # 特徵提取（Whisper expects log-mel spectrograms）
    features = processor.feature_extractor(audio, sampling_rate=16000).input_features[0]

    # 加上最大長度限制（Whisper 最大輸出長度為 448）
    labels = processor.tokenizer(
        batch["text"],
        max_length=448,
        padding="max_length",   # 如果你要用 Trainer，這樣對齊 padding
        truncation=True         # 重點：截斷過長的文字
    ).input_ids

    return {
        "input_features": features,
        "labels": labels
    }
def spilt(tsv_path, split_ratio=0.9):
    data_dir = os.curdir  # nan-tw 資料夾，內含 clips 和 train.tsv
    # 2. 讀取 .tsv
    df = pd.read_csv(os.path.join(data_dir, tsv_path), sep="\t")

    # 4. 產生完整音訊路徑
    df["audio"] = df["path"].apply(lambda x: os.path.join(data_dir, x.replace("\\", "/"))) # Construct absolute path
    df["text"] = df["sentence"]
    df = df[["audio", "text"]]
    df = df.reset_index(drop=True)
    # 5. 分割訓練與驗證集
    split = int(len(df) * split_ratio)
    df_train = df[:split].reset_index(drop=True)
    df_val = df[split:].reset_index(drop=True)

    return df_train, df_val


def preprocess_and_save(df, dsname):
    # 6. 建立 Dataset 物件
    ds = Dataset.from_pandas(df)
    
    # 10. 使用 map 預處理 Dataset
    ds = ds.map(preprocess, remove_columns=ds.column_names)
    preprocessed_path = "./preprocessed_data/" + dsname

    # Save the preprocessed datasets
    print(f"Saving preprocessed train dataset to {preprocessed_path}...")
    ds.save_to_disk(preprocessed_path)

#tra_val=spilt("train.tsv", 0.9)
#preprocess_and_save(tra_val[0], "train")
#preprocess_and_save(tra_val[1], "val")
test_val, _=spilt("test.tsv", 1.0)
preprocess_and_save(test_val, "test")
