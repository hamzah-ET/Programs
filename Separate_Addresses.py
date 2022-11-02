import pandas as pd
import numpy as np
pd.set_option('display.expand_frame_repr', False)

# country codes -> want to compare alpha-2 code
path_cc = r"C:\Users\wausa\Work\Data\Countries_And_Codes.csv"
Country_Codes = pd.read_csv(path_cc)


# test AL split
testpath = r"C:\Users\wausa\Downloads\Account all global locations build first batch_25_10.csv"
testdf = pd.read_csv(testpath)


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
    if 'Address 1' in df:
        print('Addresses Found')
    else:
        return print('Error: No \'Address\' Column')

    df = df.assign(Street='', City='', Area='', Post_Code='', Country='')


    # formatting
    df['Address 1'] = df['Address 1'].str.replace(',,', ',') # remove duplicated commas
    df['Address 1'] = df['Address 1'].str.replace('\n', '') # remove linebreak issue
    df[df.columns] = df[df.columns].apply(lambda x: x.str.strip()) # remove whitespaces from all columns
    df['Address 1'] = df['Address 1'].str.replace(' ,', '') # remove empty part of address

    # df['Street'] = df['Address 1'].str.split(',').str[0]
    # df['Town/City'] = df['Address 1'].str.split(',').str[1]

    # Global changes
    df.loc[(df['Address 1'].str.split(',').str.len() > 1), 'Country'] = df['Address 1'].str.split(',').str[-1]  # make country last line if length > 1
    df.loc[(df['Address 1'].str.split(',').str.len() == 1), 'Country'] = df['Address 1'].str.split(',').str[0]  # make country last line if length = 1

    # for length == 6 -> 6 components
    df.loc[(df['Address 1'].str.split(',').str.len() == 6), 'Street'] = df['Address 1'].str.split(',').str[0:3].str.join(',')  # make street 1st/2nd/3rd line
    df.loc[(df['Address 1'].str.split(',').str.len() == 6), 'City'] = df['Address 1'].str.split(',').str[3]  # make city 4th line

    # for length == 5 -> 5 components
    df.loc[(df['Address 1'].str.split(',').str.len() == 5), 'Street'] = df['Address 1'].str.split(',').str[0:2].str.join(',') # add join to append as single string not a list
    df.loc[(df['Address 1'].str.split(',').str.len() == 5), 'City'] = df['Address 1'].str.split(',').str[2] # make city 3rd line


    # for length == 4 -> 4 components
    df.loc[(df['Address 1'].str.split(',').str.len() == 4), 'Street'] = df['Address 1'].str.split(',').str[0] # make street first line
    df.loc[(df['Address 1'].str.split(',').str.len() == 4), 'City'] = df['Address 1'].str.split(',').str[1] # make city first line
    # df.loc[(df['Address 1'].str.split(',').str.len() == 4),] # If Country = GB PC is -1 + ' ' + -2 part of substring


    # for length == 3 -> 3 components
    df.loc[(df['Address 1'].str.split(',').str.len() == 3), 'Street'] = df['Address 1'].str.split(',').str[0] # make street 1st line (includes cities)
    df.loc[(df['Address 1'].str.split(',').str.len() == 3), 'City'] = df['Address 1'].str.split(',').str[1] # make street 1st line (includes cities)


    # for length == 2 -> 2 components
    df.loc[(df['Address 1'].str.split(',').str.len() == 2), 'City'] = df['Address 1'].str.split(',').str[0] # make city first line -> some are states


    # remove whitespaces from all columns
    df[df.columns] = df[df.columns].apply(lambda x: x.str.strip())


    # Postcode
    df['Post_Code'] = np.NAN # make all values NaN
    df.loc[(df['Post_Code'].isna()), 'Post_Code'] = df['Address 1'].str.extract(r'(\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][ABD-HJLNP-UW-Z]{2}\b)', expand = False) # UK postcodes
    df.loc[(df['Post_Code'].isna()), 'Post_Code'] = df['Address 1'].str.extract(r'(\d{5}\-?\d{0,4})', expand = False)# Us/US like postcodes

    # CCodes


    # post record format
    # df[(df['Country'].str.len() == 2), 'Country'] = Turn country code into country. If Country is 2 letters long -> change from country code to country
    # df.loc[(df['Country'].str.len() == 2) & (df['Country'].isin(Country_Codes['Alpha-2 Code']))]
    # df = df.merge(Country_Codes[['Country', 'Alpha-2 Code']], left_on = 'Country', right_on = 'Country')

    ###

    return df




