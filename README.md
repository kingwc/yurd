# Yurd
## Run server:
uvicorn main:app --reload
## Set up python 3.11.1 and venv
cmd to working folder
python -m venv venv
^creates virtual enviorment
pip install FastAPI

## Pip install from requirements file
pip install -r requirements.txt

## Update requirements file with all imports
pip freeze > requirements.txt
