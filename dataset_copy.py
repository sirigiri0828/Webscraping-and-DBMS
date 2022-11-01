# %%
import pandas as pd
import numpy as np
df_violation = pd.read_csv(r"C:\Users\dharm\OneDrive\Documents\Project\Main datasets retrieval\Violations\Major_dataset.csv",low_memory = False)

# %%
# df_violation= df_violation[df_violation["MINE_TYPE"]=="Underground"]
df_violation = df_violation[(df_violation["CAL_YR"] == 2012)]
df_violation = df_violation[df_violation["VIOLATOR_TYPE_CD"] == "Operator"]

# %%
df_violation = df_violation[["MINE_ID","MINE_TYPE","LIKELIHOOD","COAL_METAL_IND","NO_AFFECTED","PROPOSED_PENALTY","NEGLIGENCE","SIG_SUB","CIT_ORD_SAFE","INJ_ILLNESS"]].reset_index(drop=True)

# %%
lst = ["CIT_ORD_SAFE","SIG_SUB"]
Table = pd.DataFrame(index = list(set(df_violation["MINE_ID"])))

for i in lst:
    groupby_df = pd.DataFrame(df_violation.groupby("MINE_ID")[i].value_counts())
    groupby_df.columns=["count"+"_"+i]
    groupby_df= groupby_df.reset_index()
    pivot_df = groupby_df.pivot(index='MINE_ID', columns= i, values='count_'+i).fillna(0)
    Table = pd.concat([Table,pivot_df],axis = 1)

# %%
Table = Table.reset_index()
Table.rename(columns={'index':'MINE_ID'}, inplace=True )

# %%
Table

# %%
Table.info()

# %%
df_inspections = pd.read_csv(r"C:\Users\dharm\OneDrive\Documents\Project\Main datasets retrieval\Inspection\Inspections1.csv",low_memory = False)
df_inspections1 = df_inspections[(df_inspections["CAL_YR"] == 2012)]
groupby_df1 = pd.DataFrame(df_inspections1.groupby("MINE_ID")["SUM(TOTAL_INSP_HOURS)"].sum())
groupby_df1.columns=["TOTAL_INSP_HOURS"]
groupby_df1= groupby_df1.reset_index()
df_1 = pd.merge(Table,groupby_df1,on = "MINE_ID",how = "left")

# %%
df_1

# %%
df_employee_hours = pd.read_excel(r"C:\Users\dharm\OneDrive\Documents\Project\Excel sheets\Excel sheets 11-16-21\Employee Yearly.xlsx")

# %%
# employee_df = df_employee_hours .copy()

# %%
employee_df= df_employee_hours[(df_employee_hours["CALENDAR_YR"] == 2012)]
employee_df = employee_df[["MINE_ID","ANNUAL_HRS","AVG_ANNUAL_EMPL"]]
groupby_df_employee = employee_df.groupby('MINE_ID')["ANNUAL_HRS","AVG_ANNUAL_EMPL"].sum()
df_2 = pd.merge(df_1,groupby_df_employee,on = "MINE_ID",how= "left")

# %%
df_accidents_data = pd.read_csv(r"C:\Users\dharm\OneDrive\Documents\Project\Main datasets retrieval\Accidents\Accidents1.csv")
df_accidents_data= df_accidents_data[(df_accidents_data["CAL_YR"] == 2012)]
df_accidents_data= df_accidents_data[df_accidents_data["COAL_METAL_IND"]== "M"]
df_accidents_data= df_accidents_data[df_accidents_data["CONTRACTOR_ID"].isnull()]
filter_list = ['DYS AWY FRM WRK & RESTRCTD ACT', 'DAYS AWAY FROM WORK ONLY', 'DAYS RESTRICTED ACTIVITY ONLY','NO DYS AWY FRM WRK,NO RSTR ACT','PERM TOT OR PERM PRTL DISABLTY']
df_accidents_data_1 = df_accidents_data[df_accidents_data.DEGREE_INJURY.isin(filter_list)]

df_accidents_data_1 = df_accidents_data[(df_accidents_data.DEGREE_INJURY == 'DYS AWY FRM WRK & RESTRCTD ACT') | (df_accidents_data.DEGREE_INJURY == 'DAYS AWAY FROM WORK ONLY') | (df_accidents_data.DEGREE_INJURY == 'DAYS RESTRICTED ACTIVITY ONLY') | (df_accidents_data.DEGREE_INJURY == 'NO DYS AWY FRM WRK,NO RSTR ACT')| (df_accidents_data.DEGREE_INJURY == 'PERM TOT OR PERM PRTL DISABLTY')]
groupby_df_accidents = df_accidents_data_1.groupby('MINE_ID')["DAYS_RESTRICT","DAYS_LOST"].sum()
df_3 = pd.merge(df_2,groupby_df_accidents,on = "MINE_ID",how= "left")

