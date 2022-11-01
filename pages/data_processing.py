import pandas as pd

def dtypes_modifications(df):
    df['INSPECTION_BEGIN_DT']= pd.to_datetime(df['INSPECTION_BEGIN_DT'])
    df['INSPECTION_END_DT']= pd.to_datetime(df['INSPECTION_END_DT'])
    df['VIOLATION_NO']=df['VIOLATION_NO'].fillna(0).astype(float)
    df['VIOLATOR_ID']=df['VIOLATOR_ID'].astype(str)
    df['VIOLATOR_NAME']=df['VIOLATOR_NAME'].astype(str)
    df['VIOLATOR_TYPE_CD']=df['VIOLATOR_TYPE_CD'].astype(str)
    df['MINE_ID']=df['MINE_ID'].fillna(0).astype(float)
    df['MINE_NAME']=df['MINE_NAME'].astype(str)
    df['MINE_TYPE']=df['MINE_TYPE'].astype(str)
    df['COAL_METAL_IND']=df['COAL_METAL_IND'].astype(str)
    df['CONTRACTOR_ID']=df['CONTRACTOR_ID'].astype(str)
    df['FISCAL_YR']=df['FISCAL_YR'].fillna(0).astype(float)
    df['VIOLATION_ISSUE_DT']= pd.to_datetime(df['VIOLATION_ISSUE_DT'])
    df['VIOLATION_OCCUR_DT']= pd.to_datetime(df['VIOLATION_OCCUR_DT'])
    df['FISCAL_QTR']=df['FISCAL_QTR'].fillna(0).astype(float)
    df['VIOLATION_ISSUE_TIME']= pd.to_datetime(df['VIOLATION_ISSUE_TIME'])
    df['SIG_SUB']=df['SIG_SUB'].astype(str)
    df['SECTION_OF_ACT']=df['SECTION_OF_ACT'].astype(str)
    df['PART_SECTION']=df['PART_SECTION'].astype(str)
    df['SECTION_OF_ACT_1']=df['SECTION_OF_ACT_1'].astype(str)
    df['SECTION_OF_ACT_2']=df['SECTION_OF_ACT_2'].astype(str)
    df['CIT_ORD_SAFE']=df['CIT_ORD_SAFE'].astype(str)
    df['TERMINATION_DT']= pd.to_datetime(df['TERMINATION_DT'])
    df['TERMINATION_TIME']= pd.to_datetime(df['TERMINATION_TIME'])
    df['TERMINATION_TYPE']=df['TERMINATION_TYPE'].astype(str)
    df['REPLACED_BY_ORDER_NO']=df['REPLACED_BY_ORDER_NO'].astype(str)
    df['LIKELIHOOD']=df['LIKELIHOOD'].astype(str)
    df['INJ_ILLNESS']=df['INJ_ILLNESS'].astype(str)
    df['NO_AFFECTED']=df['NO_AFFECTED'].fillna(0).astype(float)
    df['NEGLIGENCE']=df['NEGLIGENCE'].astype(str)
    df['ENFORCEMENT_AREA']=df['ENFORCEMENT_AREA'].astype(str)
    df['SPECIAL_ASSESS']=df['SPECIAL_ASSESS'].astype(str)
    df['PRIMARY_OR_MILL']=df['PRIMARY_OR_MILL'].astype(str)
    df['PROPOSED_PENALTY']=df['PROPOSED_PENALTY'].fillna(0).astype(float)
    df['VIOLATOR_VIOLATION_CNT']=df['VIOLATOR_VIOLATION_CNT'].fillna(0).astype(float)
    df['VIOLATOR_INSPECTION_DAY_CNT']=df['VIOLATOR_INSPECTION_DAY_CNT'].fillna(0).astype(float)

