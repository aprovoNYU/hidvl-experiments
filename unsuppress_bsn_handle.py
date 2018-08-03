#script to generate list of handles and bsns for HIDVL records to unsuppress
#use python 3!

import re
import csv
from datetime import datetime, date, time

filetime = datetime.now()
filetime = filetime.strftime("%Y-%m-%d_%I-%M_%p")


suppressed_bsns = input("Enter file name for the list of suppressed bsns: ")
suppressed_bsns_list =[]
bsn_handle_list=[]
with open(suppressed_bsns, "r") as f:
    suppressed_reader = csv.reader(f)
    next(suppressed_reader)
    for row in suppressed_reader:
       # print(row[0])
        suppressed_bsns_list.append(row[0])


with open("hidvl_recently_published.csv", "r") as hidvl_recently_published:
    hidvl_reader = csv.reader(hidvl_recently_published)
    next(hidvl_reader)
    for row in hidvl_reader:
        need_handles_in_aleph = []

        aleph_bsn_published = row[3].replace("\n", "")

        #print(handle)
        if aleph_bsn_published in suppressed_bsns_list:
            noid = row[0]
            handle = "http://hdl.handle.net/2333.1/" + noid
            print(aleph_bsn_published, ",", noid, ",", handle)
            need_handles_in_aleph.append(aleph_bsn_published)
            #need_handles_in_aleph.append(noid)
            need_handles_in_aleph.append(handle)
            print(need_handles_in_aleph)
        bsn_handle_list.append(need_handles_in_aleph)
print(bsn_handle_list)
for x in bsn_handle_list:
    print(x)

with open ("unsuppress_bsn_handle_hidvl_%s.csv" %filetime, 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['aleph_bsn_number','handle'])
    for x in bsn_handle_list:
        #print(x)
        #with help from: https://stackoverflow.com/questions/6916542/writing-list-of-strings-to-excel-csv-file-in-python
        if x != []:
            writer.writerow(x)
print("good job--file written!")
