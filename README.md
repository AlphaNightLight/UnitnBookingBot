# UniTN Booking Bot Readme

## Table of Contents

1. [Quick start](#quick-start)
2. [Files in this repository](#files-in-this-repository)
3. [How to install the application](#how-to-install-the-application)
4. [How to instantiate a bot](#how-to-instantiate-a-bot)
5. [How to activate the bot](#how-to-activate-the-bot)
6. [Direct access to the database](#direct-access-to-the-database)

## Quick start

This README presents the information concerning the installation and run of the project on a local machine. Other resources include:

- The full function documentation, rooted in `docs/html/index.html`.
- Links to the official documentations of all the API used by this project, reported in the file `info/api_reference.txt`.
- The command cheatsheet, located in `info/cheatsheet.md`. It also summarizes the database structure.
- The project report, `report/`, with a full description of the system architecture.

## Files in this repository

In this project, you will find the following files and folders:

- `docs/`: output folder for the Doxygen documentation.
  - `html/`: folder containing the HTML documentation of the project.
  - `latex/`: folder containing the LaTex documentation of the project.

- `handlers/`: folder containing the python modules defining the handler functions.
  - `book_commands.py`: python module defining the handlers for booking manipulation.
  - `event_commands.py`: python module defining the handlers for event manipulation.
  - `generic_commands.py`: python module defining the handlers for general information.

- `info/`: folder containing additional information on the project.
  - `api_reference.txt`: plain text reporting links to the official documentations of all the libraries used in this project.
  - `cheatsheet.md`: Markdown file presenting a summary of the command usages and the database structure.
  - `UnitnBookingBot.pptx`: Power Point presentation of the project.

- `pictures/`: folder containing the pictures used in the report and the documentation.
- `report/`: folder containing the LaTex source code for the report.

- `utils/`: folder containing the python modules for database management.
  - `db_print.py`: python module defining the functions to print the database on standard output.
  - `db_read.py`: python module defining the functions to read data from the database.
  - `db_write.py`: python module defining the functions to modify the database.

- `.env`: file defining the environment variables of the project.
- `.gitignore`: to ignore temporary folders in version controlling.
- `bot_main.py`: the main python file of the project, used to run the bot.
- `create_db.py`: python script that instantiate the database used by the bot.
- `Doxyfile`: configuration file for the Doxygen documentation.
- `edit_db.py`: python script that allows direct manipulation of the database.
- `mainpage.txt`: plain text used to create the home page in the Doxygen documentation.
- `README.md`: this file.
- `requirements.txt`: plain text reporting the python requirements to run this project.

## How to install the application

You can clone this repository on your local machine with:

```bash
git clone git@github.com:AlphaNightLight/UnitnBookingBot.git
```

Then, in the root folder of the project create a python virtual environment, activate it and install the project requirements:

```bash
# Create virtual environment
python -m venv myvenv

# Activate it
source myvenv/bin/activate # Linux and MacOS
# venv\Scripts\Activate.ps1 # Windows PowerShell
# venv\Scripts\activate.bat # Windows CMD

# Install requirements
pip install -r requirements.txt
```

The next step is to create an SQLite database. Inside `.env` set the variable `DB_PATH` to the desired database location, then run the `create_db.py` script:

```bash
python3 create_db.py
```

**NOTE**: in case you already have a database compatible with this Bot, you still need to set `DB_PATH` to its location, since the main bot script will use this variable to locate the file.

Finally, remember to deactivate the virtual environment with the command `deactivate`.

## How to instantiate a bot

To obtain a Telegram Bot you need to contact the "Bot Father", `@BotFather` username. Issuing the command `/newbot` it will ask you for a name and username to assign to your bot, and return a **Token**. Copy-paste this token inside the `.env` file, as the value of the `BOT_TOKEN` variable. It's thanks to this token that the project will be able to access your Telegram account.

Trough Bot Father you can also use `/setabouttext`, `/setdescription` and `/setuserpic` to update further information about your bot. See more details on [the official API](https://core.telegram.org/bots/features#creating-a-new-bot).

It is also suggested to set a command list. To do so use the command `/mybots`, select the bot, then tap on "Edit Commands". After it a command list will be requested as message, send the following:

```text
fairs - show all fairs
events - show all events
whoami - check your user metadata
book - book an event
unbook - unbook an event
mybookings - monitor your bookings
publish - publish an event
changedes - change event description
newslot - add a new slot to an event
deleteslot - delete a slot for an event
deleteevent - delete an entire event
myevents - monitor your events
help - show command descriptions
```

## How to activate the bot

To ensure the application works as desired, first open the `.env` file and check that the environment variables correspond to the desired values:

- `DB_PATH`: shall store the path to your database file.
- `BOT_TOKEN`: shall store the token of a bot you control.
- `DEBUG`: if True than the bot will log additional information during the run.

To activate the bot it's enough to run the main script:

```bash
python3 bot_main.py
```

**NOTE**: your computer needs an internet access to be able to contact the Telegram API. In case your application is not connected to the internet then the following error will be raised: `telegram.error.NetworkError: httpx.ConnectError: [Errno 11001] getaddrinfo failed`.

To stop the bot, enter the `ctrl+C` key on the application terminal.

## Direct access to the database

The file `edit_db.py` allows you to apply database modifications directly from code, without having to contact the Telegram API and with full access to the records. To do so open the file, uncomment the functions you wish to use, and run it with:

```bash
python3 edit_db.py
```

The most common operation you want to do from code is to create and delete fairs, since it is not possible to do them from the Bot. To create a new fair uncomment `insert_fair` and set the desired name and description. The path to the database file is automatically retrieved from the environment variable. To delete a fair, use `print_fairs` to list all fairs. You need to copy the `fair_id` value of the fair you want to delete, and pass it to the `delete_fair` function.

See the command cheatsheet `info/cheatsheet.md` to have more information on the functions you can use, and in case it's not sufficient have a look at their documentation: `docs/html/index.html`.

## Maintainer

Alex Pegoraro
