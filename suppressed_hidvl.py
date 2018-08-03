#script to generate list of suppressed HIDVL records
#use python 3!

import re
import csv
from datetime import datetime, date, time

filetime = datetime.now()
filetime = filetime.strftime("%Y-%m-%d_%I-%M_%p")

bsn_list_published = []
bsn_list_published_aleph = []
bsn_list_suppressed = []
bsn_list_hidvlpublished_suppressed = []

count_suppressed=0
count_published=0
count_published_aleph=0


with open("hidvl_recently_published.csv", "r") as hidvl_recently_published:
	hidvl_reader = csv.reader(hidvl_recently_published)
	next(hidvl_reader)
	for row in hidvl_reader:
		aleph_bsn_published = row[1].replace("\n", "")
		bsn_list_published.append(aleph_bsn_published)
		count_published+=1
print(set(bsn_list_published))
print("count of records recently published to HIDVL site: ",count_published)


with open("hidvl_20180801.q", 'r') as hidvl_recs:
	for line in hidvl_recs:
		aleph_bsn = re.match(r"^\d{9}",line).group()
		#print(aleph_bsn)
		#print(line)
		handle = ""
		if "85640 L" in line:
			handle = re.search(r"(?<=85640 L \$\$u).*(?=\$\$9WEB)",line).group()
			bsn_list_published_aleph.append(aleph_bsn)
			count_published_aleph+=1
		#print(aleph_bsn, '| ', handle)
		#print(line)

		if "SUPPRESSED" in line:
			#print(aleph_bsn, '| ', handle)
			bsn_list_suppressed.append(aleph_bsn)
			count_suppressed+=1

print(set(bsn_list_published_aleph))
print("count of published aleph records: ",count_published_aleph)

print(set(bsn_list_suppressed))
print("count of suppressed records: ",count_suppressed)

#print(set(bsn_list_published) & set(bsn_list_published_aleph))
published_in_both = set(bsn_list_published) & set(bsn_list_published_aleph)
published_in_both_suppressed = published_in_both.intersection(bsn_list_suppressed)
#these have handles in aleph but are suppressed
print("count of suppressed records with handles: ",len(published_in_both_suppressed))

#these do not have handles in aleph but are published on the HIDVL site
#bsn_list_published AND bsn_list_suppressed AND NOT IN bsn_list_published_aleph

for bsn in bsn_list_published:
	if bsn in bsn_list_suppressed:
		if bsn not in bsn_list_published_aleph:
			print(bsn)
			bsn_list_hidvlpublished_suppressed.append(bsn)

# lists = []
# lists.append(bsn_list_suppressed)
# lists.append(bsn_list_published_aleph)
# lists.append(bsn_list_published)


# bsn_published_suppressed = intersect(set(bsn_list_published),bsn_list_published_aleph,bsn_list_suppressed)
# print(bsn_published_suppressed)

# published_suppressed = set(bsn_list).intersection(bsn_list_published)
#print(published_suppressed)
#print(len(bsn_list_published_suppressed))

with open ("suppressed__needAleph_handles_hidvl_%s.csv" %filetime, 'w') as file:
	writer = csv.writer(file)
	writer.writerow(['aleph_bsn_number'])
	for x in bsn_list_hidvlpublished_suppressed:
		#print(x)
		#with help from: https://stackoverflow.com/questions/6916542/writing-list-of-strings-to-excel-csv-file-in-python
		writer.writerow([x],)
print("good job--file written!")