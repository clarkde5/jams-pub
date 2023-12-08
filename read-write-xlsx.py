from pylib.lease import *

def main():
    from openpyxl import load_workbook
    response_list = GetResponseFromFile("../jams/output/Aug 23 Lease-docTR.json")
    invoice_number = response_list["invoice_number"]
    page2_items = response_list["pages"][1]["items"]
    
    wb = load_workbook("../jams/data/konica/KONICA Master2023.Blank.xlsx")
    ws = wb.active
    print(ws['A1'].value)
    ws['A1'].value = "new value"
    wb.save("../jams/data/konica/KONICA Master2023.Modified.xlsx")

if __name__ == "__main__":
    main()