
# coding: utf-8

# # HIDVL metadata spreadsheet merge script
# As part of the process to generate draft HIDVL MARC records by batch, we need to combine metadata spreadsheets from two different sources: the legacy metadata submission form (the data from which is converted via another script from a text file to a CSV file) and the new Airtable metadata submission form.

# In[1]:

#import modules and libraries
import pandas as pd
import numpy as np
from datetime import datetime, date, time
filetime = datetime.now()
filetime = filetime.strftime("%Y-%m-%d_%I-%M_%p")


# ## Legacy metadata
# In the first part of this process, we'll deal with the legacy metadata that dates prior to 2019.

# In[2]:

pre_2019_dmd = input("enter file name and if appropriate filepath of legacy metadata csv: ")


# In[3]:

# load old metadata dataframe from csv
df_pre_2019_dmd = pd.read_csv(pre_2019_dmd,na_filter=False,quotechar = '"')
#print(df_pre_2019_dmd)


# In[4]:

#regex replaces whitespace at the end of the cells with NaN; this also has the effect of flipping "blank" cells to NaN
#I'm sure there is a more elegant way to do this.
df_pre_2019_dmd = df_pre_2019_dmd.replace(r'^\s*$', np.nan, regex=True)


# In[5]:

#specify new column names for the incoming metadata column headers
pre_2019_dmd_newcols = {
    "HI_number" : "HI",
    "﻿NOID": "NOID",
    "Cataloged Status" : "Cataloged_Status",
    "Publication Cycle" : "Publication_Cycle",
    "Correction_note" : "Correction_Note",
    "Mastering Offset Timecode": "Mastering_Offset_Timecode",
    "Language": "Language_Note",
    "Subjects" : "Subjects_653",
    "Participants" : "Participants_old"

}


# In[6]:

#rename the column headers
df_pre_2019_dmd.rename(columns=pre_2019_dmd_newcols, inplace=True)
#print("new df",df_pre_2019_dmd)


# In[7]:

#add an empty column for 650 subjects
#based on https://stackoverflow.com/questions/16327055/how-to-add-an-empty-column-to-a-dataframe
df_pre_2019_dmd["Subjects_650"] = np.nan


# In[8]:

#strip the period from the end of the production credits and participants fields
#based on https://stackoverflow.com/questions/37001787/remove-ends-of-string-entries-in-pandas-dataframe-column
df_pre_2019_dmd["Additional_Production_Credits"] = df_pre_2019_dmd["Additional_Production_Credits"].str.rstrip('.')
df_pre_2019_dmd["Participants_old"] = df_pre_2019_dmd["Participants_old"].str.rstrip('.')


# In[9]:

#concatenate all of the participant, additional production credits, and performer columns.
#the catch is that sometimes these columns are empty!
#based on https://stackoverflow.com/questions/60724940/concatenate-strings-across-columns-that-are-not-null
df_pre_2019_dmd["Participants"] = df_pre_2019_dmd[["Additional_Production_Credits", "Participants_old", "Performers"]].apply(lambda x: '; '.join(x.dropna()), axis=1)
#print the participants field
print(df_pre_2019_dmd["Participants"])
#print a sample row to check that concatenation worked
print(df_pre_2019_dmd.loc[19,'Participants'])


# In[10]:

#get rid of the extra columns that we just concatenated into the new participants field
df_pre_2019_dmd.drop(["Additional_Production_Credits","Participants_old","Performers"], axis=1, inplace=True)
#get some info about the dataframe
print(df_pre_2019_dmd.info())


# ## Airtable metadata
# In the second part of this process, we'll deal with the new metadata that dates from 2020 to the present.

# In[11]:

post_2019_dmd = input("enter file name and if appropriate filepath of airtable metadata csv: ")


# In[12]:

# load new metadata dataframe from csv
df_post_2019_dmd = pd.read_csv(post_2019_dmd,na_filter=False,quotechar = '"')


# In[13]:

df_post_2019_dmd = df_post_2019_dmd.replace(r'^\s*$', np.nan, regex=True)


# In[14]:

df_post_2019_dmd = df_post_2019_dmd.fillna(np.nan)


# In[15]:

