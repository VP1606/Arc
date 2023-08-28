import csv
import os
import pandas as pd

file_path = os.path.join('../temp/collected.csv')
expected_columns = ['Cust_Code','transaction_number','Date_transaction','Cust_code1','Item','Line_no','Description','Pack_description','UOS','Pack','Qty','Sell','OnPromo','VAT','vatrate','RRP','Total_Goods','Total_Vat','Total','hierarchy1','hierarchy_description','Selling_Out_Barcode','Retail_Barcode','Brand']
# Return Shape: (BOOL, STR, ANY)
# Status (Bool), Consise Reason, Additional Info ('' if not available)

def handle():
    validate_result = validate()
    print(validate_result)
    if validate_result[0] is False:
        return validate_result
    else:
        print("Valid CSV!")
        return validate_result


def validate():
    print("B6")
    try:
        file = pd.read_csv(file_path)
        missing_columns = expected_columns
        for col in file.columns:
            if col in missing_columns:
                missing_columns.remove(col)
        if len(missing_columns) != 0:
            print(missing_columns)
            return (False, 'Missing Columns!', missing_columns)

        else:
            return (True, 'Valid CSV', '')
            
    except Exception as e:
        print(e)
        return (False, 'Error while validating file!', e)
