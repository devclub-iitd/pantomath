"""
This file deals with fetching the exam (Minor/Major Schedule)
"""

from bs4 import BeautifulSoup
import requests
import re
import json
import os

def update_exam_timetable():
    """
    Writes the updated exam timetable in DB/exam.json
    """

    slot_exam_schedule = fetch_slot_timetable()
    DATABASE_PATH = os.getcwd()+"/DB/"

    with open(os.path.join(DATABASE_PATH, "exam.json"), "w") as fl:
        fl.write(json.dumps(slot_exam_schedule, indent=4, sort_keys=True))


def delete_exam_schedule():
    """
    Deletes the exam timetable in DB/exam.json
    """
    DATABASE_PATH = os.getcwd()+"/DB/"
    if os.path.exists(os.path.join(DATABASE_PATH, 'exam.json')):
        os.remove(os.path.join(DATABASE_PATH, 'exam.json'))


def fetch_slot_timetable():
    """
    Fetches the slot wise timings and dates of 
    Minor and Major exams from timetable.iitd.ac.in
    """

    url = 'http://timetable.iitd.ac.in/schedule.html'
    page = requests.get(url)
    pageText = page.text

    soup = BeautifulSoup(pageText, 'html.parser')

    table_rows = soup.find_all('tr')
    slot_schedule = {}

    # Minor 1 schedule
    if len(table_rows) < 2:
        return slot_schedule

    M1_slots = []
    M1_dates = []
    for col in table_rows[1].find_all('td')[1:]:
        M1_slots.append(col.text)
    for col in table_rows[0].find_all('td')[2:]:
        M1_dates.append(col.text)

    for slots, date in zip(M1_slots, M1_dates):
        # slots = slots.split(',', '/')
        slots = re.split(', |/ |/  |\*|free slot', slots)
        for slot in slots:
            if slot == '' or slot == ' ':
                continue
            if slot not in slot_schedule:
                slot_schedule[slot] = {}
            slot_schedule[slot]['M1'] = date


    # Minor 2 schedule
    if len(table_rows) < 5:
        return slot_schedule
        
    M2_slots = []
    M2_dates = []
    for col in table_rows[4].find_all('td')[1:]:
        M2_slots.append(col.text)
    for col in table_rows[3].find_all('td')[2:]:
        M2_dates.append(col.text)

    for slots, date in zip(M2_slots, M2_dates):
        # slots = slots.split(',', '/')
        slots = re.split(', |/ |/  |\*|free slot', slots)
        for slot in slots:
            if slot == '' or slot == ' ':
                continue
            if slot not in slot_schedule:
                slot_schedule[slot] = {}
            slot_schedule[slot]['M2'] = date


    # Major schedule
    if len(table_rows) < 8:
        return slot_schedule
        
    MJ_slots = []
    MJ_dates = []
    for col in table_rows[7].find_all('td')[1:]:
        MJ_slots.append(col.text)
    for col in table_rows[6].find_all('td')[2:]:
        MJ_dates.append(col.text)

    for slots, date in zip(MJ_slots, MJ_dates):
        # slots = slots.split(',', '/')
        slots = re.split(', |/ |/  |\*|free slot', slots)
        for slot in slots:
            if slot == '' or slot == ' ':
                continue
            if slot not in slot_schedule:
                slot_schedule[slot] = {}
            slot_schedule[slot]['MJ'] = date

    return slot_schedule


if __name__ == '__main__':
    fetch_slot_timetable()