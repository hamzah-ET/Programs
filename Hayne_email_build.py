import pandas as pd
import glob
import os
pd.set_option('display.expand_frame_repr', False)

# path = r'C:\Users\wausa\Work\DataScienceTesting\Hayne_Task_10_22'

accounts = pd.read_csv(r"C:\Users\wausa\Work\Data\SF_Data\Accounts_All_Data.csv", encoding='ISO-8859-1')
contacts = pd.read_csv(r"C:\Users\wausa\Work\Data\SF_Data\Contacts_All_Data.csv", encoding='ISO-8859-1')



hayne_build = pd.read_csv(r"C:\Users\wausa\Work\DataScienceTesting\Hayne_Task_10_22\Combined_csv.csv")
hayne_build['First Name'].str.replace('/', '')
hayne_build['Last Name'].str.replace('/', '')

hayne_build['Contact Email Address'].isna().value_counts()



hayne_build_with_emails = hayne_build.loc[hayne_build['Contact Email Address'].notna()]
hayne_build_no_emails = hayne_build.loc[hayne_build['Contact Email Address'].isna()] # All accounts here are uniqiue and no emails from those accounts are found in the comb csv




hayne_build.loc[(hayne_build['Account ID'].isin(accounts['CASESAFE_ACCOUNT_ID__C']))] # none found
hayne_build.loc[(hayne_build['Account Name'].isin(accounts['NAME']))] # 4800 found


hayne_build_no_emails.loc[(hayne_build['Account Name'].isin(accounts['NAME']))] # 1281/1288 accounts matched to db

# import domain email topologies
path_topologies = r"C:\Users\wausa\Work\DataScienceTesting\Domains_with_email_structure_and_IDs.csv"
structures = pd.read_csv(path_topologies) # 47196 accounts


hayne_build_no_emails.loc[(hayne_build_no_emails['Account Name'].isin(structures['NAME']))] # 906 account names found in email structures list

import os
os.chdir(r'C:\Users\wausa\Work\DataScienceTesting\Hayne_Task_10_22')
hayne_build_no_emails.to_csv('hayne_build_no_emails.csv') # export contacts with no emails -> keep an eye on and compare to those



hayne_build_no_emails_with_domains = pd.merge(hayne_build_no_emails, structures[['NAME', 'DOMAIN', 'EMAIL_STRUCTURE']], left_on = 'Account Name',
                                              right_on = 'NAME',) # merge to get all emails with domains 1288 -> 1005 emails


hayne_build_no_emails_no_domains = pd.merge(hayne_build_no_emails, structures[['NAME', 'DOMAIN', 'EMAIL_STRUCTURE']], left_on = 'Account Name',
                                              right_on = 'NAME', how = 'inner') # merge to get all emails with domains 1288 -> 1005 emails



###################need to get emails with no domain match, see what I can do there whilst verifying other emails?###########################


hayne_build_no_emails_with_domains.to_csv('hayne_build_no_emails_with_domains.csv')



########################################################################################################################################## normalise to build emails
hayne_build_no_emails_with_domains['First Name'] = hayne_build_no_emails_with_domains['First Name'].str.lower()
hayne_build_no_emails_with_domains['Last Name'] = hayne_build_no_emails_with_domains['Last Name'].str.lower()
hayne_build_no_emails_with_domains['First Name'] = hayne_build_no_emails_with_domains['First Name'].str.lower().replace(' ' , '')
hayne_build_no_emails_with_domains['Last Name'] = hayne_build_no_emails_with_domains['Last Name'].str.lower().replace(' ' , '')

hayne_build_no_emails_with_domains['First Name'] = hayne_build_no_emails_with_domains['First Name'].str.replace('[^\w\s]','')
hayne_build_no_emails_with_domains['Last Name'] = hayne_build_no_emails_with_domains['Last Name'].str.replace('[^\w\s]','')

####################################################################################################################################################################


####################################################################################################################################################### build emails
# FN.LN@DOMAIN
hayne_build_no_emails_with_domains.loc[(hayne_build_no_emails_with_domains['Contact Email Address'].isna()) & (hayne_build_no_emails_with_domains['EMAIL_STRUCTURE'] ==
                                                                                               'FN.LN@DOMAIN'), 'Contact Email Address'] = \
    hayne_build_no_emails_with_domains['First Name'] + '.' + hayne_build_no_emails_with_domains['Last Name'] + hayne_build_no_emails_with_domains['DOMAIN']

