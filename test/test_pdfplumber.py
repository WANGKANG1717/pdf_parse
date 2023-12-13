import os
import pdfplumber

root_dir = "./pdf"
out_dir = "./pdf_out"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

file_names = os.listdir(root_dir)

for file_name in file_names:
    text = ""
    with pdfplumber.open("./pdf/test1.pdf") as pdf:
        for idx, page in enumerate(pdf.pages):
            print(page.images)
            text += page.extract_text()
            text += "\n"
            # print(page.extract_tables())
            img = page.to_image()
            # img.draw_rects(page.extract_words())
            if page.images:
                images = page.images
                print(type(images))
                rects = []
                for image in images:
                    image["top"] = image["y0"]
                    image["bottom"] = image["y1"]
                    image["bbox"] = [image["x0"], image["y0"], image["x1"], image["y1"]]
                    rects.append([image["x0"], image["y0"], image["x1"], image["y1"]])
                img.draw_rect(rects)
            # img.draw_rects(page.extract_text_lines())
            img.save(f"./images/extract_words_page{idx}.png", format="PNG")
    with open(
        os.path.join(root_dir, f"{file_name.removesuffix('.pdf')}_pdfplumber.txt"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(text)
