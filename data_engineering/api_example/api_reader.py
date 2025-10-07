import requests
from tqdm import tqdm
import pandas as pd

API_URL = "https://api.osf.io/v2/users/" # Базовый URL для API Open Science Framework
# Заголовки HTTP-запроса, указывающие на ожидаемый формат данных (JSON API)
HEADERS = {
    "Accept": "application/vnd.api+json",  # формат JSON API
    "Content-Type": "application/json",    # Тип содержимого
}


def load_osf_users(api_url: str, max_pages: int = 50, page_size: int = 10) -> list:
    """
    Загружает данные пользователей из OSF API "блоками".
    
    Args:
        api_url (str): URL API endpoint для пользователей
        max_pages (int): Максимальное количество страниц для загрузки (по умолчанию 50)
        page_size (int): Количество записей на странице (по умолчанию 10)
    
    Returns:
        list: Список словарей с данными пользователей
    """
    collected_users = []  # Список для хранения всех собранных данных пользователей
    next_url = api_url    # Начинаем с основного URL
    params = {"page[size]": page_size}  # Параметры для первой страницы

    for _ in tqdm(range(max_pages), desc="Fetching OSF users (pages)"): # Цикл по страницам со шкалой прогресса
        
        if not next_url:  # Прерываем цикл если нет следующей страницы
            break

        response = requests.get(next_url, headers=HEADERS, params=params, timeout=30) # Выполняем HTTP GET запрос к API        
    
        if response.status_code != 200: # Проверяем успешность запроса
            print(
                f"WARNING! Status code for URL {next_url} is {response.status_code}."
            )
            break

        payload = response.json() # JSON ответ
        data_items = payload.get("data", []) # Извлекаем массив данных из ответа
        
        # Обрабатываем каждую запись пользователя на текущей странице
        for item in data_items:
            attributes = item.get("attributes", {}) # Создаем запись с ID и всеми атрибутами пользователя
            record = {"id": item.get("id", None)}  # Основной идентификатор
            record.update(attributes)  # Добавляем все атрибуты пользователя
            collected_users.append(record)

        links = payload.get("links", {}) # Получаем ссылку на следующую страницу из метаданных ответа
        next_url = links.get("next")  # URL следующей страницы или None если последняя
        params = None  # Очищаем параметры, так как next_url уже содержит все необходимое

        if not data_items and not next_url: # Получаем ссылку на следующую страницу из метаданных ответа
            break

    return collected_users


# Основной блок выполнения
users = load_osf_users(API_URL, max_pages=50, page_size=10) # Загружаем данные пользователей из API

# Обрабатываем загруженные данные
if users:
    df = pd.DataFrame(users) # Конвертируем список словарей в DataFrame pandas
    
    # Сохраняем данные в разных форматах:
    df.to_csv("api_example/data/raw/users.csv", index=False)        # CSV для читаемости
    df.to_parquet("api_example/data/raw/users.parquet", index=False) # Parquet для эффективности
    
    print(df.info()) # Выводим информацию о структуре данных

    if "full_name" in df.columns: # Показываем примеры данных - имена пользователей если есть столбец full_name
        print(df["full_name"].head(10))  # Первые 10 имен пользователей
    else:
        print(df.head(10)) # Альтернативно показываем первые 10 записей если нет столбца с именами
else:
    print("No users were fetched") # Сообщение если данные не были загружены