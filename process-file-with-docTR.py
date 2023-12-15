import pylib.doctr as doctr
import pylib.common as common

def main():
    import os
    import json
    import argparse
    import time

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="../jams/data/konica/2023-11.lease.515780542.pdf")
    parser.add_argument("--output", type=str)
    args = parser.parse_args()

    if args.output is None:
        args.output = common.convert_pdf_to_doctr_cache(args.input)

    print("input: " + args.input)
    print("output: "+ args.output)

    start_time = time.time()
    json_export = doctr.doctr_ocr_pdf(args.input)
    end_time = time.time()
    print(f"Time Taken: {end_time - start_time}")

    common.write_json_output(args.output, json_export)

if __name__ == "__main__":
    main()