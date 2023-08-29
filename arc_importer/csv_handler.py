import csv
import os
import pandas as pd
import mysql.connector

file_path = os.path.join('../temp/collected.csv')
expected_columns = ['Cust_Code','transaction_number','Date_transaction','Cust_code1','Item','Line_no','Description','Pack_description','UOS','Pack','Qty','Sell','OnPromo','VAT','vatrate','RRP','Total_Goods','Total_Vat','Total','hierarchy1','hierarchy_description','Selling_Out_Barcode','Retail_Barcode','Brand']
# Return Shape: (BOOL, STR, ANY)
# Status (Bool), Consise Reason, Additional Info ('' if not available)

def handle():

    validate_result = validate()
    if validate_result[0] is False:
        print("Invalid CSV!")
        return validate_result

    _, _, file = validate_result

    error = [False, None]
    try:
        save_to_sql(file=file)
        error[0] = False

    except Exception as e:
        print(f"SQL Error! ::: {e}")
        error = [True, e]
    
    if error[0] is True:
        return (False, 'SQL Commiting Error', error[1])
    else:
        return (True, 'Completed Sucessfully', '')


def validate():
    try:
        file = pd.read_csv(file_path)
        missing_columns = expected_columns.copy()
        for col in file.columns:
            if col in missing_columns:
                missing_columns.remove(col)

        if len(missing_columns) != 0:
            return (False, 'Missing Columns!', missing_columns)

        else:
            return (True, 'Valid CSV', file)
            
    except Exception as e:
        return (False, 'Error while validating file!', e)

def save_to_sql(file: pd.DataFrame):
    mydb = mysql.connector.connect(
        host="rainford.dyndns.org",
        user="mpos",
        password="mpospass",
        database="mpos"
    )

    def fetch(row, key):
        try:
            val = row[key]
            if pd.isna(val):
                return ''
            else:
                return val
        except:
            return ''

    mycursor = mydb.cursor()
    
    sql = "INSERT INTO parfettsinvoice(Cust_Code,transaction_number," \
          "Date_transaction,Cust_code1,Item,Line_no,Description,Pack_description,UOS,Pack,Qty,Sell,OnPromo,VAT,vatrate,RRP,Total_Goods," \
          "Total_Vat,Total,hierarchy1,hierarchy_description,Selling_Out_Barcode,Retail_Barcode,Brand,MyUnknownColumn)" \
          "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    
    for _, row in file.iterrows():
        vals = []
        for col in expected_columns:
            vals.append(fetch(row, col))

        vals.append('')
        mycursor.execute(sql, vals)
    
    mydb.commit()
    mydb.close()

    return True