df1 = parse_address(testdf)

df1.head(60)

df1['Country'].isin(Country_Codes['Alpha-2 Code']) # if len = 2

df1['Country'].str.len()

df1['Post_Code'].astype(str).str.strip()


df1['Country']












df1["Address 1"].str.extract(r'(\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][ABD-HJLNP-UW-Z]{2}\b)')[0:60] # UK postcode

df1['Address 1'].str.extract(r'(\d{5}\-?\d{0,4})')[0:60] # US postcode

# ned/canada has another rule -? want to compare vs some machine learning tool



df1['Street'].apply(','.join[])

pd.apply(df['Street'].to_string())


df1.loc[(df1['Address 1'].str.split(',').str.len() == 6), 'Address 1'].head(60)

df1[['Address 1', 'Street', 'City', 'Area', 'Region', 'Post_Code', 'Country']].head(20)


# maybe check how many cities we can just merge from DB





test_df[2].isin(Country_Codes['Alpha-2 Code'])




pd.options.display.max_colwidth = 100

testdf.loc[(testdf['Address 1'].str.split(',').str.len() == 2), 'Address 1'][0:50]

### validate all countries/regions? compare to country data











locdf[['Street', 'City', 'County  State', 'Postcode', 'Country']]

# path_cities_UK = r"C:\Users\wausa\Work\Data\UK_Locations_With_Regions.csv"
# path_cities_UK_ONS = r"C:\Users\wausa\Work\Data\UK_city_town_info_ONS.csv"

path_cities_towns = r"C:\Users\wausa\Work\DataScienceTesting\UK_city_town_info_ONS.csv"
path_cities_towns_sub = r"C:\Users\wausa\Work\DataScienceTesting\UK_city_town_suburbanarea_info_ONS.csv"

uk_cities = pd.read_csv(path_cities_towns)
uk_cities_ons = pd.read_csv(path_cities_towns_sub)


locdf.loc[(locdf['Country'] == 'United Kingdom')]
locdf.loc[(locdf['Country'] == 'United Kingdom') & (~locdf['City'].isin(uk_cities['NAME1']))]


locdf.loc[(locdf['Country'] == 'Wales')]
locdf.loc[(locdf['Country'] == 'United Kingdom') & (~locdf['City'].isin(uk_cities_ons['NAME1']))] # 341/421 towns found in ONS data


locdf['Country'].value_counts()[0:40]

# couls plit and check how well matches country or city or ...


locdf # don't have structure from this
# linkedin locations seeem to be well structured, separated by commas




# test AL split
testpath = r"C:\Users\wausa\Work\Data\test_AL_address_split.csv"

test_df = pd.read_csv(testpath)
# want to do regex split then maybe compare to database -> make list of lines and then check if compares to list
test_df

# test_df['Address_Lines'] = test_df.Address.str.split(',')

# import list of cities/countries
uk_cities = pd.read_csv(path_cities_towns)
uk_cities_ons = pd.read_csv(path_cities_towns_sub)

# check max number of ',' in order to determine number of columns to have
# get list of country

test_df = test_df.join(test_df.Address.str.split(',', expand = True))

# before doing any comparison we need to ensure all whitespaces are removed

cols = [0, 1, 2, 3]
test_df[cols] = test_df[cols].apply(lambda x: x.str.strip())# remove whitespaces

test_df[2].isin(Country_Codes['Alpha-2 Code'])
test_df[3].isin(Country_Codes['Alpha-2 Code'])
test_df[4].isin(Country_Codes['Alpha-2 Code'])

test_df['Address']
test_df['Street'] = test_df[0]
test_df['City'] = test_df[1]
# maybe have rule based on country or by identifying string of numbers/letters
test_df['Region'] = test_df[2]

test_df[2].str.extract(r'(\d{5}\-?\d{0,4})').notna().value_counts()

[i[-1] for i in test_df[2].str.split(' ').values] # pulls last combination of letters and words



















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
