import pandas as pd
import numpy as np
import glob
import os
pd.set_option('display.expand_frame_repr', False)

# country codes -> want to compare alpha-2 code
path_cc = r"C:\Users\wausa\Work\Data\Countries_And_Codes.csv"
Country_Codes = pd.read_csv(path_cc)

# UK postcodes
path_postcodes = r"C:\Users\wausa\Work\Data\UK_Postcodes.csv"
uk_postcodes = pd.read_csv(path_postcodes)

# list of uk cities to compare and to split UK into countries
path_cities = r"C:\Users\wausa\Work\Data\UK_city_town_info_ONS.csv"
uk_cities = pd.read_csv(path_cities) # lots of dupes i.e. Little London
uk_cities = uk_cities.drop_duplicates('Town/City')






# test AL split -> need to import glob in order to combine the multiple csv files
path = r"C:\Users\wausa\Work\Data\AL_Build_Data"
all_files = glob.glob(os.path.join(path, "Account all global locations build*.csv"))
df_from_each_file = (pd.read_csv(f, low_memory=False) for f in all_files) # get individual dfs as truncated
testdf = pd.concat(df_from_each_file, ignore_index=True)


##################### Need to consider all the different formats of the address as they are not all 5/6 pieces long
# 4     2877 / 5892
# 5     1521
# 6      540
# 3      354
# 2      250
# 7      175
# 1       94
# 8       43
# 9       20
# 10      10 ################# could do one for each address -> or at least fill most common 4, 5, 6, 3

# Notes -> Singapore has structure -> street + country/postcode
# if state/country is in 'City' column, remove and add to 'Area' or something similar
# check same for city in street address for length == 3, if street contains city -> list of world cities?
# When converting alpha code to country -> check if there is a city/state/region in the column and use that to define one of the other columns
# also check city column if it contains PC/region


