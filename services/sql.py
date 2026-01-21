import os
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from azure.identity import DefaultAzureCredential
from sqlalchemy.pool import QueuePool

# Get environment variables for service principal
tenant_id = os.environ.get("AZURE_TENANT_ID")
client_id = os.environ.get("AZURE_CLIENT_ID")
client_secret = os.environ.get("AZURE_CLIENT_SECRET")
server_name = os.environ.get("AZURE_SQL_SERVER_NAME")
database_name = os.environ.get("AZURE_SQLDB_NAME")

# Initialize service principal credential
credential = DefaultAzureCredential()
#     tenant_id=tenant_id,
#     client_id=client_id,
#     client_secret=client_secret
# )

# Get access token for Azure SQL Database
token = credential.get_token("https://database.windows.net/.default")

# Build connection string with Entra ID
driver_name = '{ODBC Driver 18 for SQL Server}'
connection_string = (
    f'Driver={driver_name};'
    f'Server=tcp:{server_name}.database.windows.net,1433;'
    f'Database={database_name};'
    f'Encrypt=yes;'
    f'TrustServerCertificate=no;'
    f'Connection Timeout=30;'
    f'Authentication=ActiveDirectoryServicePrincipal;'
    f'UID={client_id};'
    f'PWD={client_secret}'
)

# Create engine with connection pooling
engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={connection_string}",
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Validates connection before using
    echo=False
)

class UserProgress(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user: str
    week_total: int
    activity: str

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

create_db_and_tables()
