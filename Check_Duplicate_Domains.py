import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', 51)
path = r"C:\Users\wausa\Work\Data\Template_For_Building_out_Accounts_-_Week_1-19.xlsx"
path1 = r"C:\Users\wausa\Work\Data\Template_For_Building_out_Accounts_-_Week_20-25.xlsx"
pathET = r"C:\Users\wausa\Work\Data\Engagetech_matched_data_from_2018_(002).xlsx"
pathAircall = r"C:\Users\wausa\Work\Data\Aircall_report_08_02.xlsx"
pathAllAccounts = r"C:\Users\wausa\Work\Data\All_Accounts_SF.csv"

# df = pd.read_excel(path)
# df1 = pd.read_excel(path1)

### use Serbia data to remove common accounts
df = pd.DataFrame()
df = df.append(pd.read_excel(path))
df = df.append(pd.read_excel(path1), ignore_index = True)

df1 = pd.read_excel(pathET)
dfAirCall = pd.read_excel(pathAircall)
dfAllAccounts = pd.read_csv(pathAllAccounts, encoding = 'ISO-8859-1')

df = df.iloc[:,0:3] # only include most useful columns
df1 = df1[df1['Matched'] == 'Yes'].reset_index(drop = True) # only matched = Yes
df['Website '] = df['Website '].str.replace('www.', '') # remove www. from websites
df['Website '].nunique() # equals 37871
df = df.drop_duplicates(subset = 'Website ') # remove duplicates

df1 = df1[~df1['Domain'].isin(df['Website '])] # removed 1050 common accounts so 1934 left
# a = []
# a.append(df1['Domain'].squeeze())
domain_changes = pd.DataFrame = ()
a = df1



### use Aircall data to remove common accounts

# get unique phone numbers called on Aircall
dfAirCall['to'] = dfAirCall['to'].astype(str) # convert call number column to string
dfAirCall['to'].nunique() # 67915 unique phone numbers

Unique_aircall_numbers = dfAirCall.drop_duplicates(subset = 'to', keep = 'last') # get details of all unique phone numbers from aircall calls

# get unique numbers from salesforce accounts/contacts
dfAllAccounts['Phone'] = dfAllAccounts['Phone'].str.replace(' ', '')
dfAllAccounts.nunique() # 167910 unique numbers from accounts
dfAllAccounts.Phone.str.contains('\+').value_counts()
dfAllAccounts['Phone'] = dfAllAccounts['Phone'].str.replace('\+', '') # remove + in dialing codes

Unique_numbers = dfAllAccounts.drop_duplicates(subset = 'Phone', keep = 'last') # get details of all unique phone numbers from all account data
Unique_numbers['Website'].str.replace('www.', '') # remove www. from websited to get domain

Websites_from_common_number = Unique_numbers[Unique_numbers['Phone'].isin(Unique_aircall_numbers['to'])][['Account Name', 'Phone', 'Website']]

Websites_from_common_number['Website'] = Websites_from_common_number['Website'].str.replace('www.', '')

Websites_from_common_number['Website'].isin(df1['Domain']).value_counts()

df1 = df1[~df1['Domain'].isin(Websites_from_common_number['Website'])] # removes another 160 domains
b  = df1

### use enagagement score != 0.05

dfAllAccounts['Website'] = dfAllAccounts['Website'].str.replace('www.', '')
Unchanged_engagement_score = dfAllAccounts.loc[dfAllAccounts['Engagement Score'] == 0.05, ['Account Name', 'Phone', 'Website']]

df1 = df1[~df1['Domain'].isin(Unchanged_engagement_score['Website'])] # removes 1000 domains
c  = df1

### use websites from accounts added in since Jan 21

pathrecent = r"C:\Users\wausa\Work\Data\Contacts added last year.xlsx"
added_recent = pd.read_excel(pathrecent)
added_recent = added_recent[['Account Name', 'Website']]
added_recent['Website'] = added_recent['Website'].str.replace('www.', '')

df1 = df1[~df1['Domain'].isin(added_recent['Website'])] # removes 1 domain
d  = df1



# a,b,c,d
df1 = pd.read_excel(pathET)
df1 = df1[df1['Matched'] == 'Yes'].reset_index(drop = True) # only matched = Yes

final = pd.concat([df1, a, b, c, d], axis = 1)
final.to_excel('Remove_dummy_domains_method.xlsx')



df2 = df2.drop_duplicates(keep = True)

df1.reset_index(drop = True)

# df1 = pd.concat([df['Account Name'].append(df['Account: Account Name'])]).reset_index(drop = True).dropna()  # combines column data and resets indices