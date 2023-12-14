from . import lease
from . import copies
import pathlib
import os
import json

def data_path():
    return "../jams/data"

def vendor_data_path(vendor_str):
    data_path_str = data_path()
    return f"{data_path_str}/{vendor_str}"

def convert_pdf_to_doctr_cache(pdf_invoice_filepath):
    path = pathlib.Path(pdf_invoice_filepath)
    file_name = path.name.replace(".pdf",".doctr.json")
    path_name = f"{path.parent}/.cache"
    return f"{path_name}/{file_name}"

def convert_xls_to_xls_output(sheet_path_str):
    path = pathlib.Path(sheet_path_str)
    file_name = path.name
    path_name = f"{path.parent}/output"
    return f"{path_name}/{file_name}"

def write_json_output(file_path, json_export):
    path = pathlib.Path(file_path)
    path_name = path.parent

    os.makedirs(path_name, exist_ok=True)

    with open(file_path,"w") as file_handler:
        file_handler.write(json.dumps(json_export, indent=2))

def write_excel_output(file_path, workbook):
    path = pathlib.Path(file_path)
    path_name = path.parent

    os.makedirs(path_name, exist_ok=True)
    
    workbook.save(file_path)

def update_lease(wb, file_path):   
    ws = wb.active

    response_list = lease.GetResponseFromFile(file_path)
    invoice_number = response_list["invoice_number"]
  
    for page in response_list["pages"]:
        for item in page["items"]:
            item_json_str = json.dumps(item)
            if not "contract_number" in item or not "serial_number" in item:
                print("Invalid item: " + item_json_str)
                continue

            singleRow = lease.findSingleRowByItem(ws.iter_rows(min_row = 6, max_col=17, max_row=127),item)
            if singleRow != None:
                singleRow[9].value = item["total_price"]
                singleRow[10].value = invoice_number
            else:
                print("Error finding record for item: " + item_json_str)
    
    return wb

def update_copies(wb, file_path):   
    ws = wb.active
    response_list = copies.GetResponseFromFile(file_path)
    
    for page in response_list:
        for item in page["items"]:
            item_json_str = json.dumps(item)
            if not "contract_number" in item or not "serial_number" in item:
                print("Invalid item: " + item_json_str)
                continue

            singleRow = copies.findSingleRowByItem(ws.iter_rows(min_row = 6, max_col=17, max_row=127),item)
            if singleRow != None:
                singleRow[15].value = item["price"][0]
                singleRow[16].value = item["invoice_number"]
            else:
                print("Error finding record for item: " + item_json_str)

    return wb