from extractor import extract_pdf_text
from llm_processor import extract_key_values
from excel_writer import write_to_excel

def main():
    pdf_path = "../Data Input.pdf"
    output_path = "../Output.xlsx"

    print("Extracting PDF...")
    full_text = extract_pdf_text(pdf_path)

    print("Sending full text to LLM (single call)...")
    rows = extract_key_values(full_text)

    print("Writing Excel...")
    write_to_excel(rows, output_path)

    print("DONE! Output saved to Output.xlsx")

if __name__ == "__main__":
    main()
