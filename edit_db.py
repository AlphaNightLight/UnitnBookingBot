from dotenv import load_dotenv
import os, sys

# Load environment variables
load_dotenv()
db = os.getenv("DB_PATH")

# Check environment variables existence
if db is None or db=="":
    sys.exit("Fatal error: database path not set. Insert it in your .env file.")
else:
    print("Database path loaded: " + db)



from utils.db_print import print_users_by_id, print_users_by_name, print_fairs, print_events, \
    print_events_with_fair, print_events_with_owner, print_event_slots
from utils.db_write import insert_user, insert_fair, insert_event, create_slot, assign_slot
from utils.db_write import update_user, update_fair, update_event, update_event_description, update_slot
from utils.db_write import delete_user, delete_fair, delete_event, delete_slot

from datetime import datetime





######################################
# Inspect the values in the database #
######################################

# print_users_by_id(db=db)
# print_users_by_name(db=db)
# print_fairs(db=db, description=False)

# print_events(db=db, description=False)
# print_events_with_fair(db=db)
# print_events_with_owner(db=db)
# print_event_slots(db=db, event_id=)





#####################################
# Insert new values in the database #
#####################################

# insert_user(db=db, user_id=, name=, username=)
# insert_fair(db=db, name=, description=)
# insert_event(db=db, fair_id=, owner_id=, name=, description=)

# start_time = datetime(year=, month=, day=, hour=, minute=, second=)
# end_time   = datetime(year=, month=, day=, hour=, minute=, second=)
# create_slot(db=db, event_id=, start_time=start_time, end_time=end_time)

# assign_slot(db=db, slot_id=, user_id=)





#####################################
# Modify the values in the database #
#####################################

# update_user(db=db, user_id=, name=, username=)
# update_fair(db=db, fair_id=, name=, description=)
# update_event(db=db, event_id=, fair_id=, owner_id=, name=, description=)
# update_event_description(db=db, event_id=, description=)

# start_time = datetime(year=, month=, day=, hour=, minute=, second=)
# end_time   = datetime(year=, month=, day=, hour=, minute=, second=)
# update_slot(db=db, slot_id=, event_id=, user_id=, start_time=start_time, end_time=end_time)





###################################
# Delete values from the database #
###################################

# delete_user(db=db, user_id=)
# delete_fair(db=db, fair_id=)
# delete_event(db=db, event_id=, delete_slots=True)
# delete_slot(db=db, slot_id=)
