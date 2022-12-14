# Yurd
## Run server:
```uvicorn main:app --reload```
```py -m uvicorn src.main:app --reload (windows, from root)```
## Set up python 3.11.1 and venv
cd to root folder
```python -m venv venv```
```venv\Scripts\activate (windows)```
```source venv/bin/activate (linux)```

^creates and installs virtual enviorment
```pip install FastAPI```

## Pip install from requirements file
```pip install -r requirements.txt```

## Update requirements file with all imports
```pip freeze > requirements.txt```

## Run Tests Locally
```py -m pytest myapp/test (windows)```