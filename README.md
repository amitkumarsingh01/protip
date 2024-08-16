## POSTGRESQL QUERY

### Creating Table
```
CREATE TABLE protip (
    s_no SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    bought_price NUMERIC(10, 2) NOT NULL,
    current_price NUMERIC(10, 2) NOT NULL,
    units INTEGER NOT NULL,
    invested_amount NUMERIC(12, 2) GENERATED ALWAYS AS (bought_price * units) STORED,
    present_value NUMERIC(12, 2) GENERATED ALWAYS AS (current_price * units) STORED,
    profit_loss NUMERIC(12, 2) GENERATED ALWAYS AS (
        (current_price * units) - (bought_price * units)
    ) STORED,
    profit_loss_percent NUMERIC(5, 2) GENERATED ALWAYS AS (
        ((current_price * units) - (bought_price * units)) / (bought_price * units) * 100
    ) STORED,
    invested_date DATE NOT NULL
);
```

### Viewing Table
```
SELECT * FROM protip
```

## How to install it
#### Clone
```
git clone https://github.com/itheaks/protip.git
```
#### Moving to Directery 
```
cd protip
cd Assignment
```
#### Installing packages and virtal env
```
pip install virtualenv
virtaulenv venv
cd venv
cd Scripts
activate
pip install Flask psycopg2-binary
```
#### To run
```
python app.py
```

## Demo

It is in Demo Folder

https://drive.google.com/file/d/1SJRWbX-sdjwsQuIRsRso4sUTQHWO8N9_/view?usp=sharing

