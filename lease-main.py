def main():
  import json
  from lease import getInvoiceNumber, \
                    getContractsForPage, \
                    getSerialNumbersForPage, \
                    getPaymentDue, \
                    convertToJson, \
                    calculateTotals
  
  f = open('src/jams/output/Aug 23 Lease-docTR.json')
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


  json_formatted_str = json.dumps(response_list, indent=2)
  print(json_formatted_str)

if __name__ == "__main__":
    main()
