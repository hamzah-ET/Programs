import pandas as pd

meetings = pd.read_csv(r"C:\Users\wausa\Downloads\report1659020225105.csv", encoding='ISO-8859-1')

df = pd.read_csv(r"C:\Users\wausa\Downloads\report1659020025551.csv", encoding='ISO-8859-1')

meetings_quest = meetings.loc[(meetings['Campaign Name'] == 'Quest Message') | (meetings['Campaign Name'] == 'Quest Nordics')]

df.loc[~meetings_quest['Account: Account ID'].isin(df['Account ID'])]

df.info()

not_in = df.loc[~df['Account ID'].isin(meetings_quest['Account: Account ID'])]

not_in.to_csv('No_quest_meeting.csv')

