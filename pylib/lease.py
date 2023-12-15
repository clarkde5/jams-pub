import logging
from . import common

logger = common.configureLogger(logging.getLogger(__name__))

def getInvoiceNumber(page_idx,page):
  import re

  invoice_number = ""

  for block in page["blocks"]:
    if invoice_number != "":
      break
    for line in block["lines"]:
      if invoice_number != "":
        break
      sorted_words = sorted(line["words"], key = lambda x: x["geometry"][0][0])
      for word in sorted_words:
        if re.search("INVOICE.*",word["value"]) and re.search("NUMBER.*",sorted_words[1]["value"]):
          invoice_number = sorted_words[2]["value"]
          break

  return invoice_number

def getContractsForPage(page_idx,page):
  import re
  CurrentFound = page_idx != 0
  contracts = []

  for block in page["blocks"]:
    for line in block["lines"]:
      for word_idx,word in enumerate(sorted(line["words"], key = lambda x: x["geometry"][0][1])):
        if re.search("CURRENT",word["value"]):
          CurrentFound = True

        if not CurrentFound:
          continue

        if re.search("\d{3}-\d{7}-\d{3}",word["value"]):
          contracts.append({"contract_number": word["value"], "pdf_y": word["geometry"][0][1]+page_idx, "page": page_idx+1})
        else:
          continue

  return contracts

def getSerialNumbersForPage(page_idx,page):
  import re
  CurrentFound = page_idx != 0
  serialNumbers = []

  for block in page["blocks"]:
    for line_idx, line in enumerate(block["lines"]):
      for word_idx,word in enumerate(sorted(line["words"], key = lambda x: x["geometry"][0][1])):
        if re.search("CURRENT",word["value"]):
          CurrentFound = True

        if not CurrentFound:
          continue

        if re.search("SERIAL",word["value"]):
          if len(line["words"]) >= 3:
            serial_number_word = line["words"][2]
          else:
            serial_number_word = word
          serialNumbers.append({"serial_number": serial_number_word["value"], "pdf_y": serial_number_word["geometry"][0][1]+page_idx, "page": page_idx+1})
        else:
          continue

  return serialNumbers

def getPaymentDue(page_idx,page):
  import re
  CurrentFound = page_idx != 0
  PleaseFound = False
  prices = []

  for block in page["blocks"]:
    for line in block["lines"]:
      for word_idx,word in enumerate(sorted(line["words"], key = lambda x: x["geometry"][0][1])):
        if re.search("PLEASE",word["value"]):
          PleaseFound = True

        if not PleaseFound:
          continue

        if re.search("CURRENT",word["value"]):
          CurrentFound = True

        if not CurrentFound:
          continue

        if re.search("-{0,1}\d+\.\d{2}",word["value"]):
          prices.append({"price": word["value"], "pdf_y": word["geometry"][0][1]+page_idx, "page": page_idx+1})
        else:
          continue

  return prices

def convertToJson(sortedData):
  currentPage = 0

  response_list = []
  current_page_dict = {}
  current_contract_number_item = {}

  for contractSerialPair in sortedData:
    if contractSerialPair["page"] != currentPage:
      currentPage = contractSerialPair["page"]     
      response_list.append({"page": currentPage})
      current_page_dict = response_list[-1]
      current_page_dict["items"] = []

    if "contract_number" in contractSerialPair:
      current_page_dict["items"].append({"contract_number": contractSerialPair["contract_number"], "price": []})
      current_contract_number_item = current_page_dict["items"][-1]
    elif "serial_number" in contractSerialPair:
      current_contract_number_item["serial_number"] = contractSerialPair["serial_number"]
    elif "price" in contractSerialPair and "price" in current_contract_number_item:
        current_contract_number_item["price"].append(contractSerialPair["price"])
    else:
      logger.error(f"Item pair not found: {contractSerialPair}")

  return response_list

def calculateTotals(response_list):
  for response_page in response_list["pages"]:
    for response_item in response_page["items"]:
      response_item["total_price"] = float(0)
      for response_price in response_item["price"]:
        response_item["total_price"] = float(response_item["total_price"]) + float(response_price)
        response_item["total_price"] = str(round(response_item["total_price"],2))
  
  return response_list

def findSingleRowByItem(relavant_rows, item):
    return next((row for row in relavant_rows if (str(row[3].value) == str(item["contract_number"]) and str(row[1].value) == str(item["serial_number"]))),None)

def GetResponseFromFile(fileToParse):
  import json
  f = open(fileToParse)
  data = json.load(f)

  contracts = []
  serialNumbers = []
  paymentDue = []

  invoice_number = getInvoiceNumber(0,data["pages"][0])

  for page_idx,page in enumerate(data["pages"]):
    contracts += getContractsForPage(page_idx,page)
    serialNumbers += getSerialNumbersForPage(page_idx,page)
    paymentDue += getPaymentDue(page_idx,page)

  contractSerials = contracts + serialNumbers + paymentDue
  contractSerials = sorted(contractSerials, key = lambda x: x["pdf_y"])

  response_list = {"pages" : convertToJson(contractSerials), "invoice_number": invoice_number}
  response_list = calculateTotals(response_list)

  return response_list

def update_workbook(wb, file_path):
    import json
    ws = wb.active

    response_list = GetResponseFromFile(file_path)
    invoice_number = response_list["invoice_number"]
  
    for page in response_list["pages"]:
        for item in page["items"]:
            item_json_str = json.dumps(item)
            if not "contract_number" in item or not "serial_number" in item:
                logger.error("Item missing contract_number and/or serial_number: " + item_json_str)
                continue

            singleRow = findSingleRowByItem(ws.iter_rows(min_row = 6, max_col=17, max_row=127),item)
            if singleRow != None:
                singleRow[9].value = item["total_price"]
                singleRow[10].value = invoice_number
            else:
                logger.error("Unable to find record for item: " + item_json_str)
    
    return wb