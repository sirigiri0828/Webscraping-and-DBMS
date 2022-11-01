import mysql.connector as msql
import pandas as pd

def get_mysql_data(query):
    try:
        connection = msql.connect(host='localhost', database = 'mhsa_database',user='root',  
                            password='MY_new_pass1')
        df = pd.read_sql(query,connection)
        connection.close()
        return df
    except Exception as e:
        connection.close()
        print(str(e))
        print("unable to fetch data")
        return None
