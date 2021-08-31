import sys
import pandas as pd

print(sys.version)
print(pd.__version__)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

location = "/run/user/1000/gvfs/smb-share:server=192.168.1.12,share=e/Agent baza/2014 BAZA MAGRO.xlsx"

ws = pd.read_excel(location, index_col=None, na_values=['NA'], usecols="A:DB")
df = pd.DataFrame(ws)

new_header = df.iloc[1]
df = df[3:]
df.columns = new_header
df = df.rename(index=lambda x: x + 2)

print(df.head())

OC_2020 = df.loc[(df['Rok przypisu'] == '20_') &
                 (df['Rozlicz skł. OWCA'].isin(['MAGRO', 'Robert'])) &
                 (df['Ryzyko'] == 'OC')]

przychod_OC_2020 = int(OC_2020['MAGRO z Inkasa'].sum())

ilosc_polis = OC_2020['Przypis'].count()

srednia_OC = int(przychod_OC_2020 / ilosc_polis)

print(przychod_OC_2020)
print(ilosc_polis)
print(srednia_OC)




