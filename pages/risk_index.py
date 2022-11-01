
import pandas as pd
import numpy as np
from .queries import get_table_data_of_year,get_table_data_of_year_mines
from sklearn import preprocessing
from numpy import log as ln



def risk_index(year):
    req_cols_for_violation=["MINE_ID","CAL_YR","MINE_TYPE","LIKELIHOOD","COAL_METAL_IND","NO_AFFECTED","PROPOSED_PENALTY","NEGLIGENCE","SIG_SUB","CIT_ORD_SAFE","INJ_ILLNESS","VIOLATOR_TYPE_CD"]
    table_name_violation=  "VIOLATIONS"
    req_cols_for_inspection=["MINE_ID","TOTAL_INSP_HOURS","CAL_YR"]
    table_name_inspection=  "INSPECTIONS"
    req_cols_for_employee_hrs=["MINE_ID","ANNUAL_HRS","AVG_ANNUAL_EMPL","CAL_YR"]
    table_name_employee_hrs=  "MINESPRODYEARLY"
    req_cols_for_mines=["MINE_ID","PRIMARY_CANVASS","CURRENT_MINE_TYPE"]
    table_name_mines=  "MINES"
    req_cols_for_accidents=["MINE_ID","DEGREE_INJURY","DAYS_RESTRICT","DAYS_LOST","CAL_YR","COAL_METAL_IND","CONTRACTOR_ID"]
    table_name_accidents=  "ACCIDENTS"

    risk_index_level = ["MINE_ID","CAL_YR"]

    df_violation=get_table_data_of_year(",".join(req_cols_for_violation),table_name_violation,year)
    print("df_violation")
    print(df_violation) 
    # df_violation = df_violation[(df_violation["CAL_YR"] == year)]   
    df_violation = df_violation[df_violation["VIOLATOR_TYPE_CD"] == "Operator"]
    df_violation = df_violation[req_cols_for_violation].reset_index(drop=True)
    lst = ["CIT_ORD_SAFE","SIG_SUB"]
    Table = pd.DataFrame(index = df_violation.groupby(["MINE_ID","CAL_YR"]).mean().index)
    for i in lst:
        groupby_df = pd.DataFrame(df_violation.groupby(risk_index_level)[i].value_counts())
        groupby_df.columns=["count"+"_"+i]
        groupby_df= groupby_df.reset_index()
        pivot_df = groupby_df.pivot(index=risk_index_level, columns= i, values='count_'+i).fillna(0)
        Table = pd.concat([Table,pivot_df],axis = 1)
    Table = Table.reset_index()
    Table.rename(columns={'index':'MINE_ID'}, inplace=True )

    df_inspections=get_table_data_of_year(",".join(req_cols_for_inspection),table_name_inspection,year)
    print("df_inspections")
    print(df_inspections) 
    groupby_df1 = pd.DataFrame(df_inspections.groupby(risk_index_level)["TOTAL_INSP_HOURS"].sum())
    groupby_df1.columns=["TOTAL_INSP_HOURS"]
    groupby_df1= groupby_df1.reset_index()
    df_1 = pd.merge(Table,groupby_df1,on = risk_index_level,how = "inner")
    print(df_1)
    df_employee_hours=get_table_data_of_year(",".join(req_cols_for_employee_hrs),table_name_employee_hrs,year)
    print("df_employee_hours")
    print(df_employee_hours) 
    employee_df = df_employee_hours[req_cols_for_employee_hrs]
    groupby_df_employee = employee_df.groupby(risk_index_level)["ANNUAL_HRS","AVG_ANNUAL_EMPL"].sum()
    df_2 = pd.merge(df_1,groupby_df_employee,on = risk_index_level,how= "inner")
    print(df_2)

    df_accidents_data=get_table_data_of_year(",".join(req_cols_for_accidents),table_name_accidents,year)
    print("df_accidents_data")
    print(df_accidents_data) 
    # df_accidents_data= df_accidents_data[(df_accidents_data["CAL_YR"] == year)]
    df_accidents_data= df_accidents_data[df_accidents_data["COAL_METAL_IND"]== "M"]
    df_accidents_data= df_accidents_data[df_accidents_data["CONTRACTOR_ID"].isnull()]
    filter_list = ['DYS AWY FRM WRK & RESTRCTD ACT', 'DAYS AWAY FROM WORK ONLY', 'DAYS RESTRICTED ACTIVITY ONLY','NO DYS AWY FRM WRK,NO RSTR ACT','PERM TOT OR PERM PRTL DISABLTY']
    df_accidents_data_1 = df_accidents_data[df_accidents_data.DEGREE_INJURY.isin(filter_list)]
    df_accidents_data_1 = df_accidents_data[(df_accidents_data.DEGREE_INJURY == 'DYS AWY FRM WRK & RESTRCTD ACT') | (df_accidents_data.DEGREE_INJURY == 'DAYS AWAY FROM WORK ONLY') | (df_accidents_data.DEGREE_INJURY == 'DAYS RESTRICTED ACTIVITY ONLY') | (df_accidents_data.DEGREE_INJURY == 'NO DYS AWY FRM WRK,NO RSTR ACT')| (df_accidents_data.DEGREE_INJURY == 'PERM TOT OR PERM PRTL DISABLTY')]
    groupby_df_accidents = df_accidents_data_1.groupby(risk_index_level)["DAYS_RESTRICT","DAYS_LOST"].sum()
    df_3 = pd.merge(df_2,groupby_df_accidents,on = risk_index_level,how= "left")
    df_3["Restricted and lost work days"] = df_3["DAYS_RESTRICT"] + df_3["DAYS_LOST"]
    df_accidents_data_1
    df_accidents_data_1 = df_accidents_data[["MINE_ID","CAL_YR","DEGREE_INJURY"]]
    lst = ["DEGREE_INJURY"]
    Table1 = pd.DataFrame(index = df_accidents_data_1.groupby(risk_index_level).mean().index)
    print(Table1.head())
    for i in lst:
        groupby_df = pd.DataFrame(df_accidents_data_1.groupby(risk_index_level)[i].value_counts())
        groupby_df.columns=["count"+"_"+i]
        groupby_df= groupby_df.reset_index()
        pivot_df = groupby_df.pivot(index=risk_index_level, columns= i, values='count_'+i).fillna(0)
        Table_accidents = pd.concat([Table1,pivot_df],axis = 1)
    Table_accidents = Table_accidents.reset_index()
    Table_accidents.head()
    Table_accidents1 = Table_accidents[["MINE_ID","CAL_YR","FATALITY","ACCIDENT ONLY","NO DYS AWY FRM WRK,NO RSTR ACT","PERM TOT OR PERM PRTL DISABLTY","DAYS AWAY FROM WORK ONLY","DYS AWY FRM WRK & RESTRCTD ACT"]]
    Table_accidents1["No. NLT Accidents"]  = Table_accidents1["ACCIDENT ONLY"] + Table_accidents1["NO DYS AWY FRM WRK,NO RSTR ACT"]
    Table_accidents1["No. LT Accidents"]  = Table_accidents1["PERM TOT OR PERM PRTL DISABLTY"] + Table_accidents1["DAYS AWAY FROM WORK ONLY"] + Table_accidents1["DYS AWY FRM WRK & RESTRCTD ACT"]
    df_4 = pd.merge(df_3,Table_accidents1,on = risk_index_level,how = "left")
    df_4 = df_4.rename(columns = {'Y':'No. S&S'})

    df_mines=get_table_data_of_year_mines(",".join(req_cols_for_mines),table_name_mines)
    df_mines = df_mines[["MINE_ID","PRIMARY_CANVASS","CURRENT_MINE_TYPE"]]
    df_mines = df_mines[df_mines["PRIMARY_CANVASS"] == "Metal"]
    df_mines= df_mines[df_mines["CURRENT_MINE_TYPE"]=="Underground"]
    df_main = pd.merge(df_4,df_mines,on = "MINE_ID",how = "inner")

    df_adding1 = pd.DataFrame(df_violation.groupby(risk_index_level)["NO_AFFECTED","PROPOSED_PENALTY"].sum())
    df_adding1.columns=["NO_AFFECTED","PROPOSED_PENALTY"]
    df_adding1= df_adding1.reset_index()
    Table_1 = pd.merge(df_main,df_adding1,how = "inner")

    print((Table_1).head())

    Table1  = Table_1[["MINE_ID","CAL_YR","AVG_ANNUAL_EMPL","ANNUAL_HRS","Citation","No. S&S","Order","TOTAL_INSP_HOURS","FATALITY","NO_AFFECTED","PROPOSED_PENALTY"]].reset_index(drop=True)
    Table1 ["No. NLT Accidents"]  = Table_1["ACCIDENT ONLY"] + Table_1["NO DYS AWY FRM WRK,NO RSTR ACT"]
    Table1 ["No. LT Accidents"]  = Table_1["PERM TOT OR PERM PRTL DISABLTY"] + Table_1["DAYS AWAY FROM WORK ONLY"] + Table_1["DYS AWY FRM WRK & RESTRCTD ACT"]
    Table1 ["Restricted and lost work days"] = Table_1["DAYS_RESTRICT"] + Table_1["DAYS_LOST"]
    Table_2 = pd.DataFrame()
    Table_2 = Table1[["MINE_ID","CAL_YR"]]
    Table_2["PROPOSED_PENALTY"] = (Table1["PROPOSED_PENALTY"])
    Table_2["NDL_IR"] = (Table1["No. NLT Accidents"] / Table1["ANNUAL_HRS"]) *200000
    Table_2["NFDL_IR"]=   (Table1["No. LT Accidents"] / Table1["ANNUAL_HRS"]) *200000
    Table_2["SM"] =   (Table1["Restricted and lost work days"] / Table1["ANNUAL_HRS"]) *200000
    Table_2["C/100"] = (Table1["Citation"] * 100)/ Table1["TOTAL_INSP_HOURS"]
    Table_2["SS/100"] = (Table1["No. S&S"] * 100)/ Table1["TOTAL_INSP_HOURS"]
    Table_2["O/100"] = (Table1["Order"] * 100)/ Table1["TOTAL_INSP_HOURS"]
    Table_2 = Table_2.set_index(["MINE_ID","CAL_YR"])
    Table_2 = Table_2.fillna(0)
    df = Table_2.copy()
    df = df.replace((np.inf, -np.inf, np.nan), 0).reset_index(drop=True)
    x = df.values

    print(x)
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    df = pd.DataFrame(x_scaled)
    df = df.set_index(Table_1.groupby(["MINE_ID","CAL_YR"]).mean().index)
    df  = df.rename(columns={1: 'NDL_IR',2: 'NFDL_IR',3: 'SM',4: 'C/100',5:'SS/100',6:'O/100',0:"PROPOSED_PENALTY"})
    df = df.round(decimals = 2)
    df = df.reset_index()
    risk_index_table = df.copy()
    risk_index_table_relative_ratio = pd.DataFrame()
    risk_index_table_relative_ratio["PROPOSED_PENALTY"] = risk_index_table["PROPOSED_PENALTY"] / risk_index_table["PROPOSED_PENALTY"].sum()
    risk_index_table_relative_ratio["NDL_IR"] = risk_index_table["NDL_IR"] / risk_index_table["NDL_IR"].sum()
    risk_index_table_relative_ratio["NFDL_IR"] = risk_index_table["NFDL_IR"] / risk_index_table["NFDL_IR"].sum()
    risk_index_table_relative_ratio["SM"] = risk_index_table["SM"] / risk_index_table["SM"].sum()
    risk_index_table_relative_ratio["C/100"]  = risk_index_table["C/100"] / risk_index_table["C/100"].sum()
    risk_index_table_relative_ratio["SS/100"] = risk_index_table["SS/100"] / risk_index_table["SS/100"].sum()
    risk_index_table_relative_ratio["O/100"] = risk_index_table["O/100"] / risk_index_table["O/100"].sum()

    risk_index_table_log = risk_index_table_relative_ratio * np.log(risk_index_table_relative_ratio)

    Penalty_weightage_factor = (-1) / (((len(risk_index_table)) * (risk_index_table_log["PROPOSED_PENALTY"].sum())))
    NDL_IR_weightage_factor = -1 / (((len(risk_index_table)) * (risk_index_table_log["NDL_IR"].sum())))
    NFDL_IR_weightage_factor = -1 / (((len(risk_index_table)) * (risk_index_table_log["NFDL_IR"].sum())))
    SM_weightage_factor = -1 / (((len(risk_index_table)) * (risk_index_table_log["SM"].sum())))
    C_weightage_factor  = -1 / (((len(risk_index_table)) * (risk_index_table_log["C/100"].sum())))
    SS_weightage_factor = -1 / (((len(risk_index_table)) * (risk_index_table_log["SS/100"].sum())))
    O_weightage_factor = -1 / (((len(risk_index_table)) * (risk_index_table_log["O/100"].sum())))

    risk_index_table["Risk_Index"] = (risk_index_table["PROPOSED_PENALTY"] * Penalty_weightage_factor) + (risk_index_table["NDL_IR"] *NDL_IR_weightage_factor) + (risk_index_table["NFDL_IR"]*NFDL_IR_weightage_factor) + (risk_index_table["SM"] *SM_weightage_factor) + (risk_index_table["C/100"] *C_weightage_factor)+ (risk_index_table["SS/100"] *SS_weightage_factor) + (risk_index_table["O/100"]*O_weightage_factor)
    risk_index_table.to_csv(r"risk_index.csv")
    return risk_index_table