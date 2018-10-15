"""
Contains code for populating the Schedule Database
It contains the venue information for each course
and functions for fetching the schedule of given student
"""

import json
import os
import csv
import re
import urllib.request
from PyPDF2 import PdfFileReader, PdfFileWriter
import camelot

def delete_course_schedule ():
    """
    Delete the course schedule DB
    """
    DATABASE_PATH = os.getcwd()+"/DB/"
    if os.path.exists(os.path.join(DATABASE_PATH, 'venue.json')):
        os.remove(os.path.join(DATABASE_PATH, 'venue.json'))


def download_venue_pdf (pdf_link):
    """
    Download the pdf file for room allotment
    """
    DATABASE_PATH = os.getcwd()+"/DB/"
    pdf_path = os.path.join(DATABASE_PATH, ('pdfs/' + 'venue.pdf'))
    urllib.request.urlretrieve(pdf_link, pdf_path)


def split_venue_pdf ():
    """
    Split the downloaded pdf and store the seperate pages
    """
    DATABASE_PATH = os.getcwd()+"/DB/"
    path = os.path.join(DATABASE_PATH, ('pdfs/' + 'venue.pdf'))
    output_path = DATABASE_PATH + 'pdfs/venue/'
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


def parse_venue_pdfs():
    """
    Parse the room allotment pdfs to generate csv data
    """

    DATABASE_PATH = os.getcwd()+"/DB/"
    path = os.path.join(DATABASE_PATH, ('pdfs/venue/'))

    num_pages_file = path + 'num_pages'
    num_tables_file = path + 'num_tables'
    with open(num_pages_file, 'r') as f:
        num_pages = int(f.read())

    table_no = 0
    for page in range(num_pages):
        if page < 3:
            continue
        pdf_file = path + str(page) + '.pdf'
        tables = camelot.read_pdf(pdf_file)


        for idx, table in enumerate(tables):
            csv_file = path + str(table_no) + '.csv'
            report_file = path + str(table_no) + '.report'
            table_no += 1
            report = table.parsing_report
            table.to_csv(csv_file)

            with open(report_file, "w") as fl:
                fl.write(json.dumps(report, indent=4))

    with open(num_tables_file, 'w') as f:
        f.write(str(table_no))

    
def extract_venue_info():
    """
    Extract the venue info from the CSV files
    """
    DATABASE_PATH = os.getcwd()+"/DB/"
    path = os.path.join(DATABASE_PATH, ('pdfs/venue/'))

    num_pages_file = path + 'num_pages'
    num_tables_file = path + 'num_tables'
    with open(num_tables_file, 'r') as f:
        num_tables = int(f.read())
        
    courses_venue_json = {}
    for table in range(num_tables):
        courses_venue_json = extract_venue_csv( (path + str(table) + '.csv'), courses_venue_json)

    # Store in the file
    with open(os.path.join(DATABASE_PATH, ("venue.json")), "w") as fl:
        fl.write(json.dumps(courses_venue_json, indent=4, sort_keys=True))

    return {}


def extract_venue_csv (csv_file, courses_venue_json):
    """
    Parses the csv file, and extract out venue of the respective course
    """
    with open(csv_file) as f:
        content = f.readlines()

    room = re.split(',', content[1])[0]
    room = re.sub('"', '', room)
    capacity = re.findall('\(.*\)', room)
    if len(capacity) < 1:
        capacity = "NA"
    else:
        capacity = capacity[0]
        capacity = re.sub('\(|\)', '', capacity)

    room = re.sub('\(.*\)', '', room)
    print (room)

    for row in content[1:]:
        columns = re.split(',', row)
        for elem in columns[2:]:
            courses = re.findall('[A-Z]{3}[0-9]{3}', elem)
            for course in courses:
                if course not in courses_venue_json:
                    courses_venue_json[course] = {
                        'room': room,
                        'capacity': capacity
                    }

    return courses_venue_json

    