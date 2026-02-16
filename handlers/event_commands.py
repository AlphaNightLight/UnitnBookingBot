"""!
@file event_commands.py
@brief Handlers that manipulate the events and associated slots.

This file contains the implementation of the Telegram Bot Handlers that manage
the lifecycle of events and slots associated to them. They are triggered by the
following commands: <code>/publish</code>, <code>/changedes</code>, <code>/newslot</code>
<code>/deleteslot</code>, <code>/deleteevent</code>, <code>/myevents</code>.
"""

from dotenv import load_dotenv
import os, re

# Load environment variables
load_dotenv()
db = os.getenv("DB_PATH")
# Check of db existence is done in bot_main.py

# In case of db error not detected by bot_main.py, like "no such table: users",
# uncomment the following to check the working directory:
# print(os.getcwd())

# In case it's not the root directory,
# change it to the root folder with the following:
# os.chdir("path_to_root")



from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from utils.db_read import get_fairs, get_user_from_id, get_fair_from_id
from utils.db_read import get_event_from_id, get_event_name, get_events_given_owner
from utils.db_read import get_slot_from_id, get_slots_given_event

from utils.db_write import insert_user, insert_event, create_slot_str
from utils.db_write import update_event_description, delete_slot, delete_event





# publish - INIT
async def ask_event_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief INIT state for /publish
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    Conversation initializer for the <code>/publish</code> command.

    This function asks the user the name of their event, then goes to STATE 0
    """
    response = "Please, type the name of your event"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    return 0

# publish - STATE 0
async def ask_event_fair(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief STATE 0 for /publish
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    STATE 0 for the <code>/publish</code> command.

    This function lists to the user the fairs as an inline keyboard,
    then goes to STATE 1
    """
    fair_list = get_fairs(db)

    if not fair_list: # If fair_list is an empty list
        await update.message.reply_text("No fairs registered yet, operation cancelled.")
        return ConversationHandler.END

    keyboard = []
    for fair_item in fair_list:
        callback_data = "fair_id:" + str(fair_item[0]) + ":name:" + update.message.text
        keyboard.append([InlineKeyboardButton(fair_item[1], callback_data=callback_data)])
    keyboard.append([InlineKeyboardButton("/cancel", callback_data="cancel")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please select a fair:", reply_markup=reply_markup)

    return 1

# publish - STATE 1
async def log_event_creation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief STATE 1 for /publish
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    STATE 1 for the <code>/publish</code> command.

    Expected callback pattern (as RegEx): <code>^fair_id:[0-9]*:name:</code>

    This function creates an event and logs its information,
    then terminates the conversation.
    """
    query = update.callback_query
    await query.answer()

    callback_data = query.data[8:]  # [8:] removes "fair_id:" prefix
    column_position = callback_data.find(":")
    fair_id = int(callback_data[:column_position])
    event_name = callback_data[column_position + 6:]  # +6 removes ":name:" infix
    fair_name, _ = get_fair_from_id(db, fair_id)

    user_id = update.effective_chat.id
    user_name = update.effective_chat.first_name + " " + update.effective_chat.last_name
    user_username = "@" + update.effective_chat.username

    insert_user(db, user_id, user_name, user_username)
    insert_event(db,fair_id,user_id,event_name,"")

    response = "Event created successfully!\n\nDetails\n"
    response += "Event: " + event_name + "\n"
    response += "Fair: " + fair_name + "\n"
    response += "Owner: " + user_name
    await query.edit_message_text(response)

    return ConversationHandler.END





# changedes - INIT
async def ask_event_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief INIT state for /changedes
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    Conversation initializer for the <code>/changedes</code> command.

    This function asks the user the new description of their event, then goes to STATE 0
    """
    response = "Please, type the description of your event"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    return 0

# changedes - STATE 0
async def select_user_event_after_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief STATE 0 for /changedes and /newslot
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    STATE 0 for <code>/changedes</code> and <code>/newslot</code> commands.

    This function lists to the user their own events as an inline keyboard,
    then goes to STATE 1
    """
    user_id = update.effective_chat.id
    event_list = get_events_given_owner(db, user_id)

    if not event_list: # If event_list is an empty list
        await update.message.reply_text("You have no events yet, operation cancelled.")
        return ConversationHandler.END

    keyboard = []
    for event_item in event_list:
        callback_data = "event_id:" + str(event_item[0]) + ":des:" + update.message.text
        keyboard.append([InlineKeyboardButton(event_item[3], callback_data=callback_data)])
    keyboard.append([InlineKeyboardButton("/cancel", callback_data="cancel")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please select an event of yours:", reply_markup=reply_markup)

    return 1

# changedes - STATE 1
async def log_description_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief STATE 1 for /changedes
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    STATE 1 for the <code>/changedes</code> command.

    Expected callback pattern (as RegEx): <code>^event_id:[0-9]*:des:</code>

    This function changes an event description and logs its information,
    then terminates the conversation.
    """
    query = update.callback_query
    await query.answer()

    callback_data = query.data[9:] # [9:] removes "event_id:" prefix
    column_position = callback_data.find(":")
    event_id = int(callback_data[:column_position])
    event_description = callback_data[column_position + 5:]  # +6 removes ":des:" infix
    user_id = update.effective_chat.id
    event_name = get_event_name(db,event_id)
    user_name, _ = get_user_from_id(db,user_id)

    update_event_description(db,event_id,event_description)

    response = "Description updated successfully!\n\nDetails\n"
    response += "Event: " + event_name + "\n"
    response += "Description: " + event_description + "\n"
    response += "Owner: " + user_name
    await query.edit_message_text(response)

    return ConversationHandler.END





# newslot - INIT
async def ask_event_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief INIT state for /newslot
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    Conversation initializer for the <code>/newslot</code> command.

    This function asks the user an event time for the slot, then goes to STATE 0
    """
    response = "Please, type the time of your event, in the following format:\n\n"
    response += "YYYY-MM-DD HH:MM:SS\nYYYY-MM-DD HH:MM:SS\n\n"
    response += "Where first row is starting time and second row is end time."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    return 0

# newslot - STATE 0
# It's again select_user_event_after_text

# newslot - STATE 1
async def log_slot_creation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief STATE 1 for /newslot
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    STATE 1 for the <code>/newslot</code> command.

    Expected callback pattern (as RegEx): <code>^event_id:[0-9]*:des:</code>

    This function creates a slot and logs its information,
    then terminates the conversation.
    """
    query = update.callback_query
    await query.answer()

    callback_data = query.data[9:] # [9:] removes "event_id:" prefix
    column_position = callback_data.find(":")
    event_id = int(callback_data[:column_position])
    slot_times = callback_data[column_position + 5:]  # +6 removes ":des:" infix

    pattern = re.compile(
        "^" + "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]" + " "
        "[0-9][0-9]:[0-9][0-9]:[0-9][0-9]" +
        "\n" +
        "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]" +
        " " + "[0-9][0-9]:[0-9][0-9]:[0-9][0-9]" + "$"
    )
    if pattern.match(slot_times):
        start_time = slot_times[:19]
        end_time = slot_times[20:]
        user_id = update.effective_chat.id
        event_name = get_event_name(db, event_id)
        user_name, _ = get_user_from_id(db, user_id)

        create_slot_str(db,event_id,start_time,end_time)

        response = "Slot created successfully!\n\nDetails\n"
        response += "Event: " + event_name + "\n"
        response += "Start time: " + start_time + "\n"
        response += "End time: " + end_time + "\n"
        response += "Owner: " + user_name
    else:
        response = "The provided date doesn't mach the format, operation cancelled."

    await query.edit_message_text(response)

    return ConversationHandler.END





# deleteslot - INIT
async def select_user_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief INIT state for /deleteslot, /deleteevent and /myevents
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    Conversation initializer for <code>/deleteslot</code>, <code>/deleteevent</code>
    and <code>/myevents</code> commands.

    This function lists to the user their own events as an inline keyboard,
    then goes to STATE 0
    """
    user_id = update.effective_chat.id
    event_list = get_events_given_owner(db, user_id)

    if not event_list:  # If event_list is an empty list
        await update.message.reply_text("You have no events yet, operation cancelled.")
        return ConversationHandler.END

    keyboard = []
    for event_item in event_list:
        callback_data = "event_id:" + str(event_item[0])
        keyboard.append([InlineKeyboardButton(event_item[3], callback_data=callback_data)])
    keyboard.append([InlineKeyboardButton("/cancel", callback_data="cancel")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please select an event of yours:", reply_markup=reply_markup)

    return 0

# deleteslot - STATE 0
async def select_slot_for_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief STATE 0 for /deleteslot
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    STATE 0 for the <code>/deleteslot</code> command.

    Expected callback pattern (as RegEx): <code>^event_id:[0-9]*$</code>

    This function lists to the user the slots of an event of their own as an inline keyboard,
    then goes to STATE 1
    """
    query = update.callback_query
    await query.answer()

    event_id = int(query.data[9:])  # [9:] removes "event_id:" prefix
    event_name = get_event_name(db, event_id)
    slot_list = get_slots_given_event(db, event_id)

    if not slot_list: # If slot_list is an empty list
        await query.edit_message_text("You have currently no slots in this event.")
        return ConversationHandler.END

    keyboard = []
    for slot_item in slot_list:
        callback_data = "slot_id:" + str(slot_item[0])
        response = slot_item[2] + " - " + slot_item[3]
        keyboard.append([InlineKeyboardButton(response, callback_data=callback_data)])
    keyboard.append([InlineKeyboardButton("/cancel", callback_data="cancel")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Which slot do you want to delete for " + event_name + "?", reply_markup=reply_markup)

    return 1

# deleteslot - STATE 1
async def confirm_slot_deleting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief STATE 1 for /deleteslot
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    STATE 1 for the <code>/deleteslot</code> command.

    Expected callback pattern (as RegEx): <code>^slot_id:[0-9]*$</code>

    This function asks the user to confirm they want to delete the selected slot,
    through an inline keyboard, then goes to STATE 2
    """
    query = update.callback_query
    await query.answer()

    slot_id = int(query.data[8:]) # [8:] removes "slot_id:" prefix
    event_id, _, start_time, end_time = get_slot_from_id(db, slot_id)
    event_name = get_event_name(db, event_id)

    callback_data = "slot_id:" + str(slot_id)
    keyboard = [
        [InlineKeyboardButton("Delete slot", callback_data=callback_data)],
        [InlineKeyboardButton("/cancel", callback_data="cancel")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    response = "Are you sure you want to delete:\n"
    response += event_name + "\n"
    response += start_time + " -\n" + end_time + "?"
    await query.edit_message_text(response, reply_markup=reply_markup)

    return 2

# deleteslot - STATE 2
async def log_slot_deleting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief STATE 2 for /deleteslot
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    STATE 2 for the <code>/deleteslot</code> command.

    Expected callback pattern (as RegEx): <code>^slot_id:[0-9]*$</code>

    This function deletes a slot and logs the information it had,
    then terminates the conversation.
    """
    query = update.callback_query
    await query.answer()

    slot_id = int(query.data[8:]) # [8:] removes "slot_id:" prefix
    event_id, _, start_time, end_time = get_slot_from_id(db, slot_id)
    event_name = get_event_name(db, event_id)

    delete_slot(db, slot_id)

    response = "Slot deleted successfully!\n\nDetails\n"
    response += "Event: " + event_name + "\n"
    response += "Start time: " + start_time + "\n"
    response += "End time: " + end_time + "\n"
    response += "This slot is no more present in the database"
    await query.edit_message_text(response)

    return ConversationHandler.END





# deleteevent - INIT
# It's again select_user_event

# deleteevent - STATE 0
async def confirm_event_deleting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief STATE 0 for /deleteevent
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    STATE 0 for the <code>/deleteevent</code> command.

    Expected callback pattern (as RegEx): <code>^event_id:[0-9]*$</code>

    This function asks the user to confirm they want to delete the selected event with
    the associated slots, through an inline keyboard, then goes to STATE 1
    """
    query = update.callback_query
    await query.answer()

    event_id = int(query.data[9:])  # [9:] removes "event_id:" prefix
    event_name = get_event_name(db, event_id)

    callback_data = "event_id:" + str(event_id)
    keyboard = [
        [InlineKeyboardButton("Delete event", callback_data=callback_data)],
        [InlineKeyboardButton("/cancel", callback_data="cancel")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    response = "Are you sure you want to delete:\n"
    response += event_name + "?\n"
    response += "All the related slots will be deleted as well"
    await query.edit_message_text(response, reply_markup=reply_markup)

    return 1

# deleteevent - STATE 1
async def log_event_deleting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief STATE 1 for /deleteevent
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    STATE 1 for the <code>/deleteevent</code> command.

    Expected callback pattern (as RegEx): <code>^event_id:[0-9]*$</code>

    This function deletes an event and the associated slots, then logs the information
    it had and terminates the conversation.
    """
    query = update.callback_query
    await query.answer()

    event_id = int(query.data[9:])  # [9:] removes "event_id:" prefix
    event_name = get_event_name(db, event_id)

    delete_event(db, event_id, True)

    response = "Event deleted successfully!\n\nDetails\n"
    response += "Event: " + event_name + "\n"
    response += "This event is no more present in the database"
    await query.edit_message_text(response)

    return ConversationHandler.END





# myevents - INIT
# It's again select_user_event

# myevents - STATE 0
async def show_event_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief STATE 0 for /myevents
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    STATE 0 for the <code>/myevents</code> command.

    Expected callback pattern (as RegEx): <code>^event_id:[0-9]*$</code>

    This function logs the information of an event and all the slots associated
    to it, including the users that booked such slots, then terminates the conversation.
    """
    query = update.callback_query
    await query.answer()

    event_id = int(query.data[9:])  # [9:] removes "event_id:" prefix
    _, owner_id, event_name, event_description = get_event_from_id(db, event_id)
    owner_name, owner_username = get_user_from_id(db,owner_id)
    slot_list = get_slots_given_event(db, event_id)

    response = "Event Details"
    response += "\n\nName: " + event_name
    response += "\n\nDescription: " + event_description
    response += "\n\nOwner: " + owner_name
    response += "\nOwner Contact: " + owner_username

    if not slot_list:  # If slot_list is an empty list
        response += "\n\nYou have currently no slots in this event."
    else:
        response += "\n\nSlot List:"

    for slot_item in slot_list:
        response += "\n\n" + slot_item[2]
        response += "\n" + slot_item[3]
        if slot_item[1] is None:
            response += "\nSlot Available"
        else:
            response += "\nSlot booked by: " + slot_item[4]
            response += "\nContact: " + slot_item[5]

    await query.edit_message_text(response)
    return ConversationHandler.END
