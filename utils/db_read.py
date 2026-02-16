"""!
@file db_read.py
@brief Functions to retrieve the values from the database.

This file contains the implementation of the functions with reading access
to the database, i.e. that can't modify the records contained in it but can only
retrieve values. They are grouped into four categories:

1) Functions to read from "users" table

2) Functions to read from "fairs" table

3) Functions to read from "events" table

4) Functions to read from "slots" table
"""

import sqlite3





# Functions to read from "users" table

def get_users(db:str) -> list[tuple[int,str,str]]:
    """! @brief Retrieves a list of all the users in the database.
    @param db: string, the path to the database file
    @return list[tuple[int,str,str]], a list of all the user records,
    each one being a tuple (user_id,name,username)

    This function retrieves all the users in the database and returns them
    as a list of tuples ordered by name, each one structured as
    <code>(user_id,name,username)</code>.
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
    res = cur.fetchall()

    con.close()
    return res

def get_user_from_id(db:str, user_id:int) -> [str, str]:
    """! @brief Retrieves the data of a specific user record.
    @param db: string, the path to the database file
    @param user_id: integer, ID of the user to retrieve
    @return name: string, the user's name
    @return username: string, the user's username

    Given the identifier of a user record, this function returns the name
    and username associated with it. In case no record is associated to the ID,
    a couple <code>(None,None)</code> is returned.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """
        SELECT name, username
        FROM users
        WHERE user_id=?
        """,
        [user_id,]
    )
    res = cur.fetchone()

    con.close()
    if res is None:
        return None, None
    return res[0], res[1]





# Functions to read from "fairs" table

def get_fairs(db:str) -> list[tuple[int,str,str]]:
    """! @brief Retrieves a list of all the fairs in the database.
    @param db: string, the path to the database file
    @return list[tuple[int,str,str]], a list of all the fair records,
    each one being a tuple (user_id,name,description)

    This function retrieves all the fairs in the database and returns them
    as a list of tuples ordered by name, each one structured as
    <code>(user_id,name,description)</code>.
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
    res = cur.fetchall()

    con.close()
    return res

def get_fair_from_id(db:str, fair_id:int) -> [str, str]:
    """! @brief Retrieves the data of a specific fair record.
    @param db: string, the path to the database file
    @param fair_id: integer, ID of the fair to retrieve
    @return name: string, the fair's name
    @return description: string, the fair's description

    Given the identifier of a fair record, this function returns the name
    and description associated with it. In case no record is associated to the ID,
    a couple <code>(None,None)</code> is returned.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """
        SELECT name, description
        FROM fairs
        WHERE fair_id=?
        """,
        [fair_id,]
    )
    res = cur.fetchone()

    con.close()
    if res is None:
        return None, None
    return res[0], res[1]





# Functions to read from "events" table

def get_events(db:str) -> list[tuple[int,int,int,str,str]]:
    """! @brief Retrieves a list of all the events in the database.
    @param db: string, the path to the database file
    @return list[tuple[int,int,int,str,str]], a list of all the event records,
    each one being a tuple (event_id,fair_id,owner_id,name,description)

    This function retrieves all the events in the database and returns them
    as a list of tuples ordered by name, each one structured as
    <code>(event_id,fair_id,owner_id,name,description)</code>.
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
    res = cur.fetchall()

    con.close()
    return res

def get_event_from_id(db:str, event_id:int) -> [int,int,str, str]:
    """! @brief Retrieves the data of a specific event record.
    @param db: string, the path to the database file
    @param event_id: integer, ID of the event to retrieve
    @return fair_id: integer, ID of the fair the event belongs to
    @return owner_id: integer, ID of the user that published the event
    @return name: string, the event's name
    @return description: string, the event's description

    Given the identifier of an event record, this function returns the data
    associated with it: fair's ID, owner's ID, name and description. In case no
    record is associated to the ID, a tuple of four None is returned.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """
        SELECT fair_id, owner_id, name, description
        FROM events
        WHERE event_id=?
        """,
        [event_id,]
    )
    res = cur.fetchone()

    con.close()
    if res is None:
        return None, None, None, None
    return res[0], res[1], res[2], res[3]

