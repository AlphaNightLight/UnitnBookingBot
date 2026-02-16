"""!
@file db_print.py
@brief Functions to print the values from the database.

This file contains the implementation of the functions with reading access to
the database that prints the records on the standard output instead of returning
them to the user. They are useful when the database is being inspected directly from
the code instead of using the Telegram API.
"""

import sqlite3





def print_users_by_id(db:str) -> None:
    """! @brief Prints all the users in the database, ordered by ID.
    @param db: string, the path to the database file
    @return None

    This function prints all the records in the <code>user</code> table
    of the specified database, ordering them by <code>user_id</code> field.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """
        SELECT user_id, name, username
        FROM users
        ORDER BY user_id ASC
        """
    )

    print(
        "| " + "ID".rjust(16) + " | " +
        "Name".rjust(32) + " | " +
        "Username".rjust(32) + " |"
    )
    print("-" * (32 + 16 + 32 + 10))

    for row in cur.fetchall():
        print(
            "| " + str(row[0]).rjust(16) + " | " +
            row[1].rjust(32) + " | " +
            row[2].rjust(32) + " |"
        )

    con.close()
    return

def print_users_by_name(db:str) -> None:
    """! @brief Prints all the users in the database, ordered by name.
    @param db: string, the path to the database file
    @return None

    This function prints all the records in the <code>user</code> table
    of the specified database, ordering them by <code>name</code> field.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """
        SELECT user_id, name, username
        FROM users
        ORDER BY name ASC
        """
    )

    print(
        "| " + "Name".rjust(32) + " | " +
        "ID".rjust(16) + " | " +
        "Username".rjust(32) + " |"
    )
    print("-" * (32 + 16 + 32 + 10))

    for row in cur.fetchall():
        print(
            "| " + row[1].rjust(32) + " | " +
            str(row[0]).rjust(16) + " | " +
            row[2].rjust(32) + " |"
        )

    con.close()
    return

def print_fairs(db:str, description:bool=False) -> None:
    """! @brief Prints all the fairs in the database, ordered by name.
    @param db: string, the path to the database file
    @param description: boolean, if True the description field is printed
    @return None

    This function prints all the records in the <code>fairs</code> table
    of the specified database, ordering them by <code>name</code> field.
    By default, the <code>description</code> field is omitted, you can print
    it as well setting the <code>description</code> parameter of this function
    to True.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """
        SELECT fair_id, name, description
        FROM fairs
        ORDER BY name ASC
        """
    )

    if description:
        print(
            "| " + "Name".rjust(32) + " | " +
            "ID".rjust(16) + " | " +
            "Description".rjust(64) + " |"
        )
        print("-" * (32 + 16 + 64 + 10))

        for row in cur.fetchall():
            print(
                "| " + row[1].rjust(32) + " | " +
                str(row[0]).rjust(16) + " | " +
                row[2].rjust(64) + " |"
            )

    else:
        print("| " + "Name".rjust(32) + " | " + "ID".rjust(16) + " |")
        print("-" * (32 + 16 + 7))

        for row in cur.fetchall():
            print(f"| {row[1].rjust(32)} | {str(row[0]).rjust(16)} |")

    con.close()
    return

def print_events(db:str, description:bool=False) -> None:
    """! @brief Prints all the events in the database, ordered by name.
    @param db: string, the path to the database file
    @param description: boolean, if True the description field is printed
    @return None

    This function prints all the records in the <code>events</code> table
    of the specified database, ordering them by <code>name</code> field.
    By default, the <code>description</code> field is omitted, you can print
    it as well setting the <code>description</code> parameter of this function
    to True.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """
        SELECT event_id, fair_id, owner_id, name, description
        FROM events
        ORDER BY name ASC
        """
    )

    if description:
        print(
            "| " + "Name".rjust(32) + " | " +
            "ID".rjust(16) + " | " +
            "Fair ID".rjust(16) + " | " +
            "Owner ID".rjust(16) + " | " +
            "Description".rjust(64) + " |"
        )
        print("-" * (32 + 16 + 16 + 16 + 64 + 16))

        for row in cur.fetchall():
            print(
                "| " + row[3].rjust(32) + " | " +
                str(row[0]).rjust(16) + " | " +
                str(row[1]).rjust(16) + " | " +
                str(row[2]).rjust(16) + " | " +
                row[4].rjust(64) + " |"
            )

    else:
        print(
            "| " + "Name".rjust(32) + " | " +
            "ID".rjust(16) + " | " +
            "Fair ID".rjust(16) + " | " +
            "Owner ID".rjust(16) + " |"
        )
        print("-" * (32 + 16 + 16 + 16 + 13))

        for row in cur.fetchall():
            print(
                "| " + row[3].rjust(32) + " | " +
                str(row[0]).rjust(16) + " | " +
                str(row[1]).rjust(16) + " | " +
                str(row[2]).rjust(16) + " |"
            )

    con.close()
    return

