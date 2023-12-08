from pylib.lease import *

def main():
  import json

  response_list = GetResponseFromFile("../jams/output/Aug 23 Lease-docTR.json")

  json_formatted_str = json.dumps(response_list, indent=2)
  print(json_formatted_str)

if __name__ == "__main__":
    main()
