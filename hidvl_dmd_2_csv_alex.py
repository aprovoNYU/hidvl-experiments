import re
import csv
from datetime import datetime

#set up current date and time for output filename
filetime = datetime.now()
filetime = filetime.strftime("%Y-%m-%d_%I-%M_%p")
def parse_records(pattern_dict,filepath):
    # create a dictionary of regular expressions that select the value of a given field.
    # pattern 2 currently using named groups, although this isn't called in the script.
    # these regular expression dictionaries are based partially on https://www.vipinajayakumar.com/parsing-text-with-python/

    # TO DO: need to deal with weird ordering of fields
    regex_dicts = {
        "rx_dict_1" : {
        'HI_number': re.compile(r'Subject: HI Episode Submission (HI[0-9]{4}.[0-9]{3}_[0-9]{2})\n'),
        'Correction_note': re.compile(r'Supplemental or Correction description: (.*?(?=Subject|HI \w.{1,} ))',
            flags=re.S),
        'Format': re.compile(r'534 .{2} \$p(.*?(?=440|SOURCE TAPE GENERATION))', flags=re.S),
        'Source_Tape_Generation': re.compile(r'SOURCE TAPE GENERATION:(.*?(?=440))',flags=re.S),
        'Series_Title': re.compile(r'440 .{2} \$a(.*?(?=711))', flags=re.S),
        'Meeting_Information': re.compile(r'711 .{2} \$a(.*?(?=Episode))', flags=re.S),
        'Run_time': re.compile(r'Run time for episode [0-9]{2}: (.*?(?=[0-9]{3}))', flags=re.S),
        'Title': re.compile(r'245 .{2} \$a(.*?(?=[0-9]{3}))', flags=re.S),
        'Alternate_Titles': re.compile(r'246 .{2} \$a(.*?(?=[0-9]{3}))', flags=re.S),
            #to solve issue with some 260s getting populated by match from comment,
            #try 260 .{2}(.*?(?=\n[0-9]{3})) and get rid of re.S flag
        'Production_Information': re.compile(r'260 .{2}(.*?(?=\n[0-9]{3}))'),
        'Main_Production_Credits': re.compile(r'508 .{2} \$a(.*?(?=[0-9]{3}))', flags=re.S),
        'Participants': re.compile(r'511 .{2} \$a(.*?(?=[0-9]{3}))', flags=re.S),
        'Summary': re.compile(r'520 .{2} \$a(.*?(?=5|6[0-9]{2}))', flags=re.S),
        'Language': re.compile(r'546 .{2} \$a(.*?(?=[0-9]{3}))', flags=re.S),
        'Subjects': re.compile(r'653 .{2} \$a(.*?(?=[0-9]{3}))', flags=re.S),
        'Worktypes': re.compile(r'655 .{2} \$a(.*?(?=[0-9]{3}))', flags=re.S),
        'Location': re.compile(r'518.*?\$[a-z](.*?(?=[0-9]{3}))', flags=re.S),
        'Rights_Holder': re.compile(r'RIGHTS HOLDER INFORMATION:(.*)', flags=re.S)

    },
    "rx_dict_2" : {
        'HI_number': re.compile(r'Subject: HI Episode Submission (?P<HI_number>HI[0-9]{4}.[0-9]{3}_[0-9]{2})\n'),
        'Correction_note': re.compile(
            r'Supplemental or Correction description: (?P<Correction_note>.*?(?=HI Episode Submission))', flags=re.S),
        'Format': re.compile(r'Format \(534\): Media Source Original: (?P<Format>.*)'),
        'Source_Tape_Generation': re.compile(r'SOURCE TAPE GENERATION: (?P<Source_Tape_Generation>.*)'),
        'Mastering Offset Timecode': re.compile(r'MASTERING OFFSET TIMECODE:(.*)'),
        'Run_Time': re.compile(
            r'Run time for episode [0-9]{2} \(300\): -->(.+)(?=\()'),
        'Series_Title': re.compile(r'SERIES TITLE\(S\) \(830\):\n(?P<Series_Title>.*)'),
        'Meeting_Information': re.compile(r'MEETING INFORMATION \(711\):\n(?P<Meeting_Information>.*)'),
        'Title': re.compile(r'TITLE \(245\):\n(?P<Title>.*)'),
        'Alternate_Titles': re.compile(r'ALTERNATE TITLE\(S\) \(246\):(?P<Alternate_Titles>.*?(?=DATE))', flags=re.S),
        'Date_of_Production': re.compile(r'DATE OF PRODUCTION \(260_c\):\n(?P<Date_of_Production>.*)'),
        'Location_Venue': re.compile(r'LOCATION/VENUE OF EVENT \(518\):\n(?P<Location_Venue>.*)'),
        'Language': re.compile(r'LANGUAGE \(546\):\n(?P<Language>.*)'),
        'Main_Production_Credits': re.compile(
            r'MAIN PRODUCTION CREDIT\(S\) \(508\+700\):\n(?P<Main_Production_Credits>.*)'),
        'Additional_Production_Credits': re.compile(
            r'ADDITIONAL PRODUCTION CREDIT\(S\) \(508\):\n(?P<Additional_Production_Credits>.*)'),
        'Participants': re.compile(r'PARTICIPANT\(S\) \(511_0\):\n(?P<Participants>.*)'),
        'Performers': re.compile(r'PERFORMER\(S\) \(511_0\):\n(?P<Performers>.*)'),
        'Worktypes': re.compile(r'WORKTYPE\(S\) \(655\):\n(?P<Worktypes>.*?(?=PERFORMANCE))', flags=re.S),
        'Performance_Genres': re.compile(
            r'PERFORMANCE GENRE\(S\) \(655\):\n(?P<Performance_Genres>.*?(?=-----------------------------------------------------------))',
            flags=re.S),
        'Summary': re.compile(
            r'SUMMARY\/ABSTRACT \(520\):(?P<Summary>.*?(?=-----------------------------------------------------------))',
            flags=re.S),
        'Subjects': re.compile(
            r'SUBJECT\(S\) \(650\/653\):(?P<Subjects>.*?(?=-----------------------------------------------------------))',
            flags=re.S),
        'Rights_Holder': re.compile(r'RIGHTS HOLDER INFORMATION:\n(?P<Rights_Holder>.*)'),
        'Broadcast_Note': re.compile(
            r'BROADCAST NOTE:\n(?P<Broadcast_Note>.*?(?=-----------------------------------------------------------))',
            flags=re.S),
        'Note_to_Cataloger': re.compile(
            r'NOTES TO CATALOGER:\n(?P<Note_to_Cataloger>.*?(?=-----------------------------------------------------------))',
            flags=re.S)
    }

    }
    # regex that will be used to split each record on its delimiter in the text file. this is based on my predecessor heidi's work.
    rec_delim_re = re.compile(r'DELIMITER \d* DELIMITERDELIMITERDELIMITERDELIMITERDELIMITER\n+')

    #create a list for all of the records
    records_list = []
    # open the metadata text file
    with open(filepath,'r') as file:
        #read the entire file
        file_contents = file.read()
        #split each record into its own chunk of text
        records_split = rec_delim_re.split(file_contents)
        # note that when splitting, you end up with an empty list item '' at the beginning
        # a filter can be used, as explained in https://stackoverflow.com/questions/16840851/python-regex-split-without-empty-string
        records = list(filter(None,records_split))

        print(records)
        #it's good to know how many records to expect in the output
        print(len(records))
        #loop through the records
        for record in records:
            #make a dictionary that will hold the fields and values in each record
            record_dict = {}
            #specify which dictionary of regular expressions should be used, based on what pattern the user entered when running the script.
            regex_dict = regex_dicts[pattern_dict]
            # this part is based on https://www.vipinajayakumar.com/parsing-text-with-python/
            for key, rx in regex_dict.items():
                # some if statements are required because each record pattern requires different processing.
                # this is because pattern 1 records repeat the field name (for example, 653) if a field has multiple values.
                # in contrast, pattern 2 records simply separate multi-valued elements with a newline character.
                # At first I looked to this question: https://stackoverflow.com/questions/5060659/regexes-how-to-access-multiple-matches-of-a-group
                # But this explanation of re.search vs re.findall I found useful: https://stackoverflow.com/questions/9000960/python-regular-expressions-re-search-vs-re-findall

                # Here's what we do if the record pattern is 1:
                if pattern_dict == "rx_dict_1":
                    # The subjects, alternate titles, and worktypes fields are all repeatable, so we use a findall method
                    if key == 'Subjects' or key == 'Alternate_Titles' or key == 'Worktypes':
                        match = rx.findall(record)
                    #for the other fields, we use a search method
                    else:
                        match = rx.search(record)
                    if match:
                        print(key, match)
                        #if the field is one of the repeatable fields outlined above, then we want to concatenate the multiple values and separate them by a pipe character.
                        #this is because the data will be output to a CSV and I want all of my values in the same cell, so that I can split them later in the process.
                        if key == 'Subjects' or key == 'Alternate_Titles' or key == 'Worktypes':
                            match_separator = '|'
                            # at first I tried the following, but then I learned about join() from https://www.tutorialspoint.com/python/string_join.htm
                            # for value in match:
                            #     match_string = match_string + value.replace('\n', "") + '|'
                            match_string = match_separator.join(match).strip().replace('\n', "") #.replace('| ',"|") I thought about cleaning up some extra spaces, but decided this would be better to do later
                            #once things have been cleaned, we put the field and value in the dictionary
                            record_dict[key] = match_string
                        #if the field is not one of the repeatable ones, we do a little string cleanup and put the match in the dictionary
                        else:
                            record_dict[key] = match.group(1).strip().replace("    ", "").replace("\n", "")

                # Here's what we do if the record pattern is 2:
                elif pattern_dict == "rx_dict_2":
                    #for these records, we only need to use re.search
                    match = rx.search(record)
                    if match:
                        print(key,match.group(1))
                        #if the field is a repeatable field, separate the values by replacing a newline character with a pipe
                        if key == 'Subjects' or key == 'Performance_Genres' or key == 'Worktypes':
                            record_dict[key] = match.group(1).strip().replace("    ", "").replace("\n", "|")
                        #if the field is not repeatable, it might still have newline characters in it. We replace these with nothing.
                        else:
                            record_dict[key] = match.group(1).strip().replace("    ", "").replace("\n", "")

            #once a single record has been searched and the fields/values added to the record dictionary, the record gets put in a list
            records_list.append(record_dict)
    #return the list of records and the regex dictionary used. This is because when writing the CSV, we want to use the regex dictionary keys as headers.
    return [records_list,regex_dict]

