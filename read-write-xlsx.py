import os
import pylib.lease as lease
import pylib.copies as copies

def update_lease(wb):
    from openpyxl import load_workbook
    import json
    
    ws = wb.active

    response_list = lease.GetResponseFromFile("../jams/data/konica/2023-08.lease.508699675.doctr.json")
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

def update_copies(wb):
    from openpyxl import load_workbook
    import json
    
    ws = wb.active

    response_list = copies.GetResponseFromFile("../jams/data/konica/2023-08.copies.9009520780.doctr.json")
    
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

def main():
    from openpyxl import load_workbook

    wb = load_workbook("../jams/data/konica/2023-08.sheet.xlsx")
    wb = update_lease(wb)
    wb = update_copies(wb)

    os.makedirs("../jams/data/konica/output", exist_ok=True)
    wb.save("../jams/data/konica/output/2023-08.sheet.read-write-xlsx.xlsx")

if __name__ == "__main__":
    main()
