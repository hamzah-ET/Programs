import pandas as pd

pd.read_csv(r"C:\Users\wausa\Work\DataScienceTesting\domains_with_email_structure.csv")


contact_labels = pd.read_csv(r"C:\Users\wausa\Work\Data\Object_Fields\Contact_Fields.csv")

field_usage = pd.read_excel(r"C:\Users\wausa\Work\Documents\Legacy_Field_Deletion_Profiles.xlsx", 'DataHub_Contacts')

contact_labels.info()
field_usage.info()

field_usage.loc[field_usage['Name'].isin(contact_labels['Field API Name'].str.lower())]

contact_labels['Field API Name'] = contact_labels['Field API Name'].str.lower()

field_usage[['Name', 'Field Names']].merge(contact_labels[['Field API Name', 'Label']], left_on = 'Name', right_on =
                                         'Field API Name')

labels = field_usage[['Name', 'Field Names']].merge(contact_labels[['Field API Name', 'Label']], left_on = 'Name', right_on =
                                         'Field API Name')

import os
os.chdir(r"C:\Users\wausa\Downloads")
labels.to_csv('labels.csv')


