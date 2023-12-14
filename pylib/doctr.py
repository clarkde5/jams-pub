def doctr_ocr_pdf(pdf_file):
    import os
    os.environ['USE_TORCH'] = '1'

    from doctr.io import DocumentFile
    from doctr.models import ocr_predictor

    doc = DocumentFile.from_pdf(pdf_file)
    predictor = ocr_predictor(pretrained=True)
    result = predictor(doc)

    return result.export()