import os
from typing import Annotated
from datetime import date, datetime, timezone
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
# from azure.identity import DefaultAzureCredential
from sqlalchemy.pool import QueuePool

# Get environment variables for service principal
tenant_id = os.environ.get("AZURE_TENANT_ID")
client_id = os.environ.get("AZURE_CLIENT_ID")
client_secret = os.environ.get("AZURE_CLIENT_SECRET")
server_name = os.environ.get("AZURE_SQL_SERVER_NAME")
database_name = os.environ.get("AZURE_SQLDB_NAME")

# Initialize service principal credential
# credential = DefaultAzureCredential()
# #     tenant_id=tenant_id,
# #     client_id=client_id,
# #     client_secret=client_secret
# # )

# # Get access token for Azure SQL Database
# token = credential.get_token("https://database.windows.net/.default")

# Build connection string with Entra ID
# Linux installation instruction for ODBC Driver https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver17&tabs=ubuntu18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline#microsoft-odbc-18
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

# class UserProgress(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     user: str
#     week_total: int
#     activity: str

# AutoGenerateID 
class CompletionRecord(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    create_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    user: str
    date: date
    activity: str
    

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def remove_all_tables():
    # This deletes EVERY table defined in your SQLModel metadata
    SQLModel.metadata.drop_all(engine)

# TODO: Fix session management and dependency injection
# def get_session():
#     with Session(engine) as session:
#         yield session


# SessionDep = Annotated[Session, Depends(get_session)]

async def create_completion_record(user: str, activity: str):
    completion_record = CompletionRecord(
        user = user,
        date = date.today(),
        activity = activity
    )
    
    # Check this will get Session properly
    with Session(engine) as session:
        session.add(completion_record)
        session.commit()

        return None 
    
async def get_completion_records_for_user(user: str):
    with Session(engine) as session:
        statement = (
            select(CompletionRecord)
            .where(CompletionRecord.user == user)
        )
        results = session.exec(statement)
        return results.all()

async def get_completion_records_for_user_for_this_month(user: str):
    with Session(engine) as session:
    # NEED an and statement to get all records for this month so far
        now = date.today()
        first_of_month = date(now.year, now.month, 1)


        statement = (
            select(CompletionRecord)
            .where(CompletionRecord.user == user)
            .where(CompletionRecord.date >= first_of_month)
        )
        results = session.exec(statement)
        return results.all()