def get_event_name(db:str, event_id:int) -> str|None:
    """! @brief Retrieves the name of a specific event record.
    @param db: string, the path to the database file
    @param event_id: integer, ID of the event to retrieve
    @return string, the event's name

    Specialization of <code>get_event_from_id</code> that returns only the
    most requested field of an event record: the name. In case no
    record is associated to the ID, None is returned.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """
        SELECT name
        FROM events
        WHERE event_id=?
        """,
        [event_id,]
    )
    res = cur.fetchone()

    con.close()
    if res is None:
        return None
    return res[0]

def get_events_given_fair(db:str, fair_id:int) -> list[tuple[int,int,int,str,str]]:
    """! @brief Retrieves a list of all the events belonging to a fair.
    @param db: string, the path to the database file
    @param fair_id: integer, only the events belonging to this fair are considered
    @return list[tuple[int,int,int,str,str]], a list of the event records
    belonging to the fair, each one being a tuple
    (event_id, fair_id, owner_id, name, description)

    This function retrieves all the events in the database belonging to a certain
    fair. The result is a list of tuples ordered by name, each one structured as
    <code>(event_id,fair_id,owner_id,name,description)</code>.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """
        SELECT event_id, fair_id, owner_id, name, description
        FROM events
        WHERE fair_id=?
        ORDER BY name ASC
        """,
        [fair_id,]
    )
    res = cur.fetchall()

    con.close()
    return res

def get_events_given_owner(db:str, owner_id:int) -> list[tuple[int,int,int,str,str]]:
    """! @brief Retrieves a list of all the events published by a user.
    @param db: string, the path to the database file
    @param owner_id: integer, the ID of the user to look for
    @return list[tuple[int,int,int,str,str]], a list of the event records
    published by that user, each one being a tuple
    (event_id, fair_id, owner_id, name, description)

    This function retrieves all the events in the database with a certain
    <code>owner_id</code>, i.e. published by a certain user. The result is
    a list of tuples ordered by name, each one structured as
    <code>(event_id,fair_id,owner_id,name,description)</code>.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """
        SELECT event_id, fair_id, owner_id, name, description
        FROM events
        WHERE owner_id=?
        ORDER BY name ASC
        """,
        [owner_id,]
    )
    res = cur.fetchall()

    con.close()
    return res





# Functions to read from "slots" table

def get_slots(db:str) -> list[tuple[int,int,int,str,str]]:
    """! @brief Retrieves a list of all the slots in the database.
    @param db: string, the path to the database file
    @return list[tuple[int,int,int,str,str]], a list of all the slot records,
    each one being a tuple (slot_id,event_id,user_id,start_time,end_time)

    This function retrieves all the slots in the database and returns them
    as a list of tuples ordered by start time, each one structured as
    <code>(slot_id,event_id,user_id,start_time,end_time)</code>.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """
        SELECT slot_id, event_id, user_id, start_time, end_time
        FROM slots
        ORDER BY start_time ASC
        """
    )
    res = cur.fetchall()

    con.close()
    return res

def get_slot_from_id(db:str, slot_id:int) -> [int, int, str, str]:
    """! @brief Retrieves the data of a specific slot record.
    @param db: string, the path to the database file
    @param slot_id: integer, ID of the slot to retrieve
    @return event_id: integer, ID of the event the slot refers to
    @return user_id: integer, ID of the user that booked this slot
    @return start_time: time string ISO-8601, date and time the slot will start
    @return end_time: time string ISO-8601, date and time the slot will end

    Given the identifier of a slot record, this function returns the data
    associated with it: event's ID, user that booked it (None if it's a free slot),
    start time and end time. The two times are time strings in ISO-8601 format.
    If no record is associated to the ID, a tuple of four None is returned.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """
        SELECT event_id, user_id, start_time, end_time
        FROM slots
        WHERE slot_id=?
        """,
        [slot_id,]
    )
    res = cur.fetchone()

    con.close()
    if res is None:
        return None, None, None, None
    return res[0], res[1], res[2], res[3]

def get_slot_dates(db:str, event_id:int) -> list[tuple[str]]:
    """! @brief Retrieves a list of all the dates with at least one free slot
    associated with them, restricted to a given event.
    @param db: string, the path to the database file
    @param event_id: integer, only slots associated with this event are considered
    @return list[tuple[str]], a list of all the days with at least one free slots
    associated with them, each one being a singleton (date,)

    This function retrieves the dates of all the slots that meets the
    following criteria:

    1) The slot is free, i.e. with NULL user

    2) The slot's event_id is the one passed as parameter

    The result is a list of tuples, each one structured as a singleton
    <code>(date,)</code>.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """
        SELECT DATE(start_time) AS slot_day
        FROM slots
        WHERE event_id=? AND user_id IS NULL
        GROUP BY slot_day
        ORDER BY slot_day
        """,
        [event_id,]
    )
    res = cur.fetchall()

    con.close()
    return res

