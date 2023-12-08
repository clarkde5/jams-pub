import os
from pylib.lease import *

def findSingleRowByItem(relavant_rows, item):
    return next((row for row in relavant_rows if (row[3].value == item["contract_number"] and row[1].value == item["serial_number"])),None)

def main():
    from openpyxl import load_workbook
    import json
    
    response_list = GetResponseFromFile("../jams/data/konica/2023-08.lease.508699675.doctr.json")
    invoice_number = response_list["invoice_number"]
  
    wb = load_workbook("../jams/data/konica/2023-08.sheet.xlsx")
    ws = wb.active

    for page in response_list["pages"]:
        for item in page["items"]:
            item_json_str = json.dumps(item)
            if not "contract_number" in item or not "serial_number" in item:
                print("Invalid item: " + item_json_str)
                continue

            singleRow = findSingleRowByItem(ws.iter_rows(min_row = 6, max_col=11, max_row=127),item)
            if singleRow != None:
                singleRow[9].value = item["total_price"]
                singleRow[10].value = invoice_number
            else:
                print("Error finding record for item: " + item_json_str)
    
    os.makedirs("../jams/data/konica/output", exist_ok=True)
    wb.save("../jams/data/konica/output/2023-08.sheet.xlsx")

if __name__ == "__main__":
    main()
