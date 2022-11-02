import pandas as pd
import numpy as np

path = r'C:\Users\wausa\Downloads\report1653401544940.csv'
df = pd.read_csv(path, encoding = 'ISO-8859-1')

df['DueDill Employee Bracket'] = np.nan # adding DueDill brackets

df.info()

df = df[['Account ID', 'Website', 'Sector Grouping', 'Employees', 'DueDill Employees', 'Number of employees on LinkedIn', 'Employee Bracket',
         'DueDill Employee Bracket', 'Linkedin Employee bracket', 'Best Guess Employees']]

df = df.rename(columns = {'Employees': 'Employee Count', 'DueDill Employees': 'DueDill Employee Count',
                     'Number of employees on LinkedIn': 'LinkedIn Employee Count',
                     'Linkedin Employee bracket': 'LinkedIn Employee Bracket', 'Best Guess Employees': 'Best Guess Employee Bracket'})

df.info()

pd.set_option('display.expand_frame_repr', False)

LinkedIn_counts = ['LinkedIn Employee Count'] # could just use index 3:5
LinkedIn_brackets = ['LinkedIn Employee Bracket'] # also here 6:8

employee_counts = ['Employee Count', 'DueDill Employee Count'] # can index employee count instead
employee_brackets = ['Employee Bracket','DueDill Employee Bracket']

########## start
# reformat LI column to put space either side of the dash
df['LinkedIn Employee Bracket'] = df['LinkedIn Employee Bracket'].apply(lambda x: str(x).replace('-', ' - '))
df['LinkedIn Employee Bracket'] = df['LinkedIn Employee Bracket'].apply(lambda x: str(x).replace(',', ''))
df = df.replace('nan', np.NaN) # nan not registering as null so replace
# df['LinkedIn Employee Bracket'].isnull().head(15)

# reformat 2 -10 and 11 - 50 to just 0-50
df.loc[(df['LinkedIn Employee Bracket'] == '2 - 10') | (df['LinkedIn Employee Bracket'] == '11 - 50'), 'LinkedIn Employee Bracket'] = '0 - 50'

for x,y in zip(LinkedIn_counts, LinkedIn_brackets):
    df.loc[(df[y].isnull()) & (df[x] < 51), y] = '0 - 50' # employee bracket is not overwritten and the formatting does not match the new format so can't exactly compare
    df.loc[(df[y].isnull()) & (df[x] > 50) & (df[x] < 201), y] = '51 - 200' # can add line to remove all brackets with no associated count (5545 in total)
    df.loc[(df[y].isnull()) & (df[x] > 200) & (df[x] < 501), y] = '201 - 500'
    df.loc[(df[y].isnull()) & (df[x] > 500) & (df[x] < 1001), y] = '501 - 1000'
    df.loc[(df[y].isnull()) & (df[x] > 1000) & (df[x] < 5001), y] = '1001 - 5000'
    df.loc[(df[y].isnull()) & (df[x] > 5000) & (df[x] < 10001), y] = '5001 - 10000'
    df.loc[(df[y].isnull()) & (df[x] > 10000), y] = '10000+'

df['LinkedIn Employee Bracket'].head(20)

# LinkedIn Bracket now contains initial brackets (pulled from LI) and brackets generated using LinkedIn employee count if no bracket is found
########################### LinkedIn column reformatted and populated ###########################

df['Employee Bracket'] = df['Employee Bracket'].apply(lambda x: str(x).replace('< 49', '0 - 50')) # change < 49 to 0 - 50
# the other bracket ranges do not translate as well


df['Employee Bracket'].head(20)


# reformat brackets for Employee Bracket for those without Employee Count
df['Employee Bracket'] = df['Employee Bracket'].apply(lambda x: str(x).replace('< 49', '0 - 50'))
df['Employee Bracket'] = df['Employee Bracket'].apply(lambda x: str(x).replace('50 - 99', '51 - 250'))
df['Employee Bracket'] = df['Employee Bracket'].apply(lambda x: str(x).replace('100 - 249', '51 - 200'))
df['Employee Bracket'] = df['Employee Bracket'].apply(lambda x: str(x).replace('250 - 499', '201 - 500'))
df['Employee Bracket'] = df['Employee Bracket'].apply(lambda x: str(x).replace('500 - 749', '501 - 1000'))
df['Employee Bracket'] = df['Employee Bracket'].apply(lambda x: str(x).replace('750 - 999', '501 - 1000'))
df['Employee Bracket'] = df['Employee Bracket'].apply(lambda x: str(x).replace('1000 - 2499', '1001 - 5000'))
df['Employee Bracket'] = df['Employee Bracket'].apply(lambda x: str(x).replace('2500 - 4999', '1001 - 5000'))
df['Employee Bracket'] = df['Employee Bracket'].apply(lambda x: str(x).replace('5000 - 7499', '5001 - 10000'))
df['Employee Bracket'] = df['Employee Bracket'].apply(lambda x: str(x).replace('7500 - 9999', '5001 - 10000'))

