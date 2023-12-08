def main():
    import os
    import json
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="../jams/data/konica/2023-11.lease.515780542.pdf")
    parser.add_argument("--output", type=str, default="../jams/data/konica/output/2023-11.lease.515780542.doctr2.json")
    args = parser.parse_args()

    print("input: " + args.input)
    print("output: "+ args.output)

    # Let's pick the desired backend
    # os.environ['USE_TF'] = '1'
    os.environ['USE_TORCH'] = '1'

    from doctr.io import DocumentFile
    from doctr.models import ocr_predictor

    doc = DocumentFile.from_pdf(args.input)
    predictor = ocr_predictor(pretrained=True)
    result = predictor(doc)

    json_export = result.export()

    os.makedirs("../jams/data/konica/output/", exist_ok=True)
    out_file = open(args.output, "w")
    out_file.write(json.dumps(json_export, indent=2))

if __name__ == "__main__":
    main()