# FL.LN@DOMAIN
hayne_build_no_emails_with_domains.loc[(hayne_build_no_emails_with_domains['Contact Email Address'].isna()) & (hayne_build_no_emails_with_domains['EMAIL_STRUCTURE'] == 'FL.LN@DOMAIN'), 'Contact Email Address']\
    = hayne_build_no_emails_with_domains['First Name'].str[0] + '.' + hayne_build_no_emails_with_domains['Last Name'] + hayne_build_no_emails_with_domains['DOMAIN']

# FLLN@DOMAIN
hayne_build_no_emails_with_domains.loc[(hayne_build_no_emails_with_domains['Contact Email Address'].isna()) & (hayne_build_no_emails_with_domains['EMAIL_STRUCTURE'] == 'FLLN@DOMAIN'), 'Contact Email Address']\
    = hayne_build_no_emails_with_domains['First Name'].str[0] + hayne_build_no_emails_with_domains['Last Name'] + hayne_build_no_emails_with_domains['DOMAIN']

# FN.LL@DOMAIN
hayne_build_no_emails_with_domains.loc[(hayne_build_no_emails_with_domains['Contact Email Address'].isna()) & (hayne_build_no_emails_with_domains['EMAIL_STRUCTURE'] == 'FN.LL@DOMAIN'), 'Contact Email Address']\
    = hayne_build_no_emails_with_domains['First Name'] + '.' + hayne_build_no_emails_with_domains['Last Name'].str[0] + hayne_build_no_emails_with_domains['DOMAIN']

# FN@DOMAIN
hayne_build_no_emails_with_domains.loc[(hayne_build_no_emails_with_domains['Contact Email Address'].isna()) & (hayne_build_no_emails_with_domains['EMAIL_STRUCTURE'] == 'FN@DOMAIN'), 'Contact Email Address']\
    = hayne_build_no_emails_with_domains['First Name'] + hayne_build_no_emails_with_domains['DOMAIN']

# FLL@DOMAIN
hayne_build_no_emails_with_domains.loc[(hayne_build_no_emails_with_domains['Contact Email Address'].isna()) & (hayne_build_no_emails_with_domains['EMAIL_STRUCTURE'] == 'FLLL@DOMAIN'), 'Contact Email Address']\
    = hayne_build_no_emails_with_domains['First Name'].str[0] + hayne_build_no_emails_with_domains['Last Name'].str[0] + hayne_build_no_emails_with_domains['DOMAIN']

# FN_LN@DOMAIN
hayne_build_no_emails_with_domains.loc[(hayne_build_no_emails_with_domains['Contact Email Address'].isna()) & (hayne_build_no_emails_with_domains['EMAIL_STRUCTURE'] == 'FN_LN@DOMAIN'), 'Contact Email Address']\
    = hayne_build_no_emails_with_domains['First Name'] + '_' + hayne_build_no_emails_with_domains['Last Name'] + hayne_build_no_emails_with_domains['DOMAIN']

# FNLN@DOMAIN
hayne_build_no_emails_with_domains.loc[(hayne_build_no_emails_with_domains['Contact Email Address'].isna()) & (hayne_build_no_emails_with_domains['EMAIL_STRUCTURE'] == 'FNLN@DOMAIN'), 'Contact Email Address']\
    = hayne_build_no_emails_with_domains['First Name'] + hayne_build_no_emails_with_domains['Last Name'] + hayne_build_no_emails_with_domains['DOMAIN']

# FNLL@DOMAIN
hayne_build_no_emails_with_domains.loc[(hayne_build_no_emails_with_domains['Contact Email Address'].isna()) & (hayne_build_no_emails_with_domains['EMAIL_STRUCTURE'] == 'FNLL@DOMAIN'), 'Contact Email Address']\
    = hayne_build_no_emails_with_domains['First Name'] + hayne_build_no_emails_with_domains['Last Name'].str[0] + hayne_build_no_emails_with_domains['DOMAIN']

####################################################################################################################################################################


hayne_build_no_emails_with_domains.loc[hayne_build_no_emails_with_domains['Contact Email Address'].isna()] # includes 40+ empty named contacts, need to be removed
hayne_build_no_emails_with_domains = hayne_build_no_emails_with_domains.loc[~hayne_build_no_emails_with_domains['Contact Email Address'].isna()] # remove no names