df = df.replace('nan', np.NaN) # nan not registering as null so replace

# df[(df['Employee Bracket'].notnull()) & (df['Employee Count'].isnull())]


# following will now populate the Employee & DueDill Brackets

for x, y in zip(employee_counts, employee_brackets): # there are multiple companies with no employee count but an employee bracket, currently this
    df.loc[df[x] < 51, y] = '0 - 50' # employee bracket is not overwritten and the formatting does not match the new format so can't exactly compare
    df.loc[(df[x] > 50) & (df[x] < 201), y] = '51 - 200' # can add line to remove all brackets with no associated count (5545 in total)
    df.loc[(df[x] > 200) & (df[x] < 501), y] = '201 - 500'
    df.loc[(df[x] > 500) & (df[x] < 1001), y] = '501 - 1000'
    df.loc[(df[x] > 1000) & (df[x] < 5001), y] = '1001 - 5000'
    df.loc[(df[x] > 5000) & (df[x] < 10001), y] = '5001 - 10000'
    df.loc[df[x] > 10000, y] = '10000+'


df.info()

# populate best guess, firstly via LI, employee and finally DueDill

df.loc[df['LinkedIn Employee Bracket'].notnull(), 'Best Guess Employee Bracket'] = df['LinkedIn Employee Bracket']
df.loc[(df['LinkedIn Employee Bracket'].isnull()) & (df['Employee Bracket'].notnull()), 'Best Guess Employee Bracket'] = df['Employee Bracket']
df.loc[(df['LinkedIn Employee Bracket'].isnull()) & (df['Employee Bracket'].isnull()), 'Best Guess Employee Bracket'] = df['DueDill Employee Bracket']

# Best guess employees now populated!





# confidence metric
df['Confidence'] = ''

df.info()

df.loc[(df['LinkedIn Employee Bracket'].notnull()) & (df['LinkedIn Employee Bracket'] == df['Employee Bracket']) & (df['Employee Bracket'] == df['DueDill Employee Bracket']), 'Confidence'] = 'Very High'

df.loc[(df['LinkedIn Employee Bracket'].notnull()) & (df['LinkedIn Employee Bracket'] == df['Employee Bracket']) & (df['Employee Bracket'] != df['DueDill Employee Bracket']), 'Confidence'] = 'High'
df.loc[(df['LinkedIn Employee Bracket'].notnull()) & (df['LinkedIn Employee Bracket'] == df['DueDill Employee Bracket']) & (df['DueDill Employee Bracket'] != df['Employee Bracket']), 'Confidence'] = 'High'

df.loc[(df['LinkedIn Employee Bracket'].notnull()) & (df['Employee Bracket'].isnull()) & (df['DueDill Employee Bracket'].isnull()), 'Confidence'] = 'Medium' # only LI bracket
df.loc[(df['LinkedIn Employee Bracket'].isnull()) & (df['Employee Bracket'].notnull()) & (df['Employee Bracket'] == df['DueDill Employee Bracket']), 'Confidence'] = 'Medium' # Emp/DD match

df.loc[(df['LinkedIn Employee Bracket'].isnull()) & (df['Employee Bracket'].notnull()) & (df['Employee Bracket'] != df['DueDill Employee Bracket']), 'Confidence'] = 'Low'
df.loc[(df['LinkedIn Employee Bracket'].isnull()) & (df['DueDill Employee Bracket'].isnull()) & (df['Employee Bracket'].notnull()), 'Confidence'] = 'Low'
df.loc[(df['LinkedIn Employee Bracket'].isnull()) & (df['Employee Bracket'].isnull()) & (df['DueDill Employee Bracket'].notnull()), 'Confidence'] = 'Low'

df.loc[(df['LinkedIn Employee Bracket'].isnull()) & (df['Employee Bracket'].isnull()) & (df['DueDill Employee Bracket'].isnull()), 'Confidence'] = np.nan


df.head(50)

df.to_csv('Employee_Count_And_Brackets.csv')

# check any not null in best guess have not null value in confidence