import pandas as pd
import glob
import os

# contacts import
contacts = pd.read_csv(r"C:\Users\wausa\Work\Data\SF_Data\Contacts_All_Data.csv", encoding='ISO-8859-1')
# contacts_with_emails = contacts[['CASESAFE_CONTACT_ID__C', 'EMAIL', 'PHONE', 'MOBILEPHONE', 'ALTERNATIVE_NUMBER__C', 'DIRECT_DIAL__C']]

path = r'C:\Users\wausa\Work\DataScienceTesting\Predicted_email_verification'

all_files = glob.glob(os.path.join(path, "df*.csv")) # advisable to use os.path.join as this makes concatenation OS independent

df_from_each_file = (pd.read_csv(f, low_memory=False) for f in all_files)
concatenated_df = pd.concat(df_from_each_file, ignore_index=True)

concatenated_df = concatenated_df[['Email', 'Verified', 'Date']]
concatenated_df = concatenated_df.drop_duplicates('Email').reindex()

concatenated_df['Verified'].value_counts() #53% verified

concatenated_df = concatenated_df.merge(contacts[['CASESAFE_CONTACT_ID__C', 'EMAIL']],
                      left_on = 'Email', right_on = 'EMAIL')
# remove nonsense columns
concatenated_df = concatenated_df[['CASESAFE_CONTACT_ID__C', 'Email', 'Verified', 'Date']]\
    .drop_duplicates('CASESAFE_CONTACT_ID__C')


concatenated_df.to_csv('Verified_emails_100000.csv')

# need to add fields to salesforce for email, verification successful, verification data



import os
import datetime
os.path.getmtime(r"C:\Users\wausa\Work\DataScienceTesting\Email_verification_12_08\df1.csv")

for item in os.scandir(path):
     # print(item.name, item.path, item.stat().st_size, item.stat().st_atime)
     print(datetime.fromtimestamp(item.stat().st_atime, tz=timezone.utc))

from datetime import datetime

os.chdir(r'C:\Users\wausa\Work\DataScienceTesting\Email_verification_12_08') #################################################################

for i in range(100, 1001):
    exec('df = pd.read_csv(\'df' + str(i) + '.csv\')')
    exec('df.insert(0, \'Date\', datetime.fromtimestamp(os.path.getctime(\'df1.csv\')).strftime(\'%Y-%m-%d\'))')
    exec('df.to_csv(\'df' + str(i) + '.csv\')')


    exec('df' + str(i) + '.insert(0, \'Date\', datetime.datetime.today().strftime(\'%Y-%m-%d\'))')
