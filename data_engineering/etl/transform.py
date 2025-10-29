from __future__ import annotations

import pandas as pd


def cast_schema(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Observation ID"] = df["Observation ID"].astype("uint16")
    df["Common Name"] = df["Common Name"].astype("category")
    df["Scientific Name"] = df["Scientific Name"].astype("category")
    df["Family"] = df["Family"].astype("category")
    df["Genus"] = df["Genus"].astype("category")
    df["Observed Length (m)"] = df["Observed Length (m)"].astype("float16")
    df["Observed Weight (kg)"] = df["Observed Weight (kg)"].astype("float16")
    df["Age Class"] = df["Age Class"].astype("category")
    df["Sex"] = df["Sex"].astype("category")
    df["Date of Observation"] = pd.to_datetime(
        df["Date of Observation"], format="%d-%m-%Y"
    )
    df["Country/Region"] = df["Country/Region"].astype("category")
    df["Habitat Type"] = df["Habitat Type"].astype("category")
    df["Conservation Status"] = df["Conservation Status"].astype("category")
    df["Observer Name"] = df["Observer Name"].astype("category")
    df["Notes"] = df["Notes"].astype("object")
    return df
