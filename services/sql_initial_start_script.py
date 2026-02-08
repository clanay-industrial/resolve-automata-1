import asyncio
from dotenv  import load_dotenv
load_dotenv()

import sql
from sql import create_db_and_tables, remove_all_tables, create_completion_record, get_completion_records_for_user, get_completion_records_for_user_for_this_month

with sql.engine.connect() as conn:
    print("Connected OK")

# print("Removing database and tables...")
remove_all_tables()

print("Creating database and tables...")
create_db_and_tables()

# print("Testing adding to DB...")
# asyncio.run(create_completion_record("test_user", "painting"))

# # result = asyncio.run(get_completion_records_for_user("test_user"))
# # for r in result:
# #     print(r)
# #     print(r.date.month)

# # result2 = asyncio.run(get_completion_records_for_user_for_this_month("test_user"))  
# # for r in result2:
# #     print(r)

# count = asyncio.run(sql.count_completion_records_for_user_for_activity("test_user2", "exercise"))
# print(f"Count for test_user exercise: {count}")

# get_activities = asyncio.run(sql.get_activities_for_user("test_user2"))
# print(f"Activities for test_user: {get_activities}")