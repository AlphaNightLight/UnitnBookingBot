"""!
@file generic_commands.py
@brief Handlers for general information.

This file contains the implementation of the Telegram Bot Handlers that manage
the generic commands <code>/start</code> and <code>/help</code>, together with the fallbacks
for invalid commands and command-less text.
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



from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler





# start - Command Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """! @brief Command handler for /start
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return None

    Command handler for the <code>/start</code> command.

    This function logs some generic information about the Bot and its purpose.
    """
    response = "Hi, I am UniTN Booking Bot!" + \
               " You can use me to book appointments for the University of Trento, Italy." + \
               " Have a look at /help for a comprehensive command description!"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    return



# help - Command Handler
async def unitn_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """! @brief Command handler for /help
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return None

    Command handler for the <code>/felp</code> command.

    This function presents the description of all the other commands.
    """
    response = "Hi, I am UniTN Booking Bot!\n" + \
               "Here is a list of my commands divided by functions:\n" + \
               \
               "\nGeneral information:\n\n" + \
               "/fairs: show all the fairs and their descriptions\n" + \
               "/events: show all events of a fair and their descriptions\n" + \
               "/whoami: show the metadata associated with this chat\n" + \
               \
               "\nManage your bookings:\n\n" + \
               "/book: book a slot for an event\n" + \
               "/unbook: cancel your booking for a slot\n" + \
               "/mybookings: show information about all your active bookings\n" + \
               \
               "\nManage your events:\n\n" + \
               "/publish: create a new event\n" + \
               "/changedes: change the description of an event of yours\n" + \
               "/newslot: add a new bookable slot to an event of yours\n" + \
               "/deleteslot: delete a slot from an event of yours\n" + \
               "/deleteevent: delete an event and all associated slots\n" + \
               "/myevents: show information about all the events you own"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    return



# Unknown commands - Message Handler
async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """! @brief Message handler for unknown commands
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return None

    This handler is triggered in case of an unknown command.

    This function prints a message that redirects the user to the /help command.
    """
    response = "Unrecognized command: " + update.message.text + \
               ", please use /help to see the list of available commands!"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    return



# Free Text - Message Handler
async def free_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """! @brief Message handler for generic text
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return None

    This handler is triggered in case of a message with no command.

    This function prints a message that redirects the user to the /help command.
    """
    response = "I can't answer to free text, please use /help" + \
               " to see the list of available commands!"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    return



# All conversations - fallback STATE
async def active_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """! @brief fallback STATE for all the conversations
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return None

    This handler is triggered inside a conversation handler in case
    the current command is repeated.

    This function prints a message that informs the user the command is
    already active.
    """
    response = "Command already active."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    return



# All conversations - fallback STATE
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief fallback STATE for all the conversations
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    This handler is triggered inside a conversation handler anytime the /cancel
    button is pressed.

    Expected callback pattern (as RegEx): <code>^cancel</code>

    This function prints a message that informs the user the operation is
    cancelled, and immediately terminates the conversation.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Operation cancelled.")
    return ConversationHandler.END



# All conversations - fallback STATE
async def unknown_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """! @brief fallback STATE for all the conversations
    @param update: Update, Telegram parameters
    @param context: ContextTypes, library status
    @return integer, the next state

    This handler is triggered inside a conversation handler anytime an invalid
    callback pattern is detected.

    This function prints an error message that informs the user the operation is
    cancelled, and immediately terminates the conversation.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Unknown callback, operation cancelled.")
    return ConversationHandler.END