def get_slot_times(db:str, event_id:int, slot_day:str) -> list[tuple[int,str,str]]:
    """! @brief Retrieves a list of all the slots in the database for a given
    date and event.
    @param db: string, the path to the database file
    @param event_id: integer, only slots associated with this event are considered
    @param slot_day: time string ISO-8601, only slots scheduled to start
    on this day are considered
    @return list[tuple[int,str,str]], a list of all the slot records,
    each one being a tuple (slot_id, start_time, end_time)

    This function retrieves all the events in the database associated with a given
    event ID <b>and</b> scheduled to start on a given day. The result is
    a list of tuples ordered by <code>start_time</code>, each one structured as
    <code>(slot_id,start_time,end_time)</code>.
    Please ensure the <code>slot_day</code> string is formatted according to an
    ISO-8601 day, i.e. "YYYY-MM-DD", as no format check is made.
    Also note that since the day is passed as a parameter, <code>start_time</code>
    and <code>end_time</code> will contain just the ISO-8601 time component
    as ""HH:MM:SS, without including the day.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """
        SELECT slot_id, TIME(start_time) AS start_time, TIME(end_time) AS end_time
        FROM slots
        WHERE event_id=? AND user_id IS NULL AND DATE(start_time)=?
        ORDER BY start_time ASC
        """,
        [event_id,slot_day]
    )
    res = cur.fetchall()

    con.close()
    return res

def get_slots_given_user(db:str, user_id:int) -> list[tuple[int,int,str,str,str,str]]:
    """! @brief Retrieves a list of all the slots booked by a user.
    @param db: string, the path to the database file
    @param user_id: integer, the ID of the user to look for
    @return list[tuple[int,int,str,str,str,str]], a list of the slot records
    booked by that user, each one being a tuple
    (slot_id,event_id,start_time,end_time,event_name,event_description)

    This function retrieves all the slots in the database with a certain
    <code>user_id</code>, i.e. booked by a certain user. The result is
    a list of tuples ordered first by event_name and then by start_time,
    each one structured as
    <code>(slot_id,event_id,start_time,end_time,event_name,event_description)</code>.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """
        SELECT slots.slot_id, slots.event_id, slots.start_time, slots.end_time,
        events.name, events.description
        FROM slots LEFT JOIN events
        ON slots.event_id = events.event_id
        WHERE slots.user_id = ?
        ORDER BY events.name ASC, slots.start_time ASC
        """,
        [user_id,]
    )
    res = cur.fetchall()

    con.close()
    return res

def get_slots_given_event(db:str, event_id:int) -> list[tuple[int,int,str,str,str,str]]:
    """! @brief Retrieves a list of all the slots associated to an event.
    @param db: string, the path to the database file
    @param event_id: integer, the ID of the event to look for
    @return list[tuple[int,int,str,str,str,str]], a list of the slot records
    associated to the event, each one being a tuple
    (slot_id,user_id,start_time,end_time,user_name,user_username)

    This function retrieves all the slots in the database with a certain
    <code>event_id</code>, i.e. associated to a certain event. The result is
    a list of tuples ordered first by start_time and then by user_name,
    each one structured as
    <code>(slot_id,user_id,start_time,end_time,user_name,user_username)</code>.
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
        ORDER BY slots.start_time ASC, users.name ASC
        """,
        [event_id,]
    )
    res = cur.fetchall()

    con.close()
    return res

def count_slots(db:str, event_id:int) -> [int, int]:
    """! @brief Counts the free and total number of slots associate with an event.
    @param db: string, the path to the database file
    @param event_id: integer, only slots associated with this event are considered
    @return free_slots: integer, number of free slots associated to the event
    @return all_slots: integer, total number of slots associated to the event

    This function counts how many slots associated to a given event are free, i.e.
    with NULL <code>user_id</code>, as well as the total number of slots associated
    to the event, regardless of their <code>user_id</code>.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(
        """
        SELECT COUNT(*)
        FROM slots
        WHERE event_id=? AND user_id IS NULL
        """,
        [event_id,]
    )
    free_slots = cur.fetchone()
    free_slots = free_slots[0]
    cur.execute(
        """
        SELECT COUNT(*)
        FROM slots
        WHERE event_id=?
        """,
        [event_id, ]
    )
    all_slots = cur.fetchone()
    all_slots = all_slots[0]

    con.close()
    return free_slots, all_slots
