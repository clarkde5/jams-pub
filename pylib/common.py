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
    return convertExtension(appendPath(pdf_invoice_filepath, ".cache"), ".pdf",".doctr.json")

def convertToOutputPath(sheet_path_str):
    return appendPath(sheet_path_str, "output")

def appendPath(file_path, subpath):
    path = pathlib.Path(file_path)
    file_name = path.name
    path_name = f"{path.parent}/{subpath}"
    return f"{path_name}/{file_name}"

def convertExtension(file_path, ext1, ext2):
    path = pathlib.Path(file_path)
    file_name = path.name.replace(ext1, ext2)
    return f"{path.parent}/{file_name}"

def write_text_output(file_path, text):
    path = pathlib.Path(file_path)
    path_name = path.parent

    os.makedirs(path_name, exist_ok=True)

    with open(file_path,"w") as file_handler:
        file_handler.write(text)

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
