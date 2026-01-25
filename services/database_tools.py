import asyncio
from langchain.tools import tool
from services.sql import count_completion_records_for_user_for_activity, create_completion_record, get_activities_for_user, get_completion_records_for_user, get_completion_records_for_user_for_this_month

# in_memory_db = {}

@tool('search_database_for_user_activity')
def search_database_for_user_activity(user: str) -> int:
    """
    Search the database for all activities for a user.

    It returns the list of activities for that user.

    Args:
        user (str): The user to search for.

    Returns: 
        string: The list of activities for that user.
    """
    # global in_memory_db

    print(f"Searching database...")

    # in_memory_db.get(user)
    result = asyncio.run(get_activities_for_user(user))

    # if user not in in_memory_db:
    #     in_memory_db[user] = 0
    
    return result

@tool('log_activity_to_database')
def log_activity_to_database(user: str, activity: str) -> int: 
    """
    This adds one log to the database. Incrementing the score by one for that activity.

    It returns the current total for that activity.

    Args:
        user (str): The user to increment the database for
        activity (str): The activity to log

    Returns:
        int: The current total in the database
    """
    # global in_memory_db

    # in_memory_db.get(user)

    # if user not in in_memory_db:
    #     in_memory_db[user] = 0

    print(f"Adding to database...")
    asyncio.run(create_completion_record(user, activity))

    result = asyncio.run(count_completion_records_for_user_for_activity(user, activity))
    print(f"New total: {result}")
    return result