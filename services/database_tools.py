from langchain.tools import tool

in_memory_db = {}

@tool('search_database')
def search_database(user: str) -> int:
    """
    Search the database for relevant information.

    it returns the current total.

    Args:
        user (str): The user to search for.

    Returns: 
        int: The current total in the database
    """
    global in_memory_db

    print(f"Searching database...{in_memory_db}")

    in_memory_db.get(user)

    if user not in in_memory_db:
        in_memory_db[user] = 0
    
    return in_memory_db

@tool('log_to_database')
def log_to_database(user: str) -> int: 
    """
    This adds one log to the database. Incrementing the score by one.

    It returns the current total. 

    Args:
        user (str): The user to increment the database for

    Returns:
        int: The current total in the database
    """
    global in_memory_db

    in_memory_db.get(user)

    if user not in in_memory_db:
        in_memory_db[user] = 0

    print(f"Adding to database...{in_memory_db}")
    in_memory_db[user] += 1
    print(f"New total: {in_memory_db}")
    return in_memory_db
