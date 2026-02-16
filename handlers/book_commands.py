"""!
@file book_commands.py
@brief Handlers that manipulate the bookings.

This file contains the implementation of the Telegram Bot Handlers that manage
the lifecycle of the bookings associated to them, as well as the handlers that
retrieve information about all events and fairs. They are triggered by the
following commands: <code>/fairs</code>, <code>/events</code>, <code>/whoami</code>
<code>/book</code>, <code>/unbook</code>, <code>/mybookings</code>.
"""

from dotenv import load_dotenv
import os

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
from utils.db_read import get_event_from_id, get_event_name, get_events_given_fair
from utils.db_read import get_slot_from_id, get_slot_dates, get_slot_times, \
    get_slots_given_user, count_slots

from utils.db_write import insert_user, assign_slot





# fairs - INIT
async def select_fair(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief INIT state for /fairs, /events and /book
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    Conversation initializer for <code>/fairs</code>, <code>/events</code>
    and <code>/book</code> commands.

    This function lists to the user all the fairs as an inline keyboard,
    then goes to STATE 0
    """
    fair_list = get_fairs(db)

    if not fair_list: # If fair_list is an empty list
        await update.message.reply_text("No fairs registered yet.")
        return ConversationHandler.END

    keyboard = []
    for fair_item in fair_list:
        callback_data = "fair_id:" + str(fair_item[0])
        keyboard.append([InlineKeyboardButton(fair_item[1], callback_data=callback_data)])
    keyboard.append([InlineKeyboardButton("/cancel", callback_data="cancel")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please select a fair:", reply_markup=reply_markup)

    return 0

# fairs - STATE 0
async def show_fair_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief STATE 0 for /fairs
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    STATE 0 for the <code>/fairs</code> command.

    Expected callback pattern (as RegEx): <code>^fair_id:[0-9]*$</code>

    This function logs to the user the information on the selected fair,
    then terminates the conversation.
    """
    query = update.callback_query
    await query.answer()

    fair_id = int(query.data[8:]) # [8:] removes "fair_id:" prefix
    fair_name, fair_description = get_fair_from_id(db, fair_id)
    response = fair_name + ":\n\n" + fair_description

    await query.edit_message_text(text=response)
    return ConversationHandler.END





# events - INIT
# It's again select_fair

# events - STATE 0
async def select_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief STATE 0 for /events and /book
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    STATE 0 for <code>/events</code> and <code>/book</code> commands.

    Expected callback pattern (as RegEx): <code>^fair_id:[0-9]*$</code>

    This function lists to the user the events associated to the selected fair,
    as an inline keyboard, then goes to STATE 1
    """
    query = update.callback_query
    await query.answer()

    fair_id = int(query.data[8:])  # [8:] removes "fair_id:" prefix
    event_list = get_events_given_fair(db, fair_id)

    if not event_list: # If fair_list is an empty list
        await query.edit_message_text("No events registered in this fair yet.")
        return ConversationHandler.END

    keyboard = []
    for event_item in event_list:
        callback_data = "event_id:" + str(event_item[0])
        keyboard.append([InlineKeyboardButton(event_item[3], callback_data=callback_data)])
    keyboard.append([InlineKeyboardButton("/cancel", callback_data="cancel")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Please select an event:", reply_markup=reply_markup)

    return 1

# events - STATE 1
async def show_event_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief STATE 1 for /events
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    STATE 1 for the <code>/events</code> command.

    Expected callback pattern (as RegEx): <code>^event_id:[0-9]*$</code>

    This function logs to the user the information on the selected event,
    then terminates the conversation.
    """
    query = update.callback_query
    await query.answer()

    event_id = int(query.data[9:]) # # [9:] removes "event_id:" prefix
    _, owner_id, event_name, event_description = get_event_from_id(db, event_id)
    owner_name, owner_username = get_user_from_id(db, owner_id)
    free_slots, all_slots = count_slots(db, event_id)

    response = "Event Details"
    response += "\n\nName: " + event_name
    response += "\n\nDescription: " + event_description

    if all_slots == 0:
        response += "\n\nNo slot available yet."
    elif free_slots == 0:
        response += "\n\nAll the " + str(all_slots) + " slots are booked."
    else:
        response += "\n\nAvailable Slots: " + str(free_slots) + " out of " + str(all_slots)

    response += "\n\nOwner: " + owner_name
    response += "\nOwner Contact: " + owner_username
    await query.edit_message_text(text=response)

    return ConversationHandler.END





# whoami - Command Handler
async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """! @brief Command handler for /whoami
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return None

    Command handler for the <code>/whoami</code> command.

    This function logs all the information associated to the current user.
    """
    user_id = update.effective_chat.id
    name, username = get_user_from_id(db, user_id)

    if name is None:
        response = "This chat is not associated to metadata yet.\n"
        response += "Your ID is: " + str(user_id)
    else:
        response = "This chat is associated to the following metadata:\n\n"
        response += "User ID: " + str(user_id) + "\n"
        response += "Name: " + name + "\n"
        response += "Username: " + username
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    return





# book - INIT
# It's again select_fair

# book - STATE 0
# It's again select_event

# book - STATE 1
async def select_slot_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief STATE 1 for /book
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    STATE 1 for the <code>/book</code> command.

    Expected callback pattern (as RegEx): <code>^event_id:[0-9]*$</code>

    This function lists to the user the dates available for the slots
    associated to a given event, as an inline keyboard, then goes to STATE 2
    """
    query = update.callback_query
    await query.answer()

    event_id = int(query.data[9:]) # [9:] removes "event_id:" prefix
    event_name = get_event_name(db, event_id)
    free_slots, all_slots = count_slots(db, event_id)

    if all_slots == 0:
        await query.edit_message_text("No slot available yet.")
        return ConversationHandler.END
    elif free_slots == 0:
        await query.edit_message_text("All the " + str(all_slots) + " slots are booked.")
        return ConversationHandler.END

    slot_dates = get_slot_dates(db, event_id)
    if not slot_dates:
        # Thanks to the previous two ifs this one shall never happen,
        # but just in case I keep it.
        await query.edit_message_text("No dates available for this event.")
        return ConversationHandler.END

    keyboard = []
    for date_item in slot_dates:
        callback_data = "event_id:" + str(event_id) + ":day:" + date_item[0]
        keyboard.append([InlineKeyboardButton(date_item[0], callback_data=callback_data)])
    keyboard.append([InlineKeyboardButton("/cancel", callback_data="cancel")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Please select a day for " + event_name + ":", reply_markup=reply_markup)

    return 2

# book - STATE 2
async def select_slot_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief STATE 2 for /book
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    STATE 2 for the <code>/book</code> command.

    Expected callback pattern (as RegEx): <code>^event_id:[0-9]*:day:[0-9|-]*$</code>

    This function lists to the user the time available for the slots
    associated to the given event-date pair, as an inline keyboard,
    then goes to STATE 3
    """
    query = update.callback_query
    await query.answer()

    callback_data = query.data[9:] # [9:] removes "event_id:" prefix
    column_position = callback_data.find(":")
    event_id = int(callback_data[:column_position])
    slot_date = callback_data[column_position+5:] # +5 removes ":day:" infix
    event_name = get_event_name(db, event_id)
    slot_times = get_slot_times(db,event_id,slot_date)

    if not slot_times:
        # Thanks to the checks in previous function, this shall never happen,
        # but just in case I keep it.
        await query.edit_message_text("No time slots available for this date.")
        return ConversationHandler.END

    keyboard = []
    for time_item in slot_times:
        callback_data = "slot_id:" + str(time_item[0])
        text_data = time_item[1] + " - " + time_item[2]
        keyboard.append([InlineKeyboardButton(text_data, callback_data=callback_data)])
    keyboard.append([InlineKeyboardButton("/cancel", callback_data="cancel")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    text_data = "Please select a time for " + event_name + ", " + slot_date + ":"
    await query.edit_message_text(text_data, reply_markup=reply_markup)

    return 3

# book - STATE 3
async def book_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief STATE 3 for /book
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    STATE 3 for the <code>/book</code> command.

    Expected callback pattern (as RegEx): <code>^slot_id:[0-9]*$</code>

    This function books a slot for the user and logs its information,
    then terminates the conversation.
    """
    query = update.callback_query
    await query.answer()

    slot_id = int(query.data[8:]) # [8:] removes "slot_id:" prefix
    user_id = update.effective_chat.id
    user_name = update.effective_chat.first_name + " " + update.effective_chat.last_name
    user_username = "@" + update.effective_chat.username
    insert_user(db,user_id,user_name,user_username)

    assign_slot(db,slot_id,user_id)
    event_id, _, start_time, end_time = get_slot_from_id(db,slot_id)
    event_name = get_event_name(db, event_id)

    response = "Booking completed successfully!\n\nDetails\n"
    response += "Event: " + event_name + "\n"
    response += "Start time: " + start_time + "\n"
    response += "End time: " + end_time + "\n"
    response += "User: " + user_name

    await query.edit_message_text(text=response)
    return ConversationHandler.END





# unbook - INIT
async def select_slot_for_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief INIT state for /unbook
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    Conversation initializer for the <code>/unbook</code> command.

    This function lists to the user the slots booked by them as an inline keyboard,
    then goes to STATE 0
    """
    user_id = update.effective_chat.id
    slot_list = get_slots_given_user(db, user_id)

    if not slot_list: # If slot_list is an empty list
        await update.message.reply_text("You have currently no bookings.")
        return ConversationHandler.END

    keyboard = []
    for slot_item in slot_list:
        callback_data = "slot_id:" + str(slot_item[0])
        response = slot_item[4] + ": " + slot_item[2]
        keyboard.append([InlineKeyboardButton(response, callback_data=callback_data)])
    keyboard.append([InlineKeyboardButton("/cancel", callback_data="cancel")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Which book do you want to cancel:", reply_markup=reply_markup)

    return 0

# unbook - STATE 0
async def confirm_unbook_slot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief STATE 0 for /unbook
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    STATE 0 for the <code>/unbook</code> command.

    Expected callback pattern (as RegEx): <code>^slot_id:[0-9]*$</code>

    This function asks the user to confirm they want to un-book the selected slot,
    through an inline keyboard, then goes to STATE 1
    """
    query = update.callback_query
    await query.answer()

    slot_id = int(query.data[8:]) # [8:] removes "slot_id:" prefix
    event_id, _, start_time, end_time = get_slot_from_id(db, slot_id)
    event_name = get_event_name(db, event_id)

    callback_data = "slot_id:" + str(slot_id)
    keyboard = [
        [InlineKeyboardButton("Unbook slot", callback_data=callback_data)],
        [InlineKeyboardButton("/cancel", callback_data="cancel")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    response = "Are you sure you want to unbook:\n"
    response += event_name + "\n"
    response += start_time + " -\n" + end_time + "?"
    await query.edit_message_text(response, reply_markup=reply_markup)

    return 1

# unbook - STATE 1
async def unbook_slot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief STATE 1 for /unbook
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    STATE 1 for the <code>/unbook</code> command.

    Expected callback pattern (as RegEx): <code>^slot_id:[0-9]*$</code>

    This function un-books a slot and logs the information it had,
    then terminates the conversation.
    """
    query = update.callback_query
    await query.answer()

    slot_id = int(query.data[8:]) # [8:] removes "slot_id:" prefix
    event_id, _, start_time, end_time = get_slot_from_id(db, slot_id)
    event_name = get_event_name(db, event_id)

    assign_slot(db, slot_id, None)

    response = "Unooking completed successfully!\n\nDetails\n"
    response += "Event: " + event_name + "\n"
    response += "Start time: " + start_time + "\n"
    response += "End time: " + end_time + "\n"
    response += "The slot is now available"
    await query.edit_message_text(response)

    return ConversationHandler.END





# mybookings - Command Handler
async def my_bookings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """! @brief Command handler for /mybookings
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return None

    Command handler for the <code>/mybookings</code> command.

    This function logs the information of all the slots associated
    to the current user.
    """
    user_id = update.effective_chat.id
    slot_list = get_slots_given_user(db, user_id)

    if not slot_list:  # If slot_list is an empty list
        response = "You have currently no bookings."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        return

    response = "You have the following bookings:\n\n"
    for slot_item in slot_list:
        response += slot_item[4] + "\n"
        response += "start: " + slot_item[2] + "\n"
        response += "end:   " + slot_item[3] + "\n\n"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    return
