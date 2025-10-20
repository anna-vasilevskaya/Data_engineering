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
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- Readme files
│
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         data_engineering and configuration for tools like black
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── data_parser 
│   │
│   ├── data_parser.py  <- Parser that loads `api_example/data/raw/users.csv` created by the API reader, selects columns, removes duplicate `id`s, drops empty rows, parse ORCID (id for scientists)
│   │    
│   └── README.md
│
├── api_example 
│   │
│   ├── api_reader.py  <- Simple script fetches users from Open Science Framework
│   │    
│   ├── images_users
│   │ 
│   ├── README.md
│   │  
│   └── data           
│       ├── processed  <- users_clean.csv and users.parqet
│       └── raw        <- users.csv and users.parquet
│
└── data_engineering   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes data_engineering a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── data_loader.py          <- Scripts to download or generate data
    │
    ├── import_dataset.py
    │
    ├── load_from_kaggle.py
    │
    └── plots.py                <- Code to create visualizations
    │
    └── write_to_db.py          <- Write 100 rows from dataset to PostgreSQL  
```

--------
### Links to Readme files

#### Load dataset
 [DataLoader](data_engineering/docs/DataLoader.md)

#### API Reader Example
**API Source**
```
The Center for Open Science is a nonprofit organization that increases the openness, integrity, and reproducibility of scientific research by developing and maintaining the open source infrastructure OSF to support the entire research lifecycle.
```

Simple script fetches users from Open Science Framework
[README.md](data_engineering/api_example/README.md)

#### API Data Parser Example

Parser that created by the API reader, selects columns, removes duplicate `id`s, drops empty rows, parse ORCID (id for scientists) 

[README.md](data_engineering/data_parser/README.md)

### Link to EDA

[EDA](data_engineering/notebooks/EDA.ipynb)

### Working with PostgreSQL database

[Code - write_to_db.py](data_engineering/data_engineering/write_to_db.py)


[README - Database.md](data_engineering/docs/Database.md)
