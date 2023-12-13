import json
import typing

from borb.pdf import Document
from borb.pdf import PDF
from borb.toolkit import SimpleTextExtraction


def main():
    # read the Document
    doc: typing.Optional[Document] = None
    l: SimpleTextExtraction = SimpleTextExtraction()
    with open("./pdf/test2.pdf", "rb") as in_file_handle:
        doc = PDF.loads(in_file_handle, [l])

    # check whether we have read a Document
    assert doc is not None

    # print the text on the first Page
    data = l.get_text_from_pdf(doc)
    for text in data.values():
        print(text)


if __name__ == "__main__":
    main()
