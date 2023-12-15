import pathlib
import os
import json
import logging

def configureLogger(logger):
    os.makedirs(".logs", exist_ok=True)
    fhandler = logging.FileHandler(filename='.logs/jams-pub.log', mode='a')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
    fhandler.setFormatter(formatter)
    logger.addHandler(fhandler)
    logger.setLevel(logging.DEBUG)
    return logger

def basicConfig():
    logging.basicConfig(level=logging.CRITICAL)

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
