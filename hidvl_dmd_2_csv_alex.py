
import re
import csv
from datetime import datetime, date, time

pattern = input('Enter record pattern number:')

#set up current date and time for filename
filetime = datetime.now()
filetime = filetime.strftime("%Y-%m-%d_%I-%M_%p")

#create a dictionary of regular expressions that select the value of a given field. Currently using named groups, although this isn't called in the script.
#these regular expression dictionaries are based partially on https://www.vipinajayakumar.com/parsing-text-with-python/

#need to add 544, 654, 555 deal with weird ordering of fields
rx_dict_1 = {
    'HI_number' : re.compile(r'Subject: HI Episode Submission (HI[0-9]{4}.[0-9]{3}_[0-9]{2})\n'),
    #submission could read as follows or could have different language
    'Correction_note' : re.compile(r'Supplemental or Correction description: (.*?(?=Subject: HI Collection Survey Form Submission))', flags=re.S),
    'Format' : re.compile(r'534 .{2} \$p(.*?(?=440))', flags=re.S),
    'Series_Title' : re.compile(r'440 .{2} \$a(.*?(?=711))', flags=re.S),
    'Meeting_Information' : re.compile(r'711 .{2} \$a(.*?(?=Episode))', flags=re.S),
    'Run_time' : re.compile(r'Run time for episode [0-9]{2}: (.*?(?=[0-9]{3}))', flags=re.S),
    'Title' : re.compile(r'245 .{2} \$a(.*?(?=[0-9]{3}))', flags=re.S),
    'Alternate_Titles' : re.compile(r'246 .{2} \$a(.*?(?=[0-9]{3}))', flags=re.S),
    'Production_Information' : re.compile(r'260 .{2}(.*?(?=5.{2}))', flags=re.S),
    'Main_Production_Credits' : re.compile(r'508 .{2} \$a(.*?(?=[0-9]{3}))', flags=re.S),
    'Participants' : re.compile(r'511 .{2} \$a(.*?(?=[0-9]{3}))', flags=re.S),
    'Summary' : re.compile(r'520 .{2} \$a(.*?(?=5|6[0-9]{2}))', flags=re.S),
    'Language' : re.compile(r'546 .{2} \$a(.*?(?=[0-9]{3}))', flags=re.S),
    'Subjects' : re.compile(r'653 .{2} \$a(.*?(?=[0-9]{3}))', flags=re.S),
    'Worktypes' : re.compile(r'655 .{2} \$a(.*?(?=[0-9]{3}))', flags=re.S),
    'Location' : re.compile(r'518.*?\$[a-z](.*?(?=[0-9]{3}))', flags=re.S),
    'Rights_Holder': re.compile(r'RIGHTS HOLDER INFORMATION:(.*)', flags=re.S)

}


