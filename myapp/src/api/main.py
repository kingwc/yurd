import sys
from fastapi import FastAPI
from sqlalchemy import inspect
from src.db.models import account_model, event_model
from src.db.database_connection import engine
from src.api.accounts_controller import APIAccountsApp
from src.api.events_controller import APIEventsApp

account_model.Base.metadata.create_all(bind=engine)
event_model.Base.metadata.create_all(bind=engine)

inspector = inspect(engine)
schemas = inspector.get_schema_names()

for schema in schemas:
    print("schema: %s" % schema)
    for table_name in inspector.get_table_names(schema=schema):
        print("Table: %s" % table_name)


app = FastAPI()

app.mount("/accounts", APIAccountsApp)
app.mount("/events", APIEventsApp)