
```python

import os
import fitz  # PyMuPDF
from markdownify import markdownify as md

def extract_text_with_structure(pdf_path):
    doc = fitz.open(pdf_path)
    html = ""

    for page in doc:
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue

                    size = span["size"]

                    if size >= 18:
                        html += f"<h1>{text}</h1>\n"
                    elif size >= 16:
                        html += f"<h2>{text}</h2>\n"
                    elif size >= 14:
                        html += f"<h3>{text}</h3>\n"
                    else:
                        html += f"<p>{text}</p>\n"

    return html


def pdf_to_markdown(pdf_path, md_out_path):
    print(f"Processing: {os.path.basename(pdf_path)}")

    html = extract_text_with_structure(pdf_path)
    markdown = md(html, heading_style="ATX")

    with open(md_out_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"✔ Saved markdown → {md_out_path}")


def convert_folder(folder):
    print(f"Scanning folder: {folder}\n")

    for file in os.listdir(folder):
        if file.lower().endswith(".pdf"):
            input_file = os.path.join(folder, file)
            output_file = os.path.join(folder, file.replace(".pdf", ".md"))

            pdf_to_markdown(input_file, output_file)

    print("\n✔ All PDFs converted!")


if __name__ == "__main__":
    folder_path = input("Enter folder containing PDF files: ")
    convert_folder(folder_path)