rx_dict_2 = {
    'HI_number' : re.compile(r'Subject: HI Episode Submission (?P<HI_number>HI[0-9]{4}.[0-9]{3}_[0-9]{2})\n'),
    'Correction_note' : re.compile(r'Supplemental or Correction description: (?P<Correction_note>.*?(?=HI Episode Submission))', flags=re.S),
    'Format' : re.compile(r'Format \(534\): Media Source Original: (?P<Format>.*)'),
    'Source_Tape_Generation' : re.compile(r'SOURCE TAPE GENERATION: (?P<Source_Tape_Generation>.*)'),
    'Run_Time' : re.compile(r'Run time for episode [0-9]{2} \(300\): --> (?P<Run_Time>[0-9]{2}:[0-9]{2}:[0-9]{2} \(hh:mm:ss\))'),
    'Series_Title' : re.compile(r'SERIES TITLE\(S\) \(830\):\n(?P<Series_Title>.*)'),
    'Meeting_Information' : re.compile(r'MEETING INFORMATION \(711\):\n(?P<Meeting_Information>.*)'),
    'Title' : re.compile(r'TITLE \(245\):\n(?P<Title>.*)'),
    'Alternate_Titles' : re.compile(r'ALTERNATE TITLE\(S\) \(246\):(?P<Alternate_Titles>.*?(?=DATE))',flags=re.S),
    'Date_of_Production' : re.compile(r'DATE OF PRODUCTION \(260_c\):\n(?P<Date_of_Production>.*)'),
    'Location_Venue' : re.compile(r'LOCATION\/VENUE OF EVENT \(518\):\n(?P<Location_Venue>.*)'),
    'Language' : re.compile(r'LANGUAGE \(546\):\n(?P<Language>.*)'),
    'Main_Production_Credits' : re.compile(r'MAIN PRODUCTION CREDIT\(S\) \(508\+700\):\n(?P<Main_Production_Credits>.*)'),
    'Additional_Production_Credits' : re.compile(r'ADDITIONAL PRODUCTION CREDIT\(S\) \(508\):\n(?P<Additional_Production_Credits>.*)'),
    'Participants' : re.compile(r'PARTICIPANT\(S\) \(511_0\):\n(?P<Participants>.*)'),
    'Performers' : re.compile(r'PERFORMER\(S\) \(511_0\):\n(?P<Performers>.*)'),
    'Worktypes' : re.compile(r'WORKTYPE\(S\) \(655\):\n(?P<Worktypes>.*?(?=PERFORMANCE))',flags=re.S),
    'Performance_Genres' : re.compile(r'PERFORMANCE GENRE\(S\) \(655\):\n(?P<Performance_Genres>.*?(?=-----------------------------------------------------------))', flags=re.S),
    'Summary' : re.compile(r'SUMMARY\/ABSTRACT \(520\):(?P<Summary>.*?(?=-----------------------------------------------------------))', flags=re.S),
    'Subjects' : re.compile(r'SUBJECT\(S\) \(650\/653\):(?P<Subjects>.*?(?=-----------------------------------------------------------))', flags=re.S),
    'Rights_Holder' : re.compile(r'RIGHTS HOLDER INFORMATION:\n(?P<Rights_Holder>.*)'),
    'Broadcast_Note' : re.compile(r'BROADCAST NOTE:\n(?P<Broadcast_Note>.*?(?=-----------------------------------------------------------))', flags=re.S),
    'Note_to_Cataloger' : re.compile(r'NOTES TO CATALOGER:\n(?P<Note_to_Cataloger>.*?(?=-----------------------------------------------------------))', flags=re.S)
}

#delimiter to split each record in the text file.
rec_delim_re = re.compile(r'DELIMITER \d* DELIMITERDELIMITERDELIMITERDELIMITERDELIMITER\n+')

#create a list for the records
records_list = []


#open the DMD text file
with open('2019-08-06-hidvl-dmd-dump_pattern1.txt','r') as file:
    #read the entire file
    file_contents = file.read()
   # print(file_contents)
    #split each record into its own chunk of text
    records = rec_delim_re.split(file_contents)
   # print(records)
    print(len(records))
    #loop through the records
    for record in records:
        #print(record)

        #create a dictionary which will contain each record's field and value
        record_dict = {}
        #while looping through each record, loop through the regexes above
        # based partially on https://www.vipinajayakumar.com/parsing-text-with-python/
        for key, rx in rx_dict_1.items():
            #within each record / text blob, search for each of the regexes
            match = rx.search(record)
            if match:
                #print(key,match.group(1))
                #add each field/value to the dictionary for this record
                record_dict[key] = match.group(1).strip().replace("    ","").replace("\n","|")
            else:
                pass

        #print(record_dict)
        #append the entire record dictionary to the list of records
        records_list.append(record_dict)
    print(records_list)
    #print(len(records_list))
#
#output as a CSV
with open ('hidvl_dmd_parsed_%s.csv' %("pattern"+pattern + "_" + filetime), 'w') as output_file:
    fieldnames = [*rx_dict_1.keys()]
        #['HI_number', 'Correction_note', 'Format', 'Source_Tape_Generation', 'Run_Time', 'Series_Title', 'Meeting_Information', 'Title', 'Alternate_Titles', 'Date_of_Production', 'Location_Venue', 'Language', 'Main_Production_Credits', 'Additional_Production_Credits', 'Participants', 'Performers', 'Worktypes', 'Performance_Genres', 'Summary', 'Subjects', 'Rights_Holder', 'Broadcast_Note', 'Note_to_Cataloger']
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    #loop through the list of records and write each dictionary as a row in the CSV
    for record in records_list:
        writer.writerow(record)
    print("yay!")

#### old attempts
# def parse_line(record):
#     for key, rx in rx_dict.items():
#         match = rx.search(record)
#         if match:
#             return key, match
#
#     return None, None

# with open('/Users/alexandra/Downloads/hidvl_20140327/hidvl_heidi/hidvl_sampledmd.txt', 'r') as file_object:

    # match = rec_delim_re.split(file_contents)
    # print(match)
    # record_list = {}
    # for rec in match:
    #     print(rec)
    #     parsed_rec = parse_record(rec)
    #     print(parsed_rec)

#     record = match[1]
#     print(record)

#                 record_list[key] = match.group(1).strip()
# print(record_list)