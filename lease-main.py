from pylib.lease import *

def main():
  import json

  response_list = GetResponseFromFile("../jams/data/konica/2023-08.lease.508699675.doctr.json")

  json_formatted_str = json.dumps(response_list, indent=2)
  print(json_formatted_str)

if __name__ == "__main__":
    main()
