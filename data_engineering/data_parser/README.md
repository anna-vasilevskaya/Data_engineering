## Users CSV Parser

Parser that loads `data/raw/users.csv` created by the API reader, selects columns, removes duplicate `id`s, drops empty rows, parse ORCID (id for scientists) and writes `data/users_clean.csv`.

### Run
From the `data_engineering` project root:
```bash
poetry run python data_engineering/parse_example/data_parser.py
```
