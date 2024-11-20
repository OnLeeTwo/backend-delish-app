# Delish Backend App

This is a documentation about Delish App API. Created by Team 1 Revou Next for Milestone 1 Project. The members are:

- Owent Ovandy (Team Lead - BE)
- Jonathan Everald
- Zsuryanuti Perdana
- Mutiara Nafsyah
- Lili Pertiwi
- Tobias Halomoan (Team Lead - FE)
- Vito Yanufan
- Imam Hari
- A'id Fawwaz

## Start the API

1. Clone git using https or SSH

```bash
git clone git@github.com:username/repository.git
```

2. Install dependency

```bash
pipenv install
```

3. Adding enviroment for index

```
# for mac or linux
export FLASK_APP=index.py
# for windows
set FLASK_APP=index.py
```

4. Migrate the database

```
flask --app index.py db upgrade
```

5. start flask app

```
flask run --debug
```

## Documentation

Documentation for usage can be found [here](https://documenter.getpostman.com/view/34496185/2sAYBRHEkZ).
