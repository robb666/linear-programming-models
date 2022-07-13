
import sys
import pandas as pd
from pulp import *

print(sys.version)
print(pd.__version__)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

location = "/run/user/1000/gvfs/smb-share:server=192.168.1.12,share=e/Agent baza/2014 BAZA MAGRO.xlsm"

ws = pd.read_excel(location, index_col=None, na_values=['NA'], usecols="A:DB")
df = pd.DataFrame(ws)

new_header = df.iloc[1]

df = df[3:]
df.columns = new_header
df = df.rename(index=lambda x: x + 2)

print(df.head(300))

