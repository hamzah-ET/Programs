import pandas as pd
pd.set_option('display.expand_frame_repr', False)

# import contacts
contacts = pd.read_csv(r"C:\Users\wausa\Work\Data\SF_Data\Contacts_All_Data.csv", encoding='ISO-8859-1')
contacts = contacts[['CASESAFE_CONTACT_ID__C', 'FIRSTNAME', 'LASTNAME', 'EMAIL', 'PHONE', 'BUSINESS_MOBILE__C', 'MOBILEPHONE', 'OTHERPHONE', 'ALTERNATIVE_NUMBER__C', 'DIRECT_DIAL__C']]

# import accounts
accounts = pd.read_csv(r"C:\Users\wausa\Work\Data\SF_Data\Accounts_All_Data.csv", encoding='ISO-8859-1')
update_accounts = accounts[['CASESAFE_ACCOUNT_ID__C', 'NAME', 'BEST_GUESS_EMPLOYEES__C', 'WEBSITE',]]

path = r"C:\Users\wausa\Downloads\Mel_contact_ids_needed.csv"

webinar_contacts = pd.read_csv(path, encoding='ISO-8859-1') # 2222 contacts
# 'Salutation', 'First Name', 'Last Name', 'Title', 'Account Name', 'Mailing Street', 'Mailing City', 'Mailing State/Province', 'Mailing Zip/Postal Code',
# 'Mailing Country', 'Phone', 'Personal Mobile', 'Email', 'Account Owner'

webinar_contacts['Email'].isna().value_counts() # 814 contacts empty

path_domains = r"C:\Users\wausa\Work\DataScienceTesting\Domains_with_email_structure_and_IDs.csv"

domains_with_emails = pd.read_csv(path_domains, encoding='ISO-8859-1')

webinar_contacts_no_email = webinar_contacts.loc[webinar_contacts['Email'].isna()]





webinar_contacts_no_email = webinar_contacts_no_email.merge(domains_with_emails[['CASESAFE_ACCOUNT_ID__C', 'DOMAIN', 'EMAIL_STRUCTURE']], left_on = 'CaseSafe Account ID',
                                right_on = 'CASESAFE_ACCOUNT_ID__C')


# now add the commands to predict email
# first normalise names
webinar_contacts_no_email['First Name'] = webinar_contacts_no_email['First Name'].str.lower()
webinar_contacts_no_email['Last Name'] = webinar_contacts_no_email['Last Name'].str.lower()
webinar_contacts_no_email['First Name'] = webinar_contacts_no_email['First Name'].str.lower().replace(' ' , '')
webinar_contacts_no_email['Last Name'] = webinar_contacts_no_email['Last Name'].str.lower().replace(' ' , '')

webinar_contacts_no_email['First Name'] = webinar_contacts_no_email['First Name'].str.replace('[^\w\s]','')
webinar_contacts_no_email['Last Name'] = webinar_contacts_no_email['Last Name'].str.replace('[^\w\s]','')


webinar_contacts_no_email['EMAIL_STRUCTURE'].value_counts() #'FN.LN@DOMAIN    489, FLLL@DOMAIN     122, FN@DOMAIN        40, 
# FNLL@DOMAIN      14, FL.LN@DOMAIN     11, FN_LN@DOMAIN      9, FNLN@DOMAIN       4,
# FN.LL@DOMAIN      1'







webinar_contacts_no_email['Email'].isna().value_counts() # check how many fille in
# FN.LN@DOMAIN -> 489 filled in
webinar_contacts_no_email.loc[(webinar_contacts_no_email['Email'].isna()) & (webinar_contacts_no_email['EMAIL_STRUCTURE'] == 'FN.LN@DOMAIN'), 'Email']\
    = webinar_contacts_no_email['First Name'] + '.' + webinar_contacts_no_email['Last Name'] + webinar_contacts_no_email['DOMAIN']

# FLLL@DOMAIN
webinar_contacts_no_email.loc[(webinar_contacts_no_email['Email'].isna()) & (webinar_contacts_no_email['EMAIL_STRUCTURE'] == 'FLLL@DOMAIN'), 'Email']\
    = webinar_contacts_no_email['First Name'].str[0] + webinar_contacts_no_email['Last Name'].str[0] + webinar_contacts_no_email['DOMAIN']

# FN@DOMAIN
webinar_contacts_no_email.loc[(webinar_contacts_no_email['Email'].isna()) & (webinar_contacts_no_email['EMAIL_STRUCTURE'] == 'FN@DOMAIN'), 'Email']\
    = webinar_contacts_no_email['First Name'] + webinar_contacts_no_email['DOMAIN']

# FNLL@DOMAIN
webinar_contacts_no_email.loc[(webinar_contacts_no_email['Email'].isna()) & (webinar_contacts_no_email['EMAIL_STRUCTURE'] == 'FNLN@DOMAIN'), 'Email']\
    = webinar_contacts_no_email['First Name'] + webinar_contacts_no_email['Last Name'].str[0] + webinar_contacts_no_email['DOMAIN']

# FL.LN@DOMAIN
webinar_contacts_no_email.loc[(webinar_contacts_no_email['Email'].isna()) & (webinar_contacts_no_email['EMAIL_STRUCTURE'] == 'FL.LN@DOMAIN'), 'Email']\
    = webinar_contacts_no_email['First Name'].str[0] + '.' + webinar_contacts_no_email['Last Name'] + webinar_contacts_no_email['DOMAIN']

# FN_LN@DOMAIN
webinar_contacts_no_email.loc[(webinar_contacts_no_email['Email'].isna()) & (webinar_contacts_no_email['EMAIL_STRUCTURE'] == 'FN_LN@DOMAIN'), 'Email']\
    = webinar_contacts_no_email['First Name'] + '_' + webinar_contacts_no_email['Last Name'] + webinar_contacts_no_email['DOMAIN']

# FNLN@DOMAIN
webinar_contacts_no_email.loc[(webinar_contacts_no_email['Email'].isna()) & (webinar_contacts_no_email['EMAIL_STRUCTURE'] == 'FNLN@DOMAIN'), 'Email']\
    = webinar_contacts_no_email['First Name'] + webinar_contacts_no_email['Last Name'] + webinar_contacts_no_email['DOMAIN']

# FN.LL@DOMAIN
webinar_contacts_no_email.loc[(webinar_contacts_no_email['Email'].isna()) & (webinar_contacts_no_email['EMAIL_STRUCTURE'] == 'FN.LL@DOMAIN'), 'Email']\
    = webinar_contacts_no_email['First Name'] + '.' + webinar_contacts_no_email['Last Name'].str[0] + webinar_contacts_no_email['DOMAIN']


webinar_contacts_no_email # new emails, need to merge to original

final_contacts = webinar_contacts.append(webinar_contacts_no_email)
final_contacts = final_contacts[final_contacts['Email'].notna()]
final_contacts = final_contacts.drop_duplicates(subset = 'Email')


final_contacts['CaseSafe Contact ID'].nunique()
final_contacts['Email'].nunique()
final_contacts['Email'].isna().value_counts()


final_contacts.to_csv('Contacts_for_Mel_with_emails.csv')








