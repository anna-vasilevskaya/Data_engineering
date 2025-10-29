# Connect to PostgreSQL and insert data

Set environment variables:
copy from .env_example to .env and set real values

Other ways:

Windows Command Prompt
```cmd
set DB_HOST=1.2.3.4
set DB_PORT=1234
set DB_NAME=db
set DB_USER=user
set DB_PASSWORD=password
set TABLE_NAME=table
```

Linux/macOS
```bash
export DB_HOST="1.2.3.4"
export DB_PORT="1234"
export DB_NAME="db"
export DB_USER="user"
export DB_PASSWORD="password"
export TABLE_NAME="table"
```

## Execute

1. Dependencies:
```bash
make requirements
poetry env activate
poetry install
```

2. Process data (ETL - no DB load):
```bash
python -m data_engineering.etl.main --source data_engineering/data/raw/dataset.csv --no-db
```

3. Upload to database (ETL - max 100 rows):
```bash
python -m data_engineering.etl.main --source data_engineering/data/raw/dataset.csv --table-name %TABLE_NAME%
```

![Write to DB](../images/write_to_db.jpg)

![PostgreSQL results](../images/postgresql_results.jpg)

![Test results](../images/test_db.jpg)

