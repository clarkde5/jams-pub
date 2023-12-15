import pylib.common as common

def main():
    from openpyxl import load_workbook

    sheet_path_str = "../jams/data/konica/2023-08.sheet.xlsx"
    wb = load_workbook(sheet_path_str)

    wb = common.update_lease(wb, "../jams/data/konica/doctr/2023-08.lease.508699675.doctr.json")
    wb = common.update_copies(wb, "../jams/data/konica/doctr/2023-08.copies.9009520780.doctr.json")

    common.write_excel_output(common.convert_xls_to_xls_output(sheet_path_str), wb)

    print("Process completed")

if __name__ == "__main__":
    main()
