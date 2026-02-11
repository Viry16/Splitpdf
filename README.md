# PDF Splitter

A simple tool to split large PDF files into smaller chunks, making them easier to upload to GitHub or send via email. This project includes both a graphical web interface (Streamlit) and a command-line script.

## Features

- **Split by Chunk Size**: Specify the number of pages per PDF file (e.g., 50 pages per file).
- **Extract Single Pages**: Option to save every page as an individual PDF.
- **Zip Download**: Download all split files as a single ZIP archive.
- **Local Save**: If running locally, you can save directly to an `output/` folder.

## Prerequisites

Make sure you have Python installed. Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### 1. Web Interface (Streamlit)

The easiest way to use the tool is via the web interface.

Run the following command:

```bash
streamlit run streamlit_app.py
```

This will open a local web server (usually at `http://localhost:8501`) where you can upload your PDF and download the split files.

### 2. Command Line Interface (CLI)

You can also use the script directly from the terminal without a UI.

**Syntax:**

```bash
python split_pdf.py <input_pdf_path> [--pages <number_of_pages>] [--output <output_directory>]
```

**Examples:**

- Split `my_large_file.pdf` into chunks of 50 pages (default):

  ```bash
  python split_pdf.py my_large_file.pdf
  ```

- Split into chunks of 10 pages:

  ```bash
  python split_pdf.py my_large_file.pdf --pages 10
  ```

- Save to a specific folder:
  ```bash
  python split_pdf.py my_large_file.pdf --output my_split_files
  ```

## Files

- `streamlit_app.py`: The main application code for the Streamlit web interface.
- `split_pdf.py`: The Python script for command-line usage.
- `requirements.txt`: List of Python dependencies.
