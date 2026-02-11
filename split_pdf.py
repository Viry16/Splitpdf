import os
import argparse
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_path, output_dir, pages_per_chunk):
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        
        print(f" splitting '{input_path}' with {total_pages} pages into chunks of {pages_per_chunk} pages...")

        for i in range(0, total_pages, pages_per_chunk):
            writer = PdfWriter()
            chunk_start = i
            chunk_end = min(i + pages_per_chunk, total_pages)
            
            for page_num in range(chunk_start, chunk_end):
                writer.add_page(reader.pages[page_num])
            
            output_filename = f"{os.path.splitext(os.path.basename(input_path))[0]}_part_{i // pages_per_chunk + 1}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
            
            print(f"Created: {output_path} (Pages {chunk_start + 1}-{chunk_end})")

        print("Done!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a PDF file into smaller chunks.")
    parser.add_argument("input_pdf", help="Path to the input PDF file.")
    parser.add_argument("--pages", type=int, default=50, help="Number of pages per chunk (default: 50).")
    parser.add_argument("--output", default="output", help="Directory to save split files (default: 'output').")

    args = parser.parse_args()
    
    split_pdf(args.input_pdf, args.output, args.pages)
