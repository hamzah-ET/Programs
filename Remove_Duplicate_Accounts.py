import numpy as np
import pandas as pd

pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', 101)

df = pd.read_csv(r"C:\Users\wausa\Downloads\Trustmarque_Target_List_01.csv")

df.info()

# df['Account: Account Name'] = df['Account: Account Name'].dropna()
# df['Account Name'].value_counts().sum()


df.drop(df.index[df['Account Name'] == df['Account: Account Name']], inplace = True)

for x in df['Account: Account Name'].dropna():
    if x.isin(df.iloc[0:73, 2]):
        print(x)



df1 = pd.concat([df['Account Name'].append(df['Account: Account Name'])]).reset_index(drop = True).dropna() # combines column data and resets indices

df1 = df1.drop_duplicates(keep = False)

df1.reset_index(drop = True)

df['Combined Account Names'] = df1



df.fillna(0)