#output the records as a CSV
def output_csv(pattern,records_list,regex_dict):
    with open('hidvl_dmd_parsed_%s.csv' % (pattern + "_" + filetime), 'w') as output_file:
        # the header of the csv is different depending on the regex dictionary used.
        # the * syntax is used inside of a list to generate the list of fieldnames
        # a comment explains this in https://stackoverflow.com/questions/16819222/how-to-return-dictionary-keys-as-a-list-in-python
        fieldnames = [*regex_dict.keys()]
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        # loop through the list of records and write each record's dictionary as a row in the CSV
        for record in records_list:
            writer.writerow(record)
        #that was a lot, so I like to congratulate myself at the end.
        print("yay!")

#the user enters the record pattern number
record_pattern_number = input('Enter record pattern number: ')
#that's used to say which regex dictionary should be used
pattern_dictionary_identifier = "rx_dict_" + record_pattern_number
#the file in this case is consistently named, so all we have to do is add the record pattern number the user entered earlier.
# this could also be a straightforward input, if the filenames weren't so consistent.
filepath = "hidvl-dmd-dump-2019-11-18_pattern"+record_pattern_number+".txt"
#filepath = input('enter file name')
#let's parse the records!
parsed_records_output = parse_records(pattern_dictionary_identifier,filepath)
#since the function returns both the records and the regex dict, store the returned records in a variable so we can pass them to the output function.
parsed_records = parsed_records_output[0]
#store the regex dictionary in its own variable so we can pass it to the output function
parsed_regex_dict = parsed_records_output[1]
#let's make a file so I can work with these records! Goodbye, metadata in a text file!
output_csv(record_pattern_number,parsed_records,parsed_regex_dict)