# %%
df_3["Restricted and lost work days"] = df_3["DAYS_RESTRICT"] + df_3["DAYS_LOST"]

# %%
df_accidents_data_read = pd.read_csv(r"C:\Users\dharm\OneDrive\Documents\Project\Main datasets retrieval\Accidents\Accidents1.csv")

# %%
df_accidents_data_read= df_accidents_data_read[df_accidents_data_read["CONTRACTOR_ID"].isnull()]

# %%
df_accidents_data_read = df_accidents_data_read[(df_accidents_data_read["CAL_YR"] == 2012)]

# %%
df_accidents_data_1 = df_accidents_data[["MINE_ID","DEGREE_INJURY"]]

# %%
df_accidents_data_1

# %%
lst = ["DEGREE_INJURY"]
Table1 = pd.DataFrame(index = list(set(df_accidents_data_1["MINE_ID"])))

for i in lst:
    groupby_df = pd.DataFrame(df_accidents_data_1.groupby("MINE_ID")[i].value_counts())
    groupby_df.columns=["count"+"_"+i]
    groupby_df= groupby_df.reset_index()
    pivot_df = groupby_df.pivot(index='MINE_ID', columns= i, values='count_'+i).fillna(0)
    Table_accidents = pd.concat([Table1,pivot_df],axis = 1)

# %%
Table_accidents

# %%
Table_accidents = Table_accidents.reset_index()

# %%
Table_accidents = Table_accidents.rename(columns = {'index':'MINE_ID'})

# %%
Table_accidents.info()

# %%
Table_accidents

# %%
Table_accidents1 = Table_accidents[["MINE_ID","FATALITY","ACCIDENT ONLY","NO DYS AWY FRM WRK,NO RSTR ACT","PERM TOT OR PERM PRTL DISABLTY","DAYS AWAY FROM WORK ONLY","DYS AWY FRM WRK & RESTRCTD ACT"]]

# %%
# Table_accidents1 = Table_accidents[["MINE_ID","ACCIDENT ONLY","NO DYS AWY FRM WRK,NO RSTR ACT","PERM TOT OR PERM PRTL DISABLTY","DAYS AWAY FROM WORK ONLY","DYS AWY FRM WRK & RESTRCTD ACT"]]

# %%
Table_accidents1

# %%
Table_accidents1["No. NLT Accidents"]  = Table_accidents1["ACCIDENT ONLY"] + Table_accidents1["NO DYS AWY FRM WRK,NO RSTR ACT"]
Table_accidents1["No. LT Accidents"]  = Table_accidents1["PERM TOT OR PERM PRTL DISABLTY"] + Table_accidents1["DAYS AWAY FROM WORK ONLY"] + Table_accidents1["DYS AWY FRM WRK & RESTRCTD ACT"]

# %%
Table_accidents1.info()

# %%
df_4 = pd.merge(df_3,Table_accidents1,on = "MINE_ID",how = "left")

# %%
df_4 = df_4 .rename(columns = {'Y':'No. S&S'})

# %%
df_4.info()

# %%
# df_4.to_csv(r"C:\Users\dharm\OneDrive\Desktop\Table_ug_2012.csv")

# %%
df_mines = pd.read_excel(r"C:\Users\dharm\OneDrive\Documents\Project\Excel sheets\Excel sheets 11-16-21\Mines dataset.xlsx")

# %%
df_mines = df_mines[["MINE_ID","PRIMARY_CANVASS","CURRENT_MINE_TYPE"]]
df_mines = df_mines[df_mines["PRIMARY_CANVASS"] == "Metal"]
df_mines= df_mines[df_mines["CURRENT_MINE_TYPE"]=="Underground"]
df_main = pd.merge(df_4,df_mines,on = "MINE_ID",how = "inner")

# %%
df_adding1 = pd.DataFrame(df_violation.groupby("MINE_ID")["NO_AFFECTED","PROPOSED_PENALTY"].sum())
df_adding1.columns=["NO_AFFECTED","PROPOSED_PENALTY"]
df_adding1= df_adding1.reset_index()
Table_1 = pd.merge(df_main,df_adding1,how = "left")

# %%
Table_1.info()

# %%
Table_1.to_csv(r"C:\Users\dharm\OneDrive\Desktop\Table_metal_ug.csv")

# %%