def print_events_with_fair(db:str) -> None:
    """! @brief Prints all the events in the database, with associated fair.
    @param db: string, the path to the database file
    @return None

    This function prints the name and ID of all the records in the
    <code>events</code> table of the specified database, together with the name
    and ID of the fair associated to them. Values are ordered by event's name.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """
        SELECT events.event_id, events.fair_id, events.name, fairs.name
        FROM events LEFT JOIN fairs
        ON events.fair_id = fairs.fair_id
        ORDER BY events.name ASC
        """
    )

    print(
        "| " + "Event Name".rjust(32) + " | " +
        "Event ID".rjust(16) + " | " +
        "Fair Name".rjust(32) + " | " +
        "Fair ID".rjust(16) + " |"
    )
    print("-" * (32 + 16 + 32 + 16 + 13))

    for row in cur.fetchall():
        print(
            "| " + row[2].rjust(32) + " | " +
            str(row[0]).rjust(16) + " | " +
            str(row[3]).rjust(32) + " | " +
            str(row[1]).rjust(16) + " |"
        )

    con.close()
    return

def print_events_with_owner(db:str) -> None:
    """! @brief Prints all the events in the database, with associated owner.
    @param db: string, the path to the database file
    @return None

    This function prints the name and ID of all the records in the
    <code>events</code> table of the specified database, together with the name
    and ID of the user that published them. Values are ordered by event's name.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """
        SELECT events.event_id, events.owner_id, events.name, users.name
        FROM events LEFT JOIN users
        ON events.owner_id = users.user_id
        ORDER BY events.name ASC
        """
    )

    print(
        "| " + "Event Name".rjust(32) + " | " +
        "Event ID".rjust(16) + " | " +
        "Owner Name".rjust(32) + " | " +
        "Owner ID".rjust(16) + " |"
    )
    print("-" * (32 + 16 + 32 + 16 + 13))

    for row in cur.fetchall():
        print(
            "| " + row[2].rjust(32) + " | " +
            str(row[0]).rjust(16) + " | " +
            str(row[3]).rjust(32) + " | " +
            str(row[1]).rjust(16) + " |"
        )

    con.close()
    return

def print_event_slots(db:str, event_id:int) -> None:
    """! @brief Prints all the slots associated to a given event in the database.
    @param db: string, the path to the database file
    @param event_id: only slots associated with this event are considered
    @return None

    This function prints the ID, start time and end time of all the records in the
    <code>slots</code> table of the specified database. In case the slot is booked
    (i.e. its <code>user_id</code> filed is not NULL) then the user's ID, name
    and username are printed as well, otherwise "SLOT AVAILABLE" will be shown.
    Values are ordered by <code>start_time</code>.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """
        SELECT slots.slot_id, slots.user_id, slots.start_time, slots.end_time,
        users.name, users.username
        FROM slots LEFT JOIN users
        ON slots.user_id = users.user_id
        WHERE slots.event_id = ?
        ORDER BY slots.start_time ASC
        """,
        (event_id,)
    )

    print(
        "| " + "Start Time".rjust(19) + " | " +
        "End Time".rjust(19) + " | " +
        "Slot ID".rjust(16) + " | " +
        "User ID".rjust(16) + " | " +
        "User's Name".rjust(32) + " | " +
        "User's Username".rjust(32) + " |"
    )
    print("-" * (19 + 19 + 16 + 16 + 32 + 32 + 19))

    for row in cur.fetchall():
        if row[1] is None:  # If no user is associated to the slot
            print(
                "| " + row[2].rjust(19) + " | " +
                row[3].rjust(19) + " | " +
                str(row[0]).rjust(16) + " | " +
                "SLOT AVAILABLE".rjust(16) + " | " +
                "".rjust(32) + " | " +
                "".rjust(32) + " |"
            )

        else:
            print(
                "| " + row[2].rjust(19) + " | " +
                row[3].rjust(19) + " | " +
                str(row[0]).rjust(16) + " | " +
                str(row[1]).rjust(16) + " | " +
                str(row[4]).rjust(32) + " | " +
                str(row[5]).rjust(32) + " |"
            )


    con.close()
    return
