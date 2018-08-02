#script to generate list of suppressed HIDVL records
#use python 3!

import re
import csv
from datetime import datetime, date, time

filetime = datetime.now()
filetime = filetime.strftime("%Y-%m-%d_%I-%M_%p")

bsn_list_published = []
bsn_list_published_suppressed = []

count_suppressed=0
count_published=0
with open("hidvl_recently_published.csv", "r") as hidvl_recently_published:
	hidvl_reader = csv.reader(hidvl_recently_published)
	next(hidvl_reader)
	for row in hidvl_reader:
		aleph_bsn_published = row[1].replace("\n", "")
		bsn_list_published.append(aleph_bsn_published)
		count_published+=1
print(bsn_list_published)
print("count of published records: ",count_published)


with open("hidvl_20180801.q", 'r') as hidvl_recs:
	for line in hidvl_recs:
		aleph_bsn = re.match(r"^\d{9}",line).group()
		#print(aleph_bsn)
		#print(line)
		handle = ""
		if "85640 L" in line:
			handle = re.search(r"(?<=85640 L \$\$u).*(?=\$\$9WEB)",line).group()
			
			if handle:
				pass
			else:
				handle = "no handle"
		#print(aleph_bsn, '| ', handle)		
		#print(line)
		
		if "SUPPRESSED" in line and aleph_bsn in bsn_list_published:
			#print(aleph_bsn, '| ', handle)
			bsn_list_published_suppressed.append(aleph_bsn)
			count_suppressed+=1
print(bsn_list_published_suppressed)
print("count of suppressed and published records: ",count_suppressed)



# published_suppressed = set(bsn_list).intersection(bsn_list_published)
# print(published_suppressed)
#print(len(bsn_list_published_suppressed))

with open ("suppressed_hidvl_%s.csv" %filetime, 'w') as file:
	writer = csv.writer(file)
	writer.writerow(['aleph_bsn_number'])
	for x in bsn_list_published_suppressed:
		#print(x)
		#with help from: https://stackoverflow.com/questions/6916542/writing-list-of-strings-to-excel-csv-file-in-python
		writer.writerow([x],)
print("good job--file written!")