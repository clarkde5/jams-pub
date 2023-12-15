from pylib.copies import *
import pylib.common as common

def main():
	import json

	input_file = "../jams/data/konica/doctr/2023-08.copies.9009520780.doctr.json"
	response_list = GetResponseFromFile(input_file)

	json_output_file = common.convertExtension(common.convertToOutputPath(input_file),".doctr.json",".json")
	common.write_text_output(json_output_file, json.dumps(response_list, indent=2))

	csv_output_file = common.convertExtension(common.convertToOutputPath(input_file),".doctr.json",".csv")
	common.write_text_output(csv_output_file, convertResponseJsonToCsv(response_list))
	
if __name__ == "__main__":
	main()
