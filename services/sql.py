import os
from typing import Annotated
from datetime import date, datetime, timezone
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
# from azure.identity import DefaultAzureCredential
from sqlalchemy.pool import QueuePool
from sqlalchemy import func
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from sqlalchemy.exc import OperationalError

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
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    user_id: int | None = None  # GUID?
    user: str
    date: date
    activity: str

class UserRecord(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True) # GUID
    last_modified: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    user: str
    phone_num: int
    date_joined: date
    preferences: str     # make a long string

    
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

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(OperationalError)
)
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
    
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(OperationalError)
)
async def get_completion_records_for_user(user: str):
    with Session(engine) as session:
        statement = (
            select(CompletionRecord)
            .where(CompletionRecord.user == user)
        )
        results = session.exec(statement)
        return results.all()
    
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(OperationalError)
)
async def get_activities_for_user(user: str) -> str:
    with Session(engine) as session:
        statement = (
            select(CompletionRecord.activity)
            .where(CompletionRecord.user == user)
            .distinct()
        )
        results = session.exec(statement).all()

        activities = [r for r in results]

        return ", ".join(activities)
    
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(OperationalError)
)
async def count_completion_records_for_user_for_activity(user: str, activity: str) -> int:
    with Session(engine) as session:
        statement = (
            select(func.count())
            .select_from(CompletionRecord)
            .where(CompletionRecord.user == user)
            .where(CompletionRecord.activity == activity)
        )
        result = session.exec(statement).one()
        return int(result)

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(OperationalError)
)
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

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(OperationalError)
)
async def count_completion_records_for_user_for_activity_for_month(user: str, activity: str) -> int:
    with Session(engine) as session:
        now = date.today()
        first_of_month = date(now.year, now.month, 1)

        statement = (
            select(func.count())
            .select_from(CompletionRecord)
            .where(CompletionRecord.user == user)
            .where(CompletionRecord.activity == activity)
            .where(CompletionRecord.date >= first_of_month)
        )
        result = session.exec(statement).one()
        return int(result)