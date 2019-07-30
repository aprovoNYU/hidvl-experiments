#!/usr/bin/env python3

import pymarc
from pymarc import Record
import copy
import csv

#create reader for the HIDVL marc file
hidvl_file = open('hidvl_20180801.mrc', 'rb')
hidvl_reader = pymarc.MARCReader(hidvl_file, to_unicode=True, force_utf8=True, utf8_handling='strict')


fieldname = input("enter field number: ")
subfield = input("enter a subfield, or enter nothing: ")

#open the hidvl mrc file
for record in hidvl_reader:

	recordfields = record.get_fields(fieldname)
	for field in recordfields:

		if subfield != None:
			field_subfield = field.get_subfields(subfield)
			print(field_subfield)
		elif subfield == None:
			pass
		print(field)
# print(field_list)
# #dedupe the field list so you just get them listed one time
# unique_field_list = f5(field_list)
# unique_field_list_sorted = sorted(unique_field_list)
# print(unique_field_list_sorted)
# print("number of",inst_code,"records: ", "oclc= ",count1, "local= ",count2)
#
# #NEXT UP: I want to write these reports to CSVs so I can put them in my spreadsheet.
#
# with open ("field_report_%s.csv" %inst_code, 'w') as file:
# 	writer = csv.writer(file)
# 	writer.writerow(['MARC_fields'])
# 	for field in unique_field_list_sorted:
# 		#with help from: https://stackoverflow.com/questions/6916542/writing-list-of-strings-to-excel-csv-file-in-python
# 		writer.writerow([field],)
# print("good job!")
