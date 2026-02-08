import asyncio
from langchain.tools import tool
from services.sql import count_completion_records_for_user_for_activity, count_completion_records_for_user_for_activity_for_month, create_completion_record, get_activities_for_user, get_completion_records_for_user, get_completion_records_for_user_for_this_month

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

@tool('count_activity_for_user_this_month')
def count_activity_for_user_this_month(user: str, activity: str) -> int:
    """
    This counts the number of times a user has done an activity this month.

    Args:
        user (str): The user to count for
        activity (str): The activity to count

    Returns:
        int: The count of that activity for that user this month
    """
    print(f"Counting activity for user this month...")
    result = asyncio.run(count_completion_records_for_user_for_activity_for_month(user, activity))
    print(f"Counted {result} activities for user {user} this month.")
    return result