import pandas as pd
pd.set_option('display.expand_frame_repr', False)
path = r"C:\Users\wausa\Work\Data\SF_Data\Accounts_All_Data.csv"
path1 = r"C:\Users\wausa\Work\Data\SF_Data\Account_Locations_All_Data.csv"
accounts = pd.read_csv(path)
account_locations = pd.read_csv(path1)


accounts['ENGAGEMENT_SCORE__C'] # E_score

# want account location info, build out account location
accounts = accounts[['CASESAFE_ACCOUNT_ID__C', 'NAME', 'ENGAGEMENT_SCORE__C','NUMBER_OF_LOCATIONS__C']]




accounts = accounts.sort_values('ENGAGEMENT_SCORE__C', ascending = False)



accounts_filled = accounts.loc[accounts['NUMBER_OF_LOCATIONS__C'] > 1][0:500]
accounts_unfilled = accounts.loc[accounts['NUMBER_OF_LOCATIONS__C'] < 2][0:500]



# many locations
accounts_filled = accounts_filled.merge(account_locations[['ACCOUNT__C', 'LOCATION_FULL_ADDRESS__C']],
                    left_on = 'CASESAFE_ACCOUNT_ID__C',
                    right_on = 'ACCOUNT__C')

accounts_filled_listed = accounts_filled.groupby('CASESAFE_ACCOUNT_ID__C')['LOCATION_FULL_ADDRESS__C']\
    .apply(list).reset_index(name = 'All_Locations')

accounts_filled = accounts_filled.merge(accounts_filled_listed,
                                        left_on='CASESAFE_ACCOUNT_ID__C',
                                        right_on='CASESAFE_ACCOUNT_ID__C').drop_duplicates('CASESAFE_ACCOUNT_ID__C')


# only 1 or zero locations
accounts_unfilled = accounts_unfilled.merge(account_locations[['ACCOUNT__C', 'LOCATION_FULL_ADDRESS__C']],
                    left_on = 'CASESAFE_ACCOUNT_ID__C',
                    right_on = 'ACCOUNT__C')


accounts_filled.to_csv('accounts_with_multiple_locations_for_serbia.csv')
accounts_unfilled.to_csv('accounts_without_multiple_locations_for_serbia.csv')