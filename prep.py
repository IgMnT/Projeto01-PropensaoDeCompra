df1['vehicle_damage'] = df1['vehicle_damage'].apply(lambda x: 1 if x == 'Yes' else 0)
df1['vehicle_age'] = df1['vehicle_age'].apply (lambda x:0 if x == '< 1 Year	' else (1 if x == '1-2 Year' else 2))