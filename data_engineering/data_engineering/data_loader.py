
import pandas as pd

file_id = "1ck8GJFPYxAXKLnl8wyGz3qa5EM4t-LPU"  # ID файла на Google Drive
file_url = f"https://drive.google.com/uc?id={file_id}"

raw_data = pd.read_csv(file_url)     # читаем файл

print(raw_data.head(10))       # выводим на экран первые 10 строк для проверки
raw_data.to_csv("data/raw/dataset.csv", index=False)  # сохраняем в папку raw