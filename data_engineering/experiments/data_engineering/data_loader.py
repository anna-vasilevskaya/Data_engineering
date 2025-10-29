import pandas as pd
import numpy as np


def load_and_process_dataset(file_url: str) -> pd.DataFrame:
    raw_data = pd.read_csv(file_url)

    raw_data["Observation ID"] = raw_data["Observation ID"].astype("uint16")
    raw_data["Common Name"] = raw_data["Common Name"].astype("category")
    raw_data["Scientific Name"] = raw_data["Scientific Name"].astype("category")
    raw_data["Family"] = raw_data["Family"].astype("category")
    raw_data["Genus"] = raw_data["Genus"].astype("category")
    raw_data["Observed Length (m)"] = raw_data["Observed Length (m)"].astype("float16")
    raw_data["Observed Weight (kg)"] = raw_data["Observed Weight (kg)"].astype(
        "float16"
    )
    raw_data["Age Class"] = raw_data["Age Class"].astype("category")
    raw_data["Sex"] = raw_data["Sex"].astype("category")
    raw_data["Date of Observation"] = pd.to_datetime(
        raw_data["Date of Observation"], format="%d-%m-%Y"
    )
    raw_data["Country/Region"] = raw_data["Country/Region"].astype("category")
    raw_data["Habitat Type"] = raw_data["Habitat Type"].astype("category")
    raw_data["Conservation Status"] = raw_data["Conservation Status"].astype("category")
    raw_data["Observer Name"] = raw_data["Observer Name"].astype("category")
    raw_data["Notes"] = raw_data["Notes"].astype(
        "object"
    )  # Keep as object for long texts

    return raw_data


def main():
    """Main function for standalone execution."""
    file_id = "1ck8GJFPYxAXKLnl8wyGz3qa5EM4t-LPU"  # ID файла на Google Drive
    file_url = f"https://drive.google.com/uc?id={file_id}"

    raw_data = load_and_process_dataset(file_url)

    print(raw_data.head(10))  # выводим на экран первые 10 строк для проверки
    print(raw_data.info())  # выводим информацию о датафрейме после приведения типов

    raw_data.to_parquet(
        "data/processed/dataset.parquet", index=False
    )  # сохраняем в папку processed в формате parquet


if __name__ == "__main__":
    main()
