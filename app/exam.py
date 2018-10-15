"""
This file deals with fetching the exam (Minor/Major Schedule)
"""

from bs4 import BeautifulSoup
import requests
import re
import json
import os
import urllib.request
from PyPDF2 import PdfFileReader, PdfFileWriter
import camelot

def update_exam_timetable():
    """
    Writes the updated exam timetable in DB/exam.json
    """

    slot_exam_schedule = fetch_slot_timetable()
    DATABASE_PATH = os.getcwd()+"/DB/"

    with open(os.path.join(DATABASE_PATH, "exam.json"), "w") as fl:
        fl.write(json.dumps(slot_exam_schedule, indent=4))


def delete_exam_schedule():
    """
    Deletes the exam timetable in DB/exam.json, minor.json, major.json
    """
    DATABASE_PATH = os.getcwd()+"/DB/"
    if os.path.exists(os.path.join(DATABASE_PATH, 'exam.json')):
        os.remove(os.path.join(DATABASE_PATH, 'exam.json'))
    if os.path.exists(os.path.join(DATABASE_PATH, 'minor.json')):
        os.remove(os.path.join(DATABASE_PATH, 'minor.json'))
    if os.path.exists(os.path.join(DATABASE_PATH, 'major.json')):
        os.remove(os.path.join(DATABASE_PATH, 'major.json'))


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
    


def download_and_segment_pdf(exam_type, pdf_link):
    """
    Download the respective file, and segment it into different pages
    to be parsed by camelot
    """
    DATABASE_PATH = os.getcwd()+"/DB/"
    pdf_path = os.path.join(DATABASE_PATH, ('pdfs/' + exam_type + '.pdf'))
    urllib.request.urlretrieve(pdf_link, pdf_path)


def split_pdf(exam_type):
    """
    Split the downloaded pdf and store the seperate pages
    """
 
    DATABASE_PATH = os.getcwd()+"/DB/"
    path = os.path.join(DATABASE_PATH, ('pdfs/' + exam_type + '.pdf'))
    output_path = DATABASE_PATH + 'pdfs/' + exam_type + '/'
    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
 
        output_filename = output_path + '{}.pdf'.format(page)
 
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
 
    num_pages_file = output_path + 'num_pages'
    num_pages = str(pdf.getNumPages())
    with open(num_pages_file, 'w') as out:
        out.write(num_pages)


def parse_pdfs(exam_type):
    """
    Parse the exam pdfs to generate csv data
    """

    DATABASE_PATH = os.getcwd()+"/DB/"
    path = os.path.join(DATABASE_PATH, ('pdfs/' + exam_type + '/'))

    num_pages_file = path + 'num_pages'
    with open(num_pages_file, 'r') as f:
        num_pages = int(f.read())

    for page in range(num_pages):
        if page == 0:
            continue
        pdf_file = path + str(page) + '.pdf'
        csv_file = path + str(page) + '.csv'
        report_file = path + str(page) + '.report'
        table = camelot.read_pdf(pdf_file)

        report = table[0].parsing_report
        table[0].to_csv(csv_file)

        with open(report_file, "w") as fl:
            fl.write(json.dumps(report, indent=4))


def extract_schedule (exam_type):
    """
    Extract the schedule from the CSV files
    """
    DATABASE_PATH = os.getcwd()+"/DB/"
    path = os.path.join(DATABASE_PATH, ('pdfs/' + exam_type + '/'))

    num_pages_file = path + 'num_pages'
    with open(num_pages_file, 'r') as f:
        num_pages = int(f.read())
        
    courses_json = {}
    for page in range(num_pages):
        if page == 0:
            continue
        courses_json = extract_schedule_csv( (path + str(page) + '.csv'), courses_json)

    # Store in the file
    with open(os.path.join(DATABASE_PATH, (exam_type + ".json")), "w") as fl:
        fl.write(json.dumps(courses_json, indent=4, sort_keys=True))


def extract_schedule_csv (csv_file, courses_json):
    """
    Parses the csv_file, and extract out the exam schedule
    Adds to courses_json
    """
    with open(csv_file) as f:
        content = f.readlines()
    
    timings = re.split(',', content[1])
    timings = gen_time_intervals(timings[2:])
    # print (content)

    for row in content[2:]:
        columns = re.split(',', row)
        # print (columns)
        room = re.sub('"', '', columns[0])
        capacity = re.sub('"', '', columns[1])
        for elem, time in zip(columns[2:], timings):
            courses = re.findall('[A-Z]{3}[0-9]{3}', elem)
            for course in courses:
                if course not in courses_json:
                    courses_json[course] = []
                courses_json[course].append({
                    'room': room,
                    'capacity': capacity,
                    'time': time
                })

    # print (courses_json)
    return courses_json



def gen_time_intervals (timings):
    """
    Clean the timings array of the form
    '"8:00-  9:00"', '"9:30- 10:30"', '"11:00-12:00"
    and make it a nice array of {start, end} objects
    """

    clean_timings = []
    for time in timings:
        time_arr = re.findall('[0-9]+:[0-9]+', time)
        time_obj = {
            'start': time_arr[0],
            'end': time_arr[1]
        }
        clean_timings.append(time_obj)
    
    return clean_timings

if __name__ == '__main__':
    fetch_slot_timetable()