def parse_address(df):
    if 'Address' in df:
        print('Addresses Found')
    else:
        return print('Error: No \'Address\' Column')

    df = df.assign(Street='', City='', Area='', Post_Code='', Country='')


    # formatting
    df['Address'] = df['Address'].str.replace(',,', ',') # remove duplicated commas
    df['Address'] = df['Address'].str.replace('\n', '') # remove linebreak issue
    df[df.columns] = df[df.columns].apply(lambda x: x.str.strip()) # remove whitespaces from all columns
    df['Address'] = df['Address'].str.replace(' ,', '') # remove empty part of address

    # df['Street'] = df['Address'].str.split(',').str[0]
    # df['Town/City'] = df['Address'].str.split(',').str[1]

    # Global changes
    df.loc[(df['Address'].str.split(',').str.len() > 1), 'Country'] = df['Address'].str.split(',').str[-1]  # make country last line if length > 1
    df.loc[(df['Address'].str.split(',').str.len() == 1), 'Country'] = df['Address'].str.split(',').str[0]  # make country last line if length = 1

    # for length == 6 -> 6 components
    df.loc[(df['Address'].str.split(',').str.len() == 6), 'Street'] = df['Address'].str.split(',').str[0:3].str.join(',')  # make street 1st/2nd/3rd line
    df.loc[(df['Address'].str.split(',').str.len() == 6), 'City'] = df['Address'].str.split(',').str[3]  # make city 4th line

    # for length == 5 -> 5 components
    df.loc[(df['Address'].str.split(',').str.len() == 5), 'Street'] = df['Address'].str.split(',').str[0:2].str.join(',') # add join to append as single string not a list
    df.loc[(df['Address'].str.split(',').str.len() == 5), 'City'] = df['Address'].str.split(',').str[2] # make city 3rd line


    # for length == 4 -> 4 components
    df.loc[(df['Address'].str.split(',').str.len() == 4), 'Street'] = df['Address'].str.split(',').str[0] # make street first line
    df.loc[(df['Address'].str.split(',').str.len() == 4), 'City'] = df['Address'].str.split(',').str[1] # make city first line
    # df.loc[(df['Address'].str.split(',').str.len() == 4),] # If Country = GB PC is -1 + ' ' + -2 part of substring


    # for length == 3 -> 3 components
    df.loc[(df['Address'].str.split(',').str.len() == 3), 'Street'] = df['Address'].str.split(',').str[0] # make street 1st line (includes cities)
    df.loc[(df['Address'].str.split(',').str.len() == 3), 'City'] = df['Address'].str.split(',').str[1] # make street 1st line (includes cities)


    # for length == 2 -> 2 components
    df.loc[(df['Address'].str.split(',').str.len() == 2), 'City'] = df['Address'].str.split(',').str[0] # make city first line -> some are states

    # for len = 1

    # remove whitespaces from all columns
    df[df.columns] = df[df.columns].apply(lambda x: x.str.strip())


    # Postcode
    df['Post_Code'] = np.NAN # make all values NaN
    df.loc[(df['Post_Code'].isna()), 'Post_Code'] = df['Address'].str.extract(r'(\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][ABD-HJLNP-UW-Z]{2}\b)', expand = False) # UK postcodes
    df.loc[(df['Post_Code'].isna()), 'Post_Code'] = df['Address'].str.extract(r'(\d{5}\-?\d{0,4})', expand = False) # Us/US like postcodes
    df.loc[(df['Post_Code'].isna()), 'Post_Code'] = df['Address'].str.extract(r'(\b\w+\s\d{4})', expand = False) # Aus postcode 4 numbers -> maybe only extract from last two parts of string or only if country equals aus?
    df.loc[(df['Post_Code'].isna()), 'Post_Code'] = df['Address'].str.extract(r'(\b\d{4})', expand=False) # New Zealand *** might be similar to Aus
    df.loc[(df['Post_Code'].isna()), 'Post_Code'] = df['Address'].str.extract(r'(\b\d{4})', expand=False) # Sweden
    # word followed by numbers may work for multiple locations including SA for example

    # CCodes copy country to code for length == 2
    # df['Country Code'] = df1['Country'].str.extract('(\s[A-Z]{2}$)', expand = False)
    df['Country Code'] = df['Country'].str.extract(r'([A-Z]{2}$)', expand = False) # get two capital letters of country code
    df = df.merge(Country_Codes[['Country Full', 'Alpha-2 Code']], how = 'left', left_on = 'Country Code', right_on = 'Alpha-2 Code').drop('Alpha-2 Code', axis = 1) # alpha-2 code matches

    df.loc[(df['Country Code'].isna()), 'Country Full'] = df['Country'] # copy value from country if no country code
    # only keep if in list of countries from 'Country Codes'
    # df.loc[(df['Country'].isin(Country_Codes['Country Full'])), 'Country Full'] = Country_Codes['Country Full'] # exact country matches -> is in list of countries

    ###
    # for all countries expect Australia as Name of region is used in postcode, remove city/region names
    # that may appear in the Postcode column before the postcode. Has to come at the
    # end in order to not remove Aus details
    # df.loc[(df['Country Full'] != 'Australia'), 'Post_Code'] = \
    #     df['Post_Code'].str.replace(r'([A-Za-z]{4,}\s)', '')

    # Aus postcodes include region/state *** could apply to other countries***
    df.loc[(df['Country Full'] == 'Australia'), 'Post_Code'] = \
        df['Address'].str.extract(r'(\b[\w ]+\b\d{4}\b)', expand = False)


    ############################################################################# UK enrichment -> postcode/city/country
    # replacing 'United Kingdom' with the specific countries *** could do same for counties
    uk_countries = ['England', 'Scotland', 'Wales', 'Northern Ireland']

    # works for all countries 'uk_countries'
    for x in uk_countries:
        df.loc[(df['Country Full'] == 'United Kingdom') &
                (df['Address'].str.contains(x)), 'Country Full'] = x

    # match postcode -> make sure to remove space when looking to match postcode
    df['Post_Code_2'] = df['Post_Code'].str.replace(' ', '')  # normalise to no space
    uk_postcodes['Post_Code_2'] = uk_postcodes['Postcode'].str.replace(' ', '')  # normalise to no space
    df = pd.merge(df, uk_postcodes[['Post_Code_2', 'County', 'Region', 'Country', 'Latitude', 'Longitude']], how='left', on='Post_Code_2')  # merge on postcode
    df.loc[(df['Country Full'] == 'United Kingdom') & (df['Country_y'].notna()), 'Country Full'] = df['Country_y']  # now replace UK with country
    df = df.drop(['Post_Code_2', 'County', 'Region', 'Country_y', 'Latitude', 'Longitude'], axis=1)  # drop additional columns added by merge
    df = df.rename(columns={'Country_x': 'Country'})  # rename column changed by merge

    # city check
    df = df.merge(uk_cities[['Town/City', 'Country']], how='left', left_on='City', right_on='Town/City')
    df.loc[(df['Country Full'] == 'United Kingdom') & (df['Country_y'].notna()), 'Country Full'] = df['Country_y']
    df = df.drop(['Town/City', 'Country_y'], axis=1)  # drop additional columns added by merge
    df = df.rename(columns={'Country_x': 'Country'})  # rename column changed by merge

    ####################################################################################################################


    return df

 # for longer than 6, maybe extract city, postcode, country explicity,
 # then take the rest as street
 # some postcodes have no space so need to incorporate that

 # want to split UK into Eng/Scot/Wales

