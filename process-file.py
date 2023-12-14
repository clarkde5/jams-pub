def main():
    import argparse
    import pylib.doctr as doctr
    import pylib.common as common
    import glob
    import pathlib
    import os
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--vendor", type=str, required=True)
    parser.add_argument("--year", type=str, default="2023")
    parser.add_argument("--month", type=str, default="08")
    args = parser.parse_args()

    vendor_data_path = common.vendor_data_path(args.vendor)
    print(f"Processing: {vendor_data_path}/{args.year}-{args.month}")
    pdf_invoice_documents = glob.glob(f"{vendor_data_path}/{args.year}-{args.month}*.pdf")

    for pdf_invoice_filepath in pdf_invoice_documents:
        doctr_cache_file = common.convert_pdf_to_doctr_cache(pdf_invoice_filepath)
        if not pathlib.Path(doctr_cache_file).exists():
            print(f"Process file: {pdf_invoice_filepath}")
            common.write_json_output(doctr_cache_file, doctr.doctr_ocr_pdf(pdf_invoice_filepath))
        else:
            print(f"Cached file found: {pdf_invoice_filepath} -> {doctr_cache_file}")

if __name__ == "__main__":
    main()