# specify new column names for the incoming metadata column headers
post_2019_dmd_newcols = {
    "HI #" : "HI",
    "Inventory": "NOID",
    "Publication cycle" : "Publication_Cycle",
    "Date of event" : "Date_of_Production",
    "Location information": "Location_Venue",
    "Language note": "Language_Note",
    "Language": "Language_List",
    "Main production credits": "Main_Production_Credits",
    "Event type" : "Worktypes",
    "Subject": "Subjects_653",
    "Copyright holder": "Rights_Holder",
    "Artist bio": "Artist_Bio",
    "Run time":"Run_Time",
    "Collection": "Series_Title",
    "Conference":"Meeting_Information"
}


# In[29]:

#rename the column headers
df_post_2019_dmd.rename(columns=post_2019_dmd_newcols, inplace=True)
#see what columns we have in the dataframe now:
#print("new df",df_post_2019_dmd)
print("new df",df_post_2019_dmd.info())
#Alternate titles have imported as non-null float64 values, and I'm not sure why!


# In[17]:

#add an empty column for 650 subjects
#based on https://stackoverflow.com/questions/16327055/how-to-add-an-empty-column-to-a-dataframe
df_post_2019_dmd["Subjects_650"] = np.nan


# In[18]:

#do some concatenation to populate the format field
df_post_2019_dmd ["Format"] = df_post_2019_dmd["How many source media form items?"].astype(str) + " " + df_post_2019_dmd["Source media format"]


# In[19]:

#combine copyright holder contact info into a single field
#based on https://stackoverflow.com/questions/60724940/concatenate-strings-across-columns-that-are-not-null
df_post_2019_dmd["Copyright_Contact"] = df_post_2019_dmd[["Copyright contact designation","Copyright address","Copyright business phone","Copyright mobile phone","Copyright fax","Copyright email 1","Copyright email 2","Copyright email 3","Copyright website"]].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_post_2019_dmd["Copyright_Contact"] = df_post_2019_dmd["Copyright_Contact"].replace('\\n', ', ', regex=True)
print(df_post_2019_dmd["Copyright_Contact"])


# In[20]:

#combine alternate titles into a single cell
#based on https://stackoverflow.com/questions/60724940/concatenate-strings-across-columns-that-are-not-null
#this may not actually concatenate any alternate titles, because there is usually only ever one
df_post_2019_dmd["Alternate_Titles"] = df_post_2019_dmd[["Alternate title 1","Alternate title 2","Alternate title 3","Alternate title 4","Alternate title 5"]].apply(lambda x: '|'.join(x.dropna()), axis=1)


# In[21]:

#tried filling the blank cells in this field with np.nan but it didn't work...
df_post_2019_dmd["Alternate_Titles"].fillna(np.nan)


# In[22]:

#I still wanted to check to see if the values had become null values!
print(df_post_2019_dmd ["Alternate_Titles"].isnull())


# In[23]:

#get rid of any newline characters
df_post_2019_dmd["Alternate_Titles"] = df_post_2019_dmd["Alternate_Titles"].replace('\\n', '', regex=True)


# In[24]:

#print a sample record that had newlines
print(df_post_2019_dmd.loc[26,"Alternate_Titles"])


# In[25]:

#drop unwanted columns and see what remains
df_post_2019_dmd.drop(["Run time rounded","DMD Finalized","How many source media form items?","Source media format","Alternate title 1","Alternate title 2","Alternate title 3","Alternate title 4","Alternate title 5","Copyright contact designation","Copyright address","Copyright business phone","Copyright mobile phone","Copyright fax","Copyright email 1","Copyright email 2","Copyright email 3","Copyright website"], axis=1, inplace=True)


# In[26]:

print(df_post_2019_dmd.info())


# In[27]:

df_combined_dmd = pd.concat([df_pre_2019_dmd,df_post_2019_dmd],ignore_index=True,keys=['pre', 'post'])
#print(df_combined_dmd)
print(df_combined_dmd.info())


# In[28]:

df_combined_dmd.to_csv("hidvl_metadata_combined_%s.csv"%filetime, index=False)


# The end!
# 
# _Some ideas for improvement: split legacy summary column into summary and bio (currently doing this in OpenRefine)_
