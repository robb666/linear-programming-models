
import sys
import pandas as pd
from pulp import *

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

rok = '20_'
rok_przypisu = (df['Rok przypisu'] == rok)
OFWCA = (df['Rozlicz skł. OWCA'].isin(['MAGRO', 'Robert']))

OC = df.loc[rok_przypisu & OFWCA & (df['Ryzyko'] == 'OC')]
AC = df.loc[rok_przypisu & OFWCA & (df['Ryzyko'] == 'AC')]
OCAC = df.loc[rok_przypisu & OFWCA & (df['Ryzyko'].isin(['OCAC', 'OC AC']))]
dom = df.loc[rok_przypisu & OFWCA & (df['Ryzyko'].isin(['mie', 'dom', 'dom ', 'mur', 'bud', 'domb', 'dlet']))]
firma = df.loc[rok_przypisu & OFWCA & (df['Ryzyko'].isin(['firma', 'kabotaż']))]
oc = df.loc[rok_przypisu & OFWCA &
            (df['Ryzyko'].isin(['ocag', 'ocbrach', 'occ', 'ocdiag', 'ocfizjoter', 'ocim', 'ocistr', 'oclek',
                                 'ocmed', 'ocnau', 'ocpie', 'ocpk', 'ocpm', 'ocpry', 'ocpzaw', 'ocrzmaj',
                                 'ocsped', 'ocsport', 'octren', 'ocwych', 'oczaw', 'oczoz', 'oczpr', 'oczpr ']))]
kl = df.loc[rok_przypisu & OFWCA & (df['Ryzyko'].isin(['kl', 'klc']))]
zycie = df.loc[rok_przypisu & OFWCA &
               (df['Ryzyko'].isin(['GO', 'GO+', 'GPR', 'GO55', 'życie', 'na życie', 'WDCIR', 'WDCIR2', 'WDCIR3']))]
inne = df.loc[rok_przypisu & OFWCA &
              (df['Ryzyko'].isin(['ASS', 'gwa', 'gwa NWK', 'gwa UWiU', 'jacht', 'nnw', 'nnwszk', 'NWk', 'rol']))]

przychod_OC = int(OC['MAGRO z Inkasa'].sum())
ilosc_polis_OC = OC['Przypis'].count()
srednia_OC = int(przychod_OC / ilosc_polis_OC)

przychod_AC = int(AC['MAGRO z Inkasa'].sum())
ilosc_polis_AC = AC['Przypis'].count()
srednia_AC = int(przychod_AC / ilosc_polis_AC)

przychod_OCAC = int(OCAC['MAGRO z Inkasa'].sum())
ilosc_polis_OCAC = OCAC['Przypis'].count()
srednia_OCAC = int(przychod_OCAC / ilosc_polis_OCAC)

przychod_dom = int(dom['MAGRO z Inkasa'].sum())
ilosc_polis_dom = dom['Przypis'].count()
srednia_dom = int(przychod_dom / ilosc_polis_dom)

przychod_firma = int(firma['MAGRO z Inkasa'].sum())
ilosc_polis_firma = firma['Przypis'].count()
srednia_firma = int(przychod_firma / ilosc_polis_firma)

przychod_oc = int(oc['MAGRO z Inkasa'].sum())
ilosc_polis_oc = oc['Przypis'].count()
srednia_oc = int(przychod_oc / ilosc_polis_oc)

przychod_kl = int(kl['MAGRO z Inkasa'].sum())
ilosc_polis_kl = kl['Przypis'].count()
srednia_kl = int(przychod_kl / ilosc_polis_kl)

przychod_zycie = int(zycie['MAGRO z Inkasa'].sum())
ilosc_polis_zycie = zycie['Przypis'].count()
srednia_zycie = int(przychod_zycie / ilosc_polis_zycie)

przychod_inne = int(inne['MAGRO z Inkasa'].sum())
ilosc_polis_inne = inne['Przypis'].count()
srednia_inne = int(przychod_inne / ilosc_polis_inne)

print(srednia_OC)
print(srednia_AC)
print(srednia_OCAC)
print(srednia_dom)
print(srednia_firma)
print(srednia_kl)
print(srednia_zycie)
print(srednia_inne)

Categories = ['MTPL', 'AC', 'FULL', 'HOUSE', 'BUSINESS', 'LIABILITY', 'TRAVEL', 'LIFE', 'OTHER']

mean_profit = {
    'MTPL': srednia_OC,
    'AC': srednia_AC,
    'FULL': srednia_OCAC,
    'HOUSE': srednia_dom,
    'BUSINESS': srednia_firma,
    'LIABILITY': srednia_oc,
    'TRAVEL': srednia_kl,
    'LIFE': srednia_zycie,
    'OTHER': srednia_inne,
}

mean_time = {
    'MTPL': 15,
    'AC': 40,
    'FULL': 40,
    'HOUSE': 20,
    'BUSINESS': 60,
    'LIABILITY': 20,
    'TRAVEL': 15,
    'LIFE': 30,
    'OTHER': 45,
}

model = LpProblem(name='insurance_commission', sense=LpMaximize)

# Definition of decision variables
x = {i: LpVariable(name=f'x{i}', lowBound=0) for i in range(1, 10)}
y = {i: LpVariable(name=f'y{i}', cat='Binary') for i in range(1, 10)}

# Add constraints
model += (10 * x[1] + 40 * x[2] + 40 * x[3] + 20 * x[4] + 60 * x[5] +
          40 * x[6] + 15 * x[7] + 30 * x[8] + 45 * x[9] <= 450, "time")

T = 450
model += (x[1] <= y[1] * T, "x1_constraint")
model += (x[2] <= y[2] * T, "x2_constraint")
model += (x[3] <= y[3] * T, "x3_constraint")
model += (x[4] <= y[4] * T, "x4_constraint")
model += (x[5] <= y[5] * T, "x5_constraint")
model += (x[6] <= y[6] * T, "x6_constraint")
model += (x[7] <= y[7] * T, "x7_constraint")
model += (x[8] <= y[8] * T, "x8_constraint")
model += (x[9] <= y[9] * T, "x9_constraint")
model += (y[1] + y[2] + y[3] + y[4] + y[5] + y[6] + y[7] + y[8] + y[9] <= 1, "y_constraint")

print('MODEL', model)

# Set the objective
model += 47 * x[1] + 90 * x[2] + 210 * x[3] + 59 * x[4] + 239 * x[5] + 95 * x[6] + 52 * x[7] + 33 * x[8] + 50 * x[9]

# Solve the optimization problem
status = model.solve()

print(f"status: {model.status}, {LpStatus[model.status]}")
print(f"objective: {model.objective.value()}")

for var in model.variables():
    print(f'{var.name}: {var.value()}')

for name, constraint in model.constraints.items():
    print(f'{name}: {constraint.value()}')
