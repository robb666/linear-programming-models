import sys
import pandas as pd

print(sys.version)
print(pd.__version__)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

location = "/run/user/1000/gvfs/smb-share:server=192.168.1.12,share=e/Agent baza/2014 BAZA MAGRO.xlsx"

ws = pd.read_excel(location, index_col=None, na_values=['na'], usecols="F:Z,AV")
df = pd.DataFrame(ws)

new_header = df.iloc[1]
df = df[2:]
df.columns = new_header
df = df.rename(index=lambda x: x + 2)

kwoty = df.loc[df['Rozlicz skł. OWCA'] == 'Robert']['Przypis'].sum()

print(kwoty)
