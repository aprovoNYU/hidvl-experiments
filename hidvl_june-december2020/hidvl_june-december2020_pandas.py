import pandas as pd
import numpy as np
from datetime import datetime, date, time
filetime = datetime.now()
filetime = filetime.strftime("%Y-%m-%d_%I-%M_%p")


def merge_columns(my_df):
    l = [pd.Series(row).str.cat(sep='; ') for _, row in my_df.iterrows()]

    return pd.DataFrame(l, columns=['Result']).to_string(index=False)

# load dataframe from csv
df_pre_2019_dmd = pd.read_csv("hidvl_dmd_parsed_combined_2019-11-22_05-09_PM-june-december2020_pre-2019.csv",na_filter=False,quotechar = '"')
print(df_pre_2019_dmd)
df_pre_2019_dmd = df_pre_2019_dmd.replace(r'^\s*$', np.nan, regex=True)
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
df_pre_2019_dmd.rename(columns=pre_2019_dmd_newcols, inplace=True)
print("new df",df_pre_2019_dmd)
#based on https://stackoverflow.com/questions/16327055/how-to-add-an-empty-column-to-a-dataframe
df_pre_2019_dmd["Subjects_650"] = np.nan

#based on https://stackoverflow.com/questions/37001787/remove-ends-of-string-entries-in-pandas-dataframe-column
df_pre_2019_dmd["Additional_Production_Credits"] = df_pre_2019_dmd["Additional_Production_Credits"].str.rstrip('.')

df_pre_2019_dmd["Participants_old"] = df_pre_2019_dmd["Participants_old"].str.rstrip('.')

#This could be where I add a conditional that reads rows and looks to see if there is a value.
#maybe using https://www.geeksforgeeks.org/join-two-text-columns-into-a-single-column-in-pandas/
#or https://stackoverflow.com/questions/41449555/pandas-combine-two-columns-with-null-values

#df_pre_2019_dmd ["Participants"] = df_pre_2019_dmd["Additional_Production_Credits"] + "; " + df_pre_2019_dmd["Participants_old"] + "; " + df_pre_2019_dmd["Performers"]

#df_pre_2019_dmd ["Participants"] = df_pre_2019_dmd[["Additional_Production_Credits","Participants_old","Performers"]].apply(lambda x: '; '.join(x) if x != "NaN" else x)
print(df_pre_2019_dmd["Participants"])
#if x != None:
 #   ' '.join(x), axis = 1)
 #                                                                                                                           )


# df_pre_2019_dmd.drop(["Additional_Production_Credits","Participants_old","Performers"], axis=1, inplace=True)
# print(df_pre_2019_dmd.info())
#
# df_post_2019_dmd = pd.read_csv("Metadata-June-December 2020 publication cycle export.csv",na_filter=False,quotechar = '"')
#
# post_2019_dmd_newcols = {
#     "HI #" : "HI",
#     "Inventory": "NOID",
#     "Publication cycle" : "Publication_Cycle",
#     "Date of event" : "Date_of_Production",
#     "Location information": "Location_Venue",
#     "Language note": "Language_Note",
#     "Language": "Language_List",
#     "Main production credits": "Main_Production_Credits",
#     "Event type" : "Worktypes",
#     "Subject": "Subjects_653",
#     "Copyright holder": "Rights_Holder",
#     "Artist bio": "Artist_Bio",
#     "Run time":"Run_Time",
#     "Collection": "Series_Title",
#     "Conference":"Meeting_Information",
#     #this last change would not happen if there were actually more than one alternate title...
#     "Alternate title 1" : "Alternate_Titles"
# }
# df_post_2019_dmd.rename(columns=post_2019_dmd_newcols, inplace=True)
# df_post_2019_dmd["Subjects_650"] = np.nan
#
# df_post_2019_dmd ["Format"] = df_post_2019_dmd["How many source media form items?"].astype(str) + " " + df_post_2019_dmd["Source media format"]
#
# #I really wanted to write some logic to only concatenate alternate titles if there was more than one, but that didn't happen this time.
# #based on http://www.datasciencemadesimple.com/join-or-concatenate-string-python-dataframe/
# #df_post_2019_dmd ["Alternate Titles"] = df_post_2019_dmd[["Alternate title 1","Alternate title 2","Alternate title 3","Alternate title 4","Alternate title 5"]].apply(lambda x: '|'.join(x), axis=1)
# #df['name_match'] = df['First_name'].apply(lambda x: 'Match' if x == 'Bill' else 'Mismatch')
# #df_post_2019_dmd["Alternate Titles"] = df_post_2019_dmd["Alternate title 1"].apply(lambda x: "|" if type(x) != float else "HELLOOO" )
# #df_post_2019_dmd.loc[df_post_2019_dmd['Alternate title 1'] != type(float), ["Alternate Titles"]] = df_post_2019_dmd["Alternate title 1"]+"|"
#
#
# df_post_2019_dmd.drop(["Run time rounded","DMD Finalized","How many source media form items?","Source media format","Alternate title 2","Alternate title 3","Alternate title 4","Alternate title 5"], axis=1, inplace=True)
#
# #print(df_post_2019_dmd["Alternate title 1"])
# #print(df_post_2019_dmd["Alternate Titles"])
# #print(df_post_2019_dmd)
# print(df_post_2019_dmd.info())
# #print(df_post_2019_dmd["Alternate Titles"][15])
# #print(type(df_post_2019_dmd["Alternate title 1"][16]))
#
# df_combined_dmd = pd.concat([df_pre_2019_dmd,df_post_2019_dmd],ignore_index=True,keys=['pre', 'post'])
# print(df_combined_dmd)
# print(df_combined_dmd.info())
# df_combined_dmd.to_csv("hidvl_june-december2020_combined_%s.csv"%filetime, index=False)