df1 = parse_address(testdf)



df1.loc[df1['Country Full'] == 'Australia']
df1['Post_Code'].isna().value_counts()

















# city check -> still 1/3 left without
df1 = df1.merge(uk_cities[['Town/City', 'Country']], how = 'left', left_on = 'City', right_on = 'Town/City')
df1.loc[(df1['Country Full'] == 'United Kingdom') & (df1['Country_y'].notna()), 'Country Full'] = df1['Country_y']
df1 = df1.drop(['Town/City', 'Country_y'], axis = 1) # drop additional columns added by merge
df1 = df1.rename(columns = {'Country_x':'Country'}) # rename column changed by merge

# postcode check
path_postcodes = r"C:\Users\wausa\Work\Data\UK_Postcodes.csv"
uk_postcodes = pd.read_csv(path_postcodes)
# uk_postcodes = uk_postcodes[['Postcode', 'County', 'Region', 'Latitude', 'Longitude']] # just to reduce memory usage

# make sure to remove space when looking to match postcode
df1['Post_Code_2'] = df1['Post_Code'].str.replace(' ', '') # normalise to no space
uk_postcodes['Post_Code_2'] = uk_postcodes['Postcode'].str.replace(' ', '') # normalise to no space
df1 = pd.merge(df1, uk_postcodes[['Post_Code_2', 'County', 'Region', 'Country', 'Latitude', 'Longitude']], how = 'left', on = 'Post_Code_2') # merge on postcode
df1.loc[(df1['Country Full'] == 'United Kingdom') & (df1['Country_y'].notna()), 'Country Full'] = df1['Country_y'] # now replace UK with country
df1 = df1.drop(['Post_Code_2', 'County', 'Region', 'Country_y', 'Latitude', 'Longitude'], axis = 1) # drop additional columns added by merge
df1 = df1.rename(columns = {'Country_x':'Country'}) # rename column changed by merge




df1.loc[df1['Country Full'] == 'United Kingdom']

# just do postcode and see how much it changes -> test inside function



df1.loc[(df1['Country Full'] == 'United Kingdom') & (df1['Post_Code'].notna())]

uk_postcodes.info()





uk_cities['Town/City'].nunique()


df1.loc[(df1['Country Full'] == 'United Kingdom') & (df1['City'].isin(uk_cities['Town/City'])), 'County Full'] =  uk_cities['']

df1.loc[(df1['Country Full'] == 'United Kingdom') & (df1['City'].isin(uk_cities['Town/City']))]


df1.merge(uk_cities, how = 'left', left_on = 'City', right_on = 'Town/City')






df1['City'].isin(uk_cities['Town/City']).value_counts()




df1.loc[df1['Country Full'] == 'United Kingdom']

# How many equal Eng/Wal/Scot and how many equal UK


























df1['Address'].head()


df1.loc[df1['Country Full'] == 'United States', 'CaseSafe Account ID'].nunique()

df1['CaseSafe Account ID (Ignore)'].nunique()


# all locations with countries == UK have cities so compare to cities in list_of_cit
# want to import all UK cities

# for UK countries -> check address to see if one of cities in there?


df1['Address 1'].str.contains(uk_countries[0])

# country check




df1.loc[(df1['Country Full'] == 'United Kingdom')] # 1686 still left




df1.loc[(df1['Country Full'] == 'United Kingdom') &
        (df1['Address 1'].str.extract('(England)') == 'England')]



df1['Address 1'].str.extract('(England)').value_counts()






uk_cities = pd.read_csv(r"C:\Users\wausa\Work\Data\UK_city_town_info_ONS.csv")

uk_cities_list = uk_cities['Town/City'].to_list()

cities_query = '|'.join(uk_cities_list)

df1['Address 1'].str.findall(r'(\b{}\b)'.format(cities_query))[0:50]















########################################################################################################################

# from deepparse.parser import AddressParser
# from deepparse.dataset_container import CSVDatasetContainer
#
# address_parser = AddressParser(model_type="bpemb", device=0)
#
# address_parser(test_df['Address'][0:5])
#
#
# address_parser(test_df['Address'][0:1])
#
#
# address_parser = AddressParser(model_type="fasttext", attention_mechanism=True)
# parse_address = address_parser("350 rue des Lilas Ouest Quebec city Quebec G1L 1B6")
#
