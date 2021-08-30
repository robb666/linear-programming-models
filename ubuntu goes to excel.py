import sys
import pandas as pd
from openpyxl import load_workbook

pd.set_option('display.max_rows', None)
# pd.options.display.max_rows = 25
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


print(sys.version)
print(pd.__version__)


# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', 2)

# pd.set_option('display.width', 180)
# # # pd.set_option('display.max_rows', 100)
# pd.set_option('display.max_colwidth', None)

#2014 BAZA MAGRO

location = "/run/user/1000/gvfs/smb-share:server=192.168.1.12,share=e/Agent baza/2014 BAZA MAGRO.xlsx"

# wb = load_workbook(location, data_only=True)


ws = pd.read_excel(location, index_col=None, na_values=['0'], usecols="F:Z")
df = pd.DataFrame(ws)
new_header = df.iloc[1]
df = df[2:]
df.columns = new_header
print(df['Kod'].str.extract(r'(pocztowy)'))
print()

