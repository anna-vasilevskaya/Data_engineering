## Open Science Framework Users API Reader

Simple script fetches users from API and saves them to `api_example/data/users.csv`.

### Prerequisites
- Python managed by Poetry
- Dependencies declared in the workspace `pyproject.toml` (uses `requests`, `tqdm`, `pandas`)

### Install
```bash
poetry install
```

### Run
From the `data_engineering` project root:
```bash
poetry run python data_engineering/api_example/api_reader.py
```

- Change page size or page count:
  - `load_osf_users(API_URL, max_pages=50, page_size=10)`
- If timeouts happen, decrease `page_size` or increase the request timeout.

### Image for command `users = load_osf_users(API_URL, max_pages=50, page_size=10)`
![Users info loader](/data_engineering/api_example/images_users/users_info.jpg)

### Image for command `print(df["full_name"].head(10))`
![List of columns](/data_engineering/api_example/images_users/users_head(10).jpg)

### Output
- CSV: `api_example/data/users.csv`

### Check dataset from "users.csv"
![Check dateset](/data_engineering/api_example/images_users/check_users_csv.jpg)

### Docs
- OSF Users List: https://developer.osf.io/#operation/users_list
- OSF Users Read: https://developer.osf.io/#operation/users_read
- Test: https://api.test.osf.io/v2/users/


