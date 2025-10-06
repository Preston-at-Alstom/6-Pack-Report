from pypdf import PdfReader
import datetime as dt

# return page number based on day of week
def page_selector():

    work_day = dt.datetime.today().weekday()
    
    mon_thur = [0,1,2,3,]
    fri      = 4
    sat      = 5
    sun      = 6 
    

    if work_day in mon_thur:
        return 0
    if work_day == fri:
        return 1
    if work_day == sat:
        return 2
    if work_day == sun: 
        return 3


def get_connected_trains(equip_file, starting_trains):


    # creating a pdf reader object
    reader = PdfReader(equip_file)

    # select page number based on day of week
    selected_page = page_selector()

    # get all text off selected page
    page_content = reader.pages[selected_page].extract_text()
    

    all_following_trains = []
    for line in page_content.splitlines():
        if any(str(item) in line for item in starting_trains):
            all_following_trains = all_following_trains +  clean_up_line(line)

    
    return all_following_trains


# remove everything 
def clean_up_line(line):
    filtered_line = []
    items = line.split()
    for item in items:
        conditions = [
            len(item) < 4 ,
            item == '______',
            ':' in item,
            '>' in item,
            '*' in item,
            item.isalpha(),
            item[:2] == 'L6',
            item[:2] == 'L1'
        ]

        if not any(conditions):
            filtered_line.append(item)


    return filtered_line