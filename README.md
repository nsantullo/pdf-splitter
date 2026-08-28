# pdf-splitter

Python script to split large PDFs into smaller chunks by file size and/or page count — useful for staying under upload limits of AI chat tools like Claude.

## Features
- Splits by target file size (MB) and/or max page count per chunk
- Handles PDFs with mixed page sizes (e.g. scanned/image-heavy documents)
- Outputs all chunks into a dedicated `output/` folder

## Requirements
- Python 3.8+
- `pypdf` (`pip3 install pypdf`)

## Usage
```bash
python3 split_pdf.py your_file.pdf --max-mb 25 --max-pages 100
```

## Options
- `--max-mb`: max size per chunk in MB (default: 25)
- `--max-pages`: max pages per chunk (default: 100)
- `--outdir`: custom output folder (default: `output/` next to the input file)