hayne_build_no_emails_with_domains.to_csv('hayne_build_no_emails_with_domains.csv') # to csv

#################################################################
from verify_email import verify_email
verify_email('david.critchley@beumergroup.com', debug = True)

import pandas as pd
hayne_build_no_emails_with_domains = pd.read_csv(r"C:\Users\wausa\Work\DataScienceTesting\Hayne_Task_10_22\hayne_build_no_emails_with_domains.csv")

import os
os.chdir(r'C:\Users\wausa\Work\DataScienceTesting\Hayne_Task_10_22') #######################################
import datetime
def sleep(num):
    for i in range(num):
        print("\rTime remaining: {} seconds.".format(num - i), end='')
        time.sleep(1)
import time

for i in range(0, 11):
    exec('email' + str(i) + ' = hayne_build_no_emails_with_domains[\'Contact Email Address\'][i*100:(i+1)*100]')
    # exec('verified' + str(i) + ' = verify_email(all_emails[\'EMAIL\'][label' + str(i) + '[0]:label' + str(i) + '[-1]+1].to_list())')
    exec('verified' + str(i) + ' = verify_email(email' + str(i) + '.to_list())')
    sleep(5)
    exec('df' + str(i) + ' = pd.DataFrame({\'Email\':email' + str(i) + ', \'Verified\':verified' + str(i) + '})')
    exec('df' + str(i) + '.insert(0, \'Date\', datetime.datetime.today().strftime(\'%Y-%m-%d\'))')
    exec('df' + str(i) + '.to_csv(r\'df' + str(i) + '.csv\')')





hayne_build_no_emails_with_domains = pd.read_csv(r"C:\Users\wausa\Work\DataScienceTesting\Hayne_Task_10_22\hayne_build_no_emails_with_domains.csv") # now with emails/verif

structures['EMAIL_STRUCTURE'].value_counts()

# FN.LN@DOMAIN    28484
# FLLL@DOMAIN      9731
# FN@DOMAIN        4168
# FL.LN@DOMAIN     1839
# FNLN@DOMAIN      1312
# FNLL@DOMAIN      1035
# FN_LN@DOMAIN      507
# FN.LL@DOMAIN      120

# summary -> roughly 1400 emails empty -> 1088 contacts associated to existing account in our DB, after removing empty contacts (no names)
# leaves us with 962 contacts with account/domain in structues (list of email topologies) and around 350 emails that are not (95% associated to account in
# crm but unfortunately there are no emails on the accounts to get a domain/topology for predicting contacts -> need to guess them

hayne_build_no_emails_with_domains.loc[(hayne_build_no_emails_with_domains['Verified'] == True)] # 465/962 true so far -> around half verified

hayne_build_no_emails_with_domains.loc[(hayne_build_no_emails_with_domains['Verified'] == False)]




hayne_build_no_emails.loc[hayne_build_no_emails['First Name'] == '/']

hayne_build_no_emails_with_domains





verify_email('dchilton@ametek.co.uk', debug = True)


























############################# emails without associated domains

hayne_build_no_emails_without_domains = hayne_build_no_emails.loc[~(hayne_build_no_emails['Account Name'].isin(structures['NAME']))]


hayne_build_no_emails_without_domains['First Name'].notna().value_counts()
hayne_build_no_emails_without_domains.to_csv('hayne_build_no_emails_without_domains.csv')


structures['EMAIL_STRUCTURE'].value_counts()


hayne_build_no_emails_without_domains = pd.read_csv(r"C:\Users\wausa\Work\DataScienceTesting\Hayne_Task_10_22\hayne_build_no_emails_without_domains.csv")


hayne_build_no_emails_without_domains['Account Name'].isin(accounts['NAME']).value_counts() # 375/382 found in accounts so check number of contacts/emails for each acc

# number of contacts = 'NUMBER_OF_CONTACTS__C'
accounts.loc[(accounts['NAME'].isin(hayne_build_no_emails_without_domains['Account Name'])), ['NAME', 'NUMBER_OF_CONTACTS__C']] # check number of contacts -> no email data

# no email data so worth checking through different emails, basically guess email
hayne_build_no_emails_without_domains['Domain'] = ''
hayne_build_no_emails_without_domains['Email_Structure'] = ''

hayne_build_no_emails_without_domains.to_csv('hayne_build_no_emails_without_domains.csv')
