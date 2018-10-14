"""
Contains code for populating the Schedule Database
It contains the venue information for each course
and functions for fetching the schedule of given student
"""

import json
import os
import csv

def update_course_schedule ():
    """
    Updates the schedules for all courses by calling appropriate functions
    """

    update_venue_csv()

    DATABASE_PATH = os.getcwd()+"/DB/"
    update_schedule_json(DATABASE_PATH)


def delete_course_schedule ():
    """
    Delete the course schedule DB
    """
    DATABASE_PATH = os.getcwd()+"/DB/"
    if os.path.exists(os.path.join(DATABASE_PATH, 'venue.json')):
        os.remove(os.path.join(DATABASE_PATH, 'venue.json'))


def update_venue_csv ():
    """
    Generate the venue.csv file in the /DB/csv_files folder
    """

    return True


def update_schedule_json (db_path):
    """
    Generates the DB/venue.json file using the DB/csv_files/venue.csv, slot.json
    """

    venue_json ={}
    with open(os.path.join(db_path,"csv_files/venue.csv"), "r") as fl:
        vreader = csv.reader(fl,delimiter=',')
        for row in vreader:
            course = row[1].strip().upper()
            slot = row[0].strip().upper()
            venue = row[2].strip().upper()
            if(course not in venue):
                venue_json[course] = {}
                
            venue_json[course][slot] = venue

    with open(os.path.join(db_path,"venue.json"), "w") as fl:
        fl.write(json.dumps(venue_json, indent=4, sort_keys=True))


