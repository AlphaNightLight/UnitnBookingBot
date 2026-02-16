from dotenv import load_dotenv
import os, sys, logging

# Load environment variables
load_dotenv()
db = os.getenv("DB_PATH")
bot_token = os.getenv("BOT_TOKEN")
debug = os.getenv("DEBUG", "False").strip().lower() == "true"



# Setup logging mode according to debug
if debug:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
else:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.ERROR
    )

    # Filter out the PTBUserWarning triggered by ConversationHandler
    from warnings import filterwarnings
    from telegram.warnings import PTBUserWarning
    filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)





from telegram.ext import filters, MessageHandler, ApplicationBuilder, \
    CommandHandler, CallbackQueryHandler, ConversationHandler

from handlers.generic_commands import start, unitn_help, unknown_command, free_text, active_command, \
    cancel, unknown_callback
from handlers.book_commands import select_fair, show_fair_description, select_event, show_event_description, whoami
from handlers.book_commands import select_slot_date, select_slot_time, book_event, select_slot_for_user, \
    confirm_unbook_slot, unbook_slot, my_bookings
from handlers.event_commands import ask_event_name, ask_event_fair, log_event_creation, ask_event_description, \
    select_user_event_after_text, log_description_update, ask_event_date, log_slot_creation
from handlers.event_commands import select_user_event, select_slot_for_event, confirm_slot_deleting, \
    log_slot_deleting, confirm_event_deleting, log_event_deleting, show_event_details





