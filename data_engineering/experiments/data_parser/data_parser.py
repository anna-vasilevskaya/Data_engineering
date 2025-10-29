import ast
from datetime import datetime
from typing import Any, List, Optional

import pandas as pd


def parse(value: Any) -> Any:
    """
    Парсит строковые значения, содержащие JSON-подобные структуры.
    
    Args:
        value (Any): Входное значение для парсинга
        
    Returns:
        Any: Распарсенное значение или оригинальное значение, если парсинг не удался
    """
    if isinstance(value, str):
        value = value.strip() # Удаляем лишние пробелы
        if (value.startswith("{") and value.endswith("}")) or (
            value.startswith("[") and value.endswith("]") 
        ):                                                      # Проверяем, является ли строка JSON-объектом или массивом
            try:
                return ast.literal_eval(value) # Безопасное преобразование строки в Python объект
            except Exception:
                return value  # В случае ошибки возвращаем оригинальное значение
    return value


def extract_orcid(social: Any) -> Optional[str]:
    """
    Извлекает ORCID идентификатор из поля social.
    
    ORCID - уникальный идентификатор исследователя.
    
    Args:
        social (Any): Данные социальных профилей пользователя
        
    Returns:
        Optional[str]: ORCID идентификатор или None, если не найден
    """
    parsed = parse(social) # Парсим поле social
    if isinstance(parsed, dict):
        orcid = parsed.get("orcid") # Извлекаем ORCID из словаря
        return str(orcid) if orcid else None
    return None


def parse_users(input_folder: str = "api_example/data/raw/", output_folder: str = "api_example/data/processed/") -> None:
    """
    Основная функция для очистки и обработки данных пользователей.
    
    Args:
        input_folder (str): Папка с исходными данными
        output_folder (str): Папка для сохранения обработанных данных
    """
    df = pd.read_csv(input_folder+"users.csv") # Загрузка данных из CSV файла

    columns = [
        "id",
        "full_name",
        "given_name",
        "middle_names",
        "family_name",
        "suffix",
        "date_registered",
        "active",
        "timezone",
        "locale",
        "social",
        "employment",
        "education",
    ] # Список желаемых колонок для сохранения
    existing_columns = [c for c in columns if c in df.columns]
    if existing_columns:
        df = df[existing_columns]  # Фильтруем только существующие колонки из желаемого списка

    # Чистка данных
    if "id" in df.columns:
        df = df.drop_duplicates(subset=["id"]).reset_index(drop=True) # Удаляем дубликаты по идентификатору пользователя
    df = df.dropna(how="all").reset_index(drop=True) # Удаляем строки, где все значения NaN

    df.to_csv(output_folder+"users_clean.csv", index=False) # CSV для читаемости
    df.to_parquet(output_folder+"users_clean.parquet", index=False) # Parquet для эффективности



if __name__ == "__main__": # Создает необходимые директории и запускает обработку данных.
    import os
    os.makedirs("api_example/data/raw", exist_ok=True) # Для исходных данных
    os.makedirs("api_example/data/processed", exist_ok=True) # Для обработанных данных
    parse_users() # Запуск основной функции обработки


