from assignment_api import *

import pdfplumber

def main():
    for file_path in [f"resources/chart{i}.pdf" for i in [1,2,3]]:
        with pdfplumber.open(file_path) as pdf:
            print(pdf_to_extra_dict(pdf).items())
if __name__ == "__main__":
    main()