if __name__ == '__main__':
    # Check environment variables existence
    if db is None or db=="":
        sys.exit("Fatal error: database path not set. Insert it in your .env file.")
    else:
        print("Database path loaded: " + db)

    if bot_token is None or bot_token=="":
        sys.exit("Fatal error: bot token not set. Insert it in your .env file.")
    else:
        print("Bot token loaded.")

    if debug:
        print("Debug mode: ON")
    else:
        print("Debug mode: OFF")

    # Instantiate the bot
    application = ApplicationBuilder().token(bot_token).build()



    #######################
    # HANDLER DEFINITIONS #
    #######################



    # Default Commands
    # These handlers provide the user general information about the Bot

    application.add_handler(
        # Message sent at the rbot initialization
        CommandHandler('start', start)
    )

    application.add_handler(
        # Provide command descriptions
        CommandHandler('help', unitn_help)
    )



    # Information commands
    # These handlers show the user information about the fairs, events and their own account

    application.add_handler(ConversationHandler(
        # Show fairs and their descriptions
        entry_points=[CommandHandler("fairs", select_fair)],
        states={
            0: [CallbackQueryHandler(show_fair_description, pattern="^fair_id:[0-9]*$")]
        },
        fallbacks=[
            CommandHandler("fairs", active_command),
            CallbackQueryHandler(cancel, pattern="^cancel"),
            CallbackQueryHandler(unknown_callback, pattern="")
        ]
    ))

    application.add_handler(ConversationHandler(
        # Show events and their descriptions
        entry_points=[CommandHandler("events", select_fair)],
        states={
            0: [CallbackQueryHandler(select_event, pattern="^fair_id:[0-9]*$")],
            1: [CallbackQueryHandler(show_event_description, pattern="^event_id:[0-9]*$")]
        },
        fallbacks=[
            CommandHandler("events", active_command),
            CallbackQueryHandler(cancel, pattern="^cancel"),
            CallbackQueryHandler(unknown_callback, pattern="")
        ]
    ))

    application.add_handler(
        # Show information abot the user's account
        CommandHandler('whoami', whoami)
    )



    # Booking commands
    # These handlers allow the student-side user to manage their bookings

    application.add_handler(ConversationHandler(
        # Book an event
        entry_points=[CommandHandler("book", select_fair)],
        states={
            0: [CallbackQueryHandler(select_event, pattern="^fair_id:[0-9]*$")],
            1: [CallbackQueryHandler(select_slot_date, pattern="^event_id:[0-9]*$")],
            2: [CallbackQueryHandler(select_slot_time, pattern="^event_id:[0-9]*:day:[0-9|-]*$")],
            3: [CallbackQueryHandler(book_event, pattern="^slot_id:[0-9]*$")]
        },
        fallbacks=[
            CommandHandler("book", active_command),
            CallbackQueryHandler(cancel, pattern="^cancel"),
            CallbackQueryHandler(unknown_callback, pattern="")
        ]
    ))

    application.add_handler(ConversationHandler(
        # Un-book an event
        entry_points=[CommandHandler("unbook", select_slot_for_user)],
        states={
            0: [CallbackQueryHandler(confirm_unbook_slot, pattern="^slot_id:[0-9]*$")],
            1: [CallbackQueryHandler(unbook_slot, pattern="^slot_id:[0-9]*$")]
        },
        fallbacks=[
            CommandHandler("unbook", active_command),
            CallbackQueryHandler(cancel, pattern="^cancel"),
            CallbackQueryHandler(unknown_callback, pattern="")
        ]
    ))

    application.add_handler(
        # Monitor your bookings
        CommandHandler('mybookings', my_bookings)
    )



    # Event commands
    # These handlers allow the company-side user to manage their events

    application.add_handler(ConversationHandler(
        # Publish a new event
        entry_points=[CommandHandler("publish", ask_event_name)],
        states={
            0: [MessageHandler(filters.TEXT, ask_event_fair)],
            1: [CallbackQueryHandler(log_event_creation, pattern="^fair_id:[0-9]*:name:")]
        },
        fallbacks=[
            CommandHandler("publish", active_command),
            CallbackQueryHandler(cancel, pattern="^cancel"),
            CallbackQueryHandler(unknown_callback, pattern="")
        ]
    ))

    application.add_handler(ConversationHandler(
        # Change the description of an event
        entry_points=[CommandHandler("changedes", ask_event_description)],
        states={
            0: [MessageHandler(filters.TEXT, select_user_event_after_text)],
            1: [CallbackQueryHandler(log_description_update, pattern="^event_id:[0-9]*:des:")]
        },
        fallbacks=[
            CommandHandler("changedes", active_command),
            CallbackQueryHandler(cancel, pattern="^cancel"),
            CallbackQueryHandler(unknown_callback, pattern="")
        ]
    ))

    application.add_handler(ConversationHandler(
        # Add a new slot to an event
        entry_points=[CommandHandler("newslot", ask_event_date)],
        states={
            0: [MessageHandler(filters.TEXT, select_user_event_after_text)],
            1: [CallbackQueryHandler(log_slot_creation, pattern="^event_id:[0-9]*:des:")]
        },
        fallbacks=[
            CommandHandler("newslot", active_command),
            CallbackQueryHandler(cancel, pattern="^cancel"),
            CallbackQueryHandler(unknown_callback, pattern="")
        ]
    ))

    application.add_handler(ConversationHandler(
        # Delete a slot from an event
        entry_points=[CommandHandler("deleteslot", select_user_event)],
        states={
            0: [CallbackQueryHandler(select_slot_for_event, pattern="^event_id:[0-9]*$")],
            1: [CallbackQueryHandler(confirm_slot_deleting, pattern="^slot_id:[0-9]*$")],
            2: [CallbackQueryHandler(log_slot_deleting, pattern="^slot_id:[0-9]*$")]
        },
        fallbacks=[
            CommandHandler("deleteslot", active_command),
            CallbackQueryHandler(cancel, pattern="^cancel"),
            CallbackQueryHandler(unknown_callback, pattern="")
        ]
    ))

    application.add_handler(ConversationHandler(
        # Delete an event
        entry_points=[CommandHandler("deleteevent", select_user_event)],
        states={
            0: [CallbackQueryHandler(confirm_event_deleting, pattern="^event_id:[0-9]*$")],
            1: [CallbackQueryHandler(log_event_deleting, pattern="^event_id:[0-9]*$")]
        },
        fallbacks=[
            CommandHandler("deleteevent", active_command),
            CallbackQueryHandler(cancel, pattern="^cancel"),
            CallbackQueryHandler(unknown_callback, pattern="")
        ]
    ))

    application.add_handler(ConversationHandler(
        # Monitor your events
        entry_points=[CommandHandler("myevents", select_user_event)],
        states={
            0: [CallbackQueryHandler(show_event_details, pattern="^event_id:[0-9]*$")]
        },
        fallbacks=[
            CommandHandler("myevents", active_command),
            CallbackQueryHandler(cancel, pattern="^cancel"),
            CallbackQueryHandler(unknown_callback, pattern="")
        ]
    ))



    # Fallback handlers
    # These handlers allows the bot to react to unknown commands or text
    # They must be the last two, in this order, otherwise they will
    # always match a message bypassing other handlers

    application.add_handler(
        # Answer to an unknown command
        MessageHandler(filters.COMMAND, unknown_command)
    )

    application.add_handler(
        # Answer to free text
        MessageHandler(filters.TEXT & (~filters.COMMAND), free_text)
    )



    # Launch the bot
    print("BOT STARTED")
    application.run_polling()
