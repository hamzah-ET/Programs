import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import calendar

accounts = pd.read_csv(r"C:\Users\wausa\Work\Data\SF_Data\Accounts_All_Data.csv", encoding='ISO-8859-1')
contacts = pd.read_csv(r'C:\Users\wausa\Work\Data\SF_Data\Contacts_All_Data.csv', encoding='ISO-8859-1')

############################### LASTACTIVITYDATE -----------------> Last reached out to

contacts['LASTACTIVITYDATE'] = pd.to_datetime(contacts['LASTACTIVITYDATE'])

# get number of contacts with last activity date in the past 30 days and engagement score > 0.05
contacts.loc[(contacts['ENGAGEMENT_SCORE__C'] > 0.05) & (contacts['LASTACTIVITYDATE'] > pd.to_datetime(datetime.today() - timedelta(30)))].shape[0] / (len(contacts)/100)

# for only engagement score > 0.05
contacts.loc[(contacts['ENGAGEMENT_SCORE__C'] > 0.05) & (contacts['LASTACTIVITYDATE'] > pd.to_datetime(datetime.today() - timedelta(30)))].shape[0] / (contacts.loc[(contacts['ENGAGEMENT_SCORE__C'] > 0.05)].shape[0]/100)


# get number of contacts with last activity date in the past 30 days and engagement score < 0.05
contacts.loc[(contacts['ENGAGEMENT_SCORE__C'] < 0.05) & (contacts['LASTACTIVITYDATE'] > pd.to_datetime(datetime.today() - timedelta(30)))].shape[0] / (len(contacts)/100)

# for only engagement score > 0.05
contacts.loc[(contacts['ENGAGEMENT_SCORE__C'] < 0.05) & (contacts['LASTACTIVITYDATE'] > pd.to_datetime(datetime.today() - timedelta(30)))].shape[0] / (contacts.loc[(contacts['ENGAGEMENT_SCORE__C'] < 0.05)].shape[0]/100)





### Accounts
contacts_at_acc = contacts.loc[(contacts['LASTACTIVITYDATE'] > pd.to_datetime(datetime.today() - timedelta(30))), 'ACCOUNTID'].drop_duplicates() # get number of unique
#a accounts from all contacts reached out to

# get number of accounts with a contact with last activity date in the past 30 days and account engagement score > 0.05
accounts.loc[accounts['CASESAFE_ACCOUNT_ID__C'].isin(contacts_at_acc) & (accounts['ENGAGEMENT_SCORE__C'] > 0.05), 'CASESAFE_ACCOUNT_ID__C'].nunique() / (len(accounts)/100)

# for only accounts with engagement score > 0.05
accounts.loc[accounts['CASESAFE_ACCOUNT_ID__C'].isin(contacts_at_acc) & (accounts['ENGAGEMENT_SCORE__C'] > 0.05), 'CASESAFE_ACCOUNT_ID__C'].nunique() / (accounts.loc[(accounts['ENGAGEMENT_SCORE__C'] > 0.05)].shape[0]/100)


# get number of accounts with a contact with last activity date in the past 30 days and account engagement score < 0.05
accounts.loc[accounts['CASESAFE_ACCOUNT_ID__C'].isin(contacts_at_acc) & (accounts['ENGAGEMENT_SCORE__C'] < 0.05), 'CASESAFE_ACCOUNT_ID__C'].nunique() / (len(accounts)/100)

# for only accounts with engagement score > 0.05
accounts.loc[accounts['CASESAFE_ACCOUNT_ID__C'].isin(contacts_at_acc) & (accounts['ENGAGEMENT_SCORE__C'] < 0.05), 'CASESAFE_ACCOUNT_ID__C'].nunique() / (accounts.loc[(accounts['ENGAGEMENT_SCORE__C'] < 0.05)].shape[0]/100)





############################### % of data last worked (12 Months,12-18,18-24, >24), us making progress against our data not getting out of date. ????????

accounts['DATE_TEAM_LAST_WORKED__C'] = pd.to_datetime(accounts['DATE_TEAM_LAST_WORKED__C'])

accounts.loc[(accounts['DATE_TEAM_LAST_WORKED__C'].notnull())].shape[0] / (len(accounts)/100) # 57.7% of accounts have value in

accounts.loc[(accounts['DATE_TEAM_LAST_WORKED__C'] > pd.to_datetime(datetime.today() - timedelta(91))), 'DATE_TEAM_LAST_WORKED__C'].shape[0] # 3 months 6037 accounts

accounts.loc[(accounts['DATE_TEAM_LAST_WORKED__C'] > pd.to_datetime(datetime.today() - timedelta(182))), 'DATE_TEAM_LAST_WORKED__C'].shape[0] # 6 months 48,973 accounts

accounts.loc[(accounts['DATE_TEAM_LAST_WORKED__C'] > pd.to_datetime(datetime.today() - timedelta(273))), 'DATE_TEAM_LAST_WORKED__C'].shape[0] # 9 months 88,951 accounts

accounts.loc[(accounts['DATE_TEAM_LAST_WORKED__C'] > pd.to_datetime(datetime.today() - timedelta(365))), 'DATE_TEAM_LAST_WORKED__C'].shape[0] # 1 year 88,951 accounts (work done in last year)

x = []
for i in range(12, 0, -1):
    x.append(accounts.loc[(accounts['DATE_TEAM_LAST_WORKED__C'] > pd.to_datetime(datetime.today() - timedelta(i*30))), 'DATE_TEAM_LAST_WORKED__C'].shape[0])
x = np.array(x)

plt.plot(x)

accounts.loc[(accounts['DATE_TEAM_LAST_WORKED__C'] < pd.to_datetime(datetime.today() - timedelta(365)))] # zero contacts


x = []
for i in range(0, 130, 1):
    x.append(accounts.loc[(accounts['DATE_TEAM_LAST_WORKED__C'] < (pd.to_datetime(datetime.today() - timedelta(365) + timedelta((i*30))))].shape[0]/(len(accounts)/100)) # zero contacts
x = np.array(x)
y = ['Nov-21', 'Dec-21', 'Jan-22', 'Feb-22', 'Mar-22', 'Apr-22', 'May-22', 'Jun-22', 'Jul-22', 'Aug-22', 'Sep-22', 'Oct-22', 'Nov-22']

plt.plot(y, x, linewidth=3,)
plt.xlabel('Month-Year')
plt.ylabel('% Of Accounts Worked On In The Past 12 Months (As Of The Current Month)')
# plt.fill_between(y[0], y[-1], alpha = 0.3)



