import pylib.doctr as doctr

def main():
    import os
    import json
    import argparse
    import time

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="../jams/data/konica/2023-11.lease.515780542.pdf")
    parser.add_argument("--output", type=str, default="../jams/data/konica/output/2023-11.lease.515780542.doctr2.json")
    args = parser.parse_args()

    print("input: " + args.input)
    print("output: "+ args.output)

    start_time = time.time()
    json_export = doctr.doctr_ocr_pdf(args.input)
    end_time = time.time()
    print(f"Time Taken: {end_time - start_time}")

    os.makedirs("../jams/data/konica/output/", exist_ok=True)
    out_file = open(args.output, "w")
    out_file.write(json.dumps(json_export, indent=2))

if __name__ == "__main__":
    main()