import pandas as pd
pd.set_option("display.max_rows", 100)
pd.set_option("display.max_columns", 8)
df = pd.read_csv('orders.csv')
df.fillna(0, inplace=True)
print(df)

import pandas as pd


'''
new_df = df.dropna()

print(new_df.to_string())'''

import pandas as pd
import pandas as pd

'''

df.dropna(inplace = True)

print(df.to_string())

'''
import pandas as pd



df.fillna(130, inplace = True)