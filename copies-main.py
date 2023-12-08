from pylib.copies import *

def main():
	import json
	import os

	response_list = GetResponseFromFile("../jams/data/konica/2023-08.copies.9009520780.doctr.json")
	
	# json_formatted_str = json.dumps(response_list, indent=2)
	csv_output = "page,contract_number,serial_number,invoice_amount,invoice_number,invoice_total\r\n"
	for page in response_list:
		for item in page["items"]:
			csv_output += str(page["page"])+","+item["contract_number"]+","+item["serial_number"]+",\""+json.dumps(item["price"]).replace("\"","\"\"")+"\","+item["invoice_number"]+",\""+item["invoice_total"]+"\"\r\n"

	os.makedirs("../jams/data/konica/output/", exist_ok=True)
	csv_file_out = open(os.path.abspath("../jams/data/konica/output/2023-08.copies.9009520780.copies-main.csv"), "w")
	csv_file_out.write(csv_output)
	

if __name__ == "__main__":
	main()
