import re
#getting unique items in a list in a fast way, courtesy of https://www.peterbe.com/plog/uniqifiers-benchmark

def f5(seq, idfun=None):
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

fields_regex=re.compile(r'^([0-9]{3})', flags=re.S)
#rec_delim_re = re.compile(r'DELIMITER \d* DELIMITERDELIMITERDELIMITERDELIMITERDELIMITER\n+')
field_list = []
with open('/Users/alexandra/Desktop/hidvl-experiments/2019_08-06-hidvl-dmd-dump_pattern1.txt','r') as file:
    #read the entire file
    lines = file.readlines()
   # print(lines)
    for line in lines:
       # print(line)
    #print(file_contents)
        match = fields_regex.search(line)
        if match:
            field = match.group(1)
            print(field)
            field_list.append(field)

print(field_list)
unique_field_list = f5(field_list)
print(unique_field_list)