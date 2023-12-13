import os
import time
from pdfminer.high_level import extract_text

start_time = time.time()

root_dir = "./pdf"
out_dir = "./pdf_out"
package_name = "pdfminer"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

file_names = os.listdir(root_dir)

for file_name in file_names:
    text = extract_text(os.path.join(root_dir, file_name))
    # print(text)
    with open(
        os.path.join(out_dir, f"{file_name.removesuffix('.pdf')}_{package_name}.txt"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(text)
end_time = time.time()
print(f"{package_name} -- 所用时间:{end_time - start_time: 0.2f}s")
