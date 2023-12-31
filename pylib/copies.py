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
			for word_idx,word in enumerate(sorted_words):
				if re.search("Invoice",word["value"]) and re.search("Nbr:",sorted_words[1]["value"]):
					invoice_number = sorted_words[2]["value"]
					break

	return invoice_number

def getInvoiceTotal(page_idx,page):
	import re
	StartingPlaceFound = page_idx != 0
	invoice_total = ""

	for block in page["blocks"]:
		if invoice_total != "":
			break
		for line in block["lines"]:
			if invoice_total != "":
				break
			sorted_words = sorted(line["words"], key = lambda x: x["geometry"][0][0])
			if len(sorted_words) == 4:
				if re.search("This",sorted_words[1]["value"]):
					invoice_total = sorted_words[3]["value"]
					break

	return invoice_total

def getContractsForPage(page_idx,page):
	import re
	StartingPlaceFound = page_idx != 0
	contracts = []
	
	for block in page["blocks"]:
		for line in block["lines"]:
			for word_idx,word in enumerate(sorted(line["words"], key = lambda x: x["geometry"][0][1])):
				if re.search("Unit",word["value"]):
					StartingPlaceFound = True

				if not StartingPlaceFound:
					continue
				
				if re.search("Contract",word["value"]):
					if len(line["words"])>=3:
						contract_number_word = line["words"][2]
						if re.search("\d{8}",contract_number_word["value"]): 
							contracts.append({"contract_number": contract_number_word["value"], "pdf_y": contract_number_word["geometry"][0][1]+page_idx, "page": page_idx+1})
				else:
					continue
						
	return contracts

def getSerialNumbersForPage(page_idx,page):
	import re
	StartingPlaceFound = page_idx != 0
	serialNumbers = []

	for block in page["blocks"]:
		for line_idx,line in enumerate(block["lines"]):
			sorted_words = sorted(line["words"], key = lambda x: x["geometry"][0][1])  
			for word_idx,word in enumerate(sorted_words):
				if re.search("Unit",word["value"]):
					StartingPlaceFound = True

				if not StartingPlaceFound:
					continue

				if re.search("Contract",word["value"]):
					if len(line["words"])>=3:
						contract_number_word = line["words"][2]
						if re.search("\d{8}",contract_number_word["value"]): 
							serial_number_word = block["lines"][line_idx+1]["words"][0]
							if serial_number_word["value"][4] == 'O':
								serial_number_word["value"] = serial_number_word["value"][:4] + "0" + serial_number_word["value"][5:]  
							serialNumbers.append({"serial_number": serial_number_word["value"], "pdf_y": serial_number_word["geometry"][0][1]+page_idx, "page": page_idx+1})
				else:
					continue

	return serialNumbers

def getPaymentDue(page_idx,page):

	import re
	StartingPlaceFound = page_idx != 0
	prices = []
	
	for block in page["blocks"]:
		for line in block["lines"]:
			for word_idx,word in enumerate(sorted(line["words"], key = lambda x: x["geometry"][0][1])):
				if re.search("\$\-{0,1}\d+\.\d{2}",word["value"]):
					prices.append({"price": word["value"], "pdf_y": word["geometry"][0][1]+page_idx, "page": page_idx+1})
				else:
					continue

	return prices


def convertToJson(sortedData,invoice_number,invoice_total):

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
			current_page_dict["items"].append({"contract_number": contractSerialPair["contract_number"], "serial_number": [], "price": [], "invoice_number":invoice_number, "invoice_total":invoice_total })
			current_contract_number_item = current_page_dict["items"][-1]
		elif "serial_number" in contractSerialPair:
			current_contract_number_item["serial_number"] = contractSerialPair["serial_number"]
		elif "price" in contractSerialPair:
			current_contract_number_item["price"].append(contractSerialPair["price"])
		else:
			logger.error("Error unknown pair: " + contractSerialPair)

	return response_list

def findSingleRowByItem(relavant_rows, item):
    return next((row for row in relavant_rows if (str(row[4].value) == str(item["contract_number"]) and str(row[1].value) == str(item["serial_number"]))),None)

def GetResponseFromFile(fileToParse):
	import json
	import os
	
	f = open(os.path.abspath(fileToParse))
	data = json.load(f)

	contracts = []
	serialNumbers = []
	paymentDue = []
	invoice_number = ""
	invoice_total = ""

	for page_idx,page in enumerate(data["pages"]):
		if invoice_number == "":
			invoice_number = getInvoiceNumber(page_idx,page)
		if invoice_total == "":
			invoice_total = getInvoiceTotal(page_idx,page)
		contracts += getContractsForPage(page_idx,page)
		serialNumbers += getSerialNumbersForPage(page_idx,page)
		paymentDue += getPaymentDue(page_idx,page)

	contractSerials = contracts + serialNumbers + paymentDue
	contractSerials = sorted(contractSerials, key = lambda x: x["pdf_y"])

	return convertToJson(contractSerials,invoice_number,invoice_total)

def update_workbook(wb, file_path):
    import json
    ws = wb.active

    response_list = GetResponseFromFile(file_path)
    
    for page in response_list:
        for item in page["items"]:
            item_json_str = json.dumps(item)
            if not "contract_number" in item or not "serial_number" in item:
                logger.error("Invalid item: " + item_json_str)
                continue

            singleRow = findSingleRowByItem(ws.iter_rows(min_row = 6, max_col=17, max_row=127),item)
            if singleRow != None:
                singleRow[15].value = item["price"][0]
                singleRow[16].value = item["invoice_number"]
            else:
                logger.error("Unable to find record for item: " + item_json_str)

    return wb

def convertResponseJsonToCsv(response_list):
	import json
	
	csv_output = "page,contract_number,serial_number,invoice_amount,invoice_number,invoice_total\r\n"
	
	for page in response_list:
		for item in page["items"]:
			csv_output += str(page["page"])+","+item["contract_number"]+","+item["serial_number"]+",\""+json.dumps(item["price"]).replace("\"","\"\"")+"\","+item["invoice_number"]+",\""+item["invoice_total"]+"\"\r\n"
	
	return csv_output

