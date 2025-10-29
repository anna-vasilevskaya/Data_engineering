# Data Driven Engineering

## Dataset
https://www.kaggle.com/datasets/zadafiyabhrami/global-crocodile-species-dataset

## data_engineering

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

analysis of dataset

## Project Organization

```
├── README.md                       <- Top-level README
├── data_engineering/               <- Main project directory
│   ├── pyproject.toml              <- Project config (dependencies, tools)
│   ├── poetry.lock
│   ├── Makefile
│   ├── docs/                       <- Project docs
│   │   ├── DataLoader.md
│   │   └── Database.md
│   ├── notebooks/                  <- Jupyter notebooks
│   │   ├── EDA.ipynb
│   │   └── README.md
│   ├── images/                     <- Screenshots/figures
│   ├── reports/
│   │   └── figures/
│   ├── tests/
│   │   ├── test_db.py
│   │   └── select.sql
│   ├── data/                       <- Runtime data (created by code)
│   │   ├── raw/
│   │   └── processed/
│   ├── etl/                        <- ETL package (production)
│   │   ├── __init__.py
│   │   ├── extract.py
│   │   ├── transform.py
│   │   ├── load.py
│   │   ├── utils.py
│   │   └── main.py
│   └── experiments/                <- Legacy/examples (kept for reference)
│       ├── api_example/
│       │   ├── api_reader.py
│       │   ├── data/{raw,processed}
│       │   ├── images_users/
│       │   └── README.md
│       ├── data_parser/
│       │   ├── data_parser.py
│       │   └── README.md
│       └── data_engineering/
│           ├── config.py
│           ├── data_loader.py
│           ├── import_dataset.py
│           ├── load_from_kaggle.py
│           ├── plots.py
│           └── write_to_db.py
```

--------
### Links to Readme files

#### Load dataset
 [DataLoader](data_engineering/docs/DataLoader.md)

### Link to EDA

[EDA](data_engineering/notebooks/EDA.ipynb)

[NBViewer](https://nbviewer.org/github/anna-vasilevskaya/Data_engineering/blob/main/data_engineering/notebooks/EDA.ipynb)

[MyBinder](https://mybinder.org/v2/gh/anna-vasilevskaya/Data_engineering/f579a7e7859221552ce0da9a68cf84e1d24ac0aa?urlpath=lab%2Ftree%2Fdata_engineering%2Fnotebooks%2FEDA.ipynb)

[Screenshots of dynamic visualization](data_engineering/notebooks/README.md)

### Working with PostgreSQL database

[Code - write_to_db.py](data_engineering/experiments/data_engineering/write_to_db.py)


[README - Database.md](data_engineering/docs/Database.md)

#### API Reader Example
**API Source**
```
The Center for Open Science is a nonprofit organization that increases the openness, integrity, and reproducibility of scientific research by developing and maintaining the open source infrastructure OSF to support the entire research lifecycle.
```

Simple script fetches users from Open Science Framework
[README.md](data_engineering/experiments/api_example/README.md)

#### API Data Parser Example

Parser that created by the API reader, selects columns, removes duplicate `id`s, drops empty rows, parse ORCID (id for scientists) 

[README.md](data_engineering/experiments/data_parser/README.md)

## ETL package

```
data_engineering/etl/
├── __init__.py        # package metadata
├── extract.py         # read raw source (CSV/Parquet/URL), validate, save CSV to data/raw
├── transform.py       # type casting and basic normalization
├── load.py            # write parquet to data/processed and load <=100 rows into DB
├── utils.py           # filesystem helpers
└── main.py            # CLI orchestrator
```

- Data directories: `data_engineering/data/raw` and `data_engineering/data/processed` are created at runtime.
- DB connection uses environment variables: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`.

### Run

Minimal run (no DB load):

```bash
python -m data_engineering.etl.main --source data_engineering/data/raw/dataset.csv --no-db
```

Load into a DB table (max 100 rows):

```bash
python -m data_engineering.etl.main --source data_engineering/data/raw/dataset.csv --table-name vasilevskaia
```

The pipeline will:
- Extract: read the source and save `data_engineering/data/raw/dataset.csv`.
- Transform: cast schema (dtypes, dates).
- Load: write `data_engineering/data/processed/dataset.parquet` and optionally insert up to 100 rows into the target table.

