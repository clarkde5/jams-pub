def main():
    import argparse
    import pylib.doctr as doctr
    import pylib.common as common
    import glob
    import pathlib
    import datetime
    from openpyxl import load_workbook
    

    parser = argparse.ArgumentParser()
    parser.add_argument("--vendor", type=str, required=True)
    parser.add_argument("--year", type=str, default=str(datetime.date.today().year))
    parser.add_argument("--month", type=str, default="08")
    args = parser.parse_args()

    vendor_data_path = common.vendor_data_path(args.vendor)
    print(f"Processing: {vendor_data_path}/{args.year}-{args.month}")
    pdf_invoice_documents = glob.glob(f"{vendor_data_path}/{args.year}-{args.month}*.pdf")

    sheet_path_str = f"{vendor_data_path}/{args.year}-{args.month}.sheet.xlsx"
    sheet_path = pathlib.Path(sheet_path_str)
    if not sheet_path.is_file():
        print(f"Sheet template does not exist: {sheet_path_str}")
        return
    
    wb = load_workbook(sheet_path_str)

    for pdf_invoice_filepath in pdf_invoice_documents:
        doctr_cache_file = common.convert_pdf_to_doctr_cache(pdf_invoice_filepath)
        if not pathlib.Path(doctr_cache_file).exists():
            print(f"Process file: {pdf_invoice_filepath}")
            common.write_json_output(doctr_cache_file, doctr.doctr_ocr_pdf(pdf_invoice_filepath))
        else:
            print(f"Cached file found: {pdf_invoice_filepath} -> {doctr_cache_file}")

    for doctr_cache_file in [common.convert_pdf_to_doctr_cache(pdf_invoice_filepath) for pdf_invoice_filepath in pdf_invoice_documents]:
        if "lease" in doctr_cache_file:
            wb = common.update_lease(wb, doctr_cache_file)
        elif "copies" in doctr_cache_file:
            wb = common.update_copies(wb, doctr_cache_file)

    common.write_excel_output(common.convert_xls_to_xls_output(sheet_path_str), wb)

if __name__ == "__main__":
    main()