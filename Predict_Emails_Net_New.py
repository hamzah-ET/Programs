from verify_email import verify_email
import os
from datetime import datetime
import numpy as np
import pandas as pd
import time
import datetime

pd.set_option('display.expand_frame_repr', False) # see all rows

# function to display timer/delay. Delay allows pinging domains to be more accurate
def sleep(num):
    for i in range(num):
        print("\rTime remaining: {} seconds.".format(num - i), end='')
        time.sleep(1) # #

def read_file(df):
    # File should take the form: 'CaseSafe Account ID', 'CaseSafe Contact ID' (If available)
    # 'First Name', 'Last Name', 'Account Name', 'Domain' (Must haves) -> scope to change domain to website if website == @'domain'
    # Will add email structures as column headers and then True/False for each and verification date

    df = df.assign(Predicted_Email = '', Verified = '', Verification_Date = '')

    if 'Domain' not in df.columns:
        df['Website'] = df['Website'].str.replace('www.', '')
        df['Website'] = df['Website'].str.split('/').str[0]
        df['Website'] = '@' + df['Website'] #
        df.rename({'Website':'Domain'}, axis = 1, inplace = True) # rename column


    df['FN.LN@DOMAIN'] = df.loc[(df['Predicted_Email'].isna()), 'FN.LN@DOMAIN'] = df['First Name'] + '.' + df['Last Name'] + df['Domain']
    df['FNLN@DOMAIN'] = df.loc[(df['Predicted_Email'].isna()), 'FNLN@DOMAIN'] = df['First Name'] + df['Last Name'] + df['Domain']
    df['FN_LN@DOMAIN'] = df.loc[(df['Predicted_Email'].isna()), 'FN_LN@DOMAIN'] = df['First Name'] + '_' + df['Last Name'] + df['Domain']
    df['FLLN@DOMAIN'] = df.loc[(df['Predicted_Email'].isna()), 'FLLN@DOMAIN'] = df['First Name'].str[0] + df['Last Name'] + df['Domain']
    df['FL.LN@DOMAIN'] = df.loc[(df['Predicted_Email'].isna()), 'FL.LN@DOMAIN'] = df['First Name'].str[0] + '.' + df['Last Name'] + df['Domain']
    df['FNLL@DOMAIN'] = df.loc[(df['Predicted_Email'].isna()), 'FNLL@DOMAIN'] = df['First Name'] + df['Last Name'].str[0] + df['Domain']
    ######
    df['FLLL@DOMAIN'] = df.loc[(df['Predicted_Email'].isna()), 'FLLL@DOMAIN'] = df['First Name'].str[0] + df['Last Name'].str[0] + df['Domain']
    df['FN@DOMAIN'] = df.loc[(df['Predicted_Email'].isna()), 'FN@DOMAIN'] = df['First Name'] + df['Domain']
    df['FN.LL@DOMAIN'] = df.loc[(df['Predicted_Email'].isna()), 'FN.LL@DOMAIN'] = df['First Name'] + '.' + df['Last Name'].str[0] + df['Domain']


    ### start email verification
    df.loc[(df['FN.LN@DOMAIN'].apply(verify_email) == True), 'Verified'] = 'FN.LN@DOMAIN'
    df.loc[(df['Verified'] == 'FN.LN@DOMAIN'), 'Predicted_Email'] = df['FN.LN@DOMAIN']
    sleep(3)

    df.loc[(df['Verified'] == '') & (df['FNLN@DOMAIN'].apply(verify_email) == True), 'Verified'] = 'FNLN@DOMAIN'
    df.loc[(df['Verified'] == 'FNLN@DOMAIN'), 'Predicted_Email'] = df['FNLN@DOMAIN']
    sleep(3)

    df.loc[(df['Verified'] == '') & (df['FN_LN@DOMAIN'].apply(verify_email) == True), 'Verified'] = 'FN_LN@DOMAIN'
    df.loc[(df['Verified'] == 'FN_LN@DOMAIN'), 'Predicted_Email'] = df['FN_LN@DOMAIN']
    sleep(3)

    df.loc[(df['Verified'] == '') & (df['FLLN@DOMAIN'].apply(verify_email) == True), 'Verified'] = 'FLLN@DOMAIN'
    df.loc[(df['Verified'] == 'FLLN@DOMAIN'), 'Predicted_Email'] = df['FLLN@DOMAIN']
    sleep(3)

    df.loc[(df['Verified'] == '') & (df['FL.LN@DOMAIN'].apply(verify_email) == True), 'Verified'] = 'FL.LN@DOMAIN'
    df.loc[(df['Verified'] == 'FL.LN@DOMAIN'), 'Predicted_Email'] = df['FL.LN@DOMAIN']
    sleep(3)

    df.loc[(df['Verified'] == '') & (df['FNLL@DOMAIN'].apply(verify_email) == True), 'Verified'] = 'FNLL@DOMAIN'
    df.loc[(df['Verified'] == 'FNLL@DOMAIN'), 'Predicted_Email'] = df['FNLL@DOMAIN']
    sleep(3)

    #####
    df.loc[(df['Verified'] == '') & (df['FLLL@DOMAIN'].apply(verify_email) == True), 'Verified'] = 'FLLL@DOMAIN'
    df.loc[(df['Verified'] == 'FLLL@DOMAIN'), 'Predicted_Email'] = df['FLLL@DOMAIN']
    sleep(3)

    df.loc[(df['Verified'] == '') & (df['FN@DOMAIN'].apply(verify_email) == True), 'Verified'] = 'FN@DOMAIN'
    df.loc[(df['Verified'] == 'FN@DOMAIN'), 'Predicted_Email'] = df['FN@DOMAIN']
    sleep(3)

    df.loc[(df['Verified'] == '') & (df['FN.LL@DOMAIN'].apply(verify_email) == True), 'Verified'] = 'FN.LL@DOMAIN'
    df.loc[(df['Verified'] == 'FN.LL@DOMAIN'), 'Predicted_Email'] = df['FN.LL@DOMAIN']

    df['Verification_Date'] = datetime.datetime.today().strftime('%Y-%m-%d') # get date of verification

    df.loc[(df['Last Name'].str.len() == 1), 'Initial_Only'] = 'Y'

    return df

# if __name__ == "__main__" :
#     print('abc')

path = r"C:\Users\wausa\Work\DataScienceTesting\test_email_pred.csv"
df = pd.read_csv(path)

df1 = read_file(df[5:10])

print(df1)



# import os
# os.chdir(r'C:\Users\wausa\Work\DataScienceTesting\Hayne_Task_10_22')
# df1.to_csv('final_hayne_contacts.csv')


# df1.to_csv('test_' + datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + '.csv')
#
# print(df1)
#





