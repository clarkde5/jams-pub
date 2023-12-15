from pylib.lease import *

def main():
  import json

  input_file = "../jams/data/konica/doctr/2023-08.lease.508699675.doctr.json"
  response_list = GetResponseFromFile(input_file)

  json_output_file = common.convertExtension(common.convertToOutputPath(input_file),".doctr.json",".json")
  common.write_text_output(json_output_file, json.dumps(response_list, indent=2))

if __name__ == "__main__":
    main()
