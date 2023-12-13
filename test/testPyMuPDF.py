import fitz  # imports the pymupdf library

doc = fitz.open("./pdf/test2.pdf")  # open a document
for page in doc:  # iterate the document pages
    text = page.get_text()  # get plain text encoded as UTF-8
    print(text)
