import os
import pylib.common as common

def main():
    from openpyxl import load_workbook

    wb = load_workbook("../jams/data/konica/2023-08.sheet.xlsx")

    wb = common.update_lease(wb, "../jams/data/konica/doctr/2023-08.lease.508699675.doctr.json")
    wb = common.update_copies(wb, "../jams/data/konica/doctr/2023-08.copies.9009520780.doctr.json")

    common.write_excel_output("../jams/data/konica/output/2023-08.sheet.read-write-xlsx.xlsx", wb)

    print("Process completed")

if __name__ == "__main__":
    main()
