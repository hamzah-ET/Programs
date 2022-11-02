import pandas as pd
import glob
import os

headers = pd.read_csv(r"C:\Users\wausa\Downloads\opname_csv_gb\Doc\OS_Open_Names_Header.csv")
path = r"C:\Users\wausa\Downloads\opname_csv_gb\Data"

all_files = glob.glob(os.path.join(path, "*.csv")) # advisable to use os.path.join as this makes concatenation OS independent

df_from_each_file = (pd.read_csv(f, low_memory=False) for f in all_files)
concatenated_df = pd.concat(df_from_each_file, ignore_index=True)

pd.read_csv(r'C:\\Users\\wausa\\Downloads\\opname_csv_gb\\Data\\HW62.csv')

df = []
for filename in all_files:
    df1 = pd.read_csv(filename, header = None)
    df.append(df1)

df = pd.concat(df)

df.to_csv('All_OS_Data_Locations.csv')

# reload all_data file
all_data = pd.read_csv(r"C:\Users\wausa\Work\DataScienceTesting\All_OS_Data_Locations.csv")

all_data = all_data.drop('Unnamed: 0', axis = 1) # remove index column to allow match

all_data.columns = headers.columns # get headers from header file

all_data.columns

all_data['LOCAL_TYPE'].value_counts()[0:10]

all_data.loc[all_data['NAME1'] == 'Maidstone', 'LOCAL_TYPE']

# Name1, COUNTRY


UK_Cities = all_data.loc[(all_data['LOCAL_TYPE'] == 'City') | (all_data['LOCAL_TYPE'] == 'Town') |
                         (all_data['LOCAL_TYPE'] == 'Suburban Area'), ['NAME1', 'COUNTY_UNITARY', 'REGION', 'COUNTRY']]

UK_Cities_towns = all_data.loc[(all_data['LOCAL_TYPE'] == 'City') | (all_data['LOCAL_TYPE'] == 'Town'),
                         ['NAME1', 'COUNTY_UNITARY', 'REGION', 'COUNTRY']]


UK_Cities.to_csv('UK_city_town_suburbanarea_info_ONS.csv')

UK_Cities_towns.to_csv('UK_city_town_info_ONS.csv')





SELECT ApiVersion,CreatedById,CreatedDate,EventType,Id,
IsDeleted,LastModifiedById,LastModifiedDate,LogDate,LogFile,LogFileContentType,LogFileFieldNames,LogFileFieldTypes,LogFileLength,SystemModstamp FROM EventLogFile


SELECT LogFile, EventType, CreatedDate FROM EventLogFile WHERE EventType IN ('API', 'RestApi', 'ApiTotalUsage')
