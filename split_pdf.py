#!/usr/bin/env python3
"""
Split a large PDF into smaller chunks, targeting a max size per chunk (in MB)
and/or a max number of pages per chunk.

Usage:
    pip install pypdf
    python split_pdf.py input.pdf --max-mb 25 --max-pages 100
"""

import argparse
import os
from typing import Optional
from pypdf import PdfReader, PdfWriter


def split_pdf(input_path: str, max_mb: float, max_pages: int, outdir: Optional[str] = None):
    max_bytes = max_mb * 1024 * 1024
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)

    base = os.path.splitext(os.path.basename(input_path))[0]
    outdir = outdir or os.path.join(os.path.dirname(os.path.abspath(input_path)), "output")
    os.makedirs(outdir, exist_ok=True)

    part_num = 1
    writer = PdfWriter()
    pages_in_current_writer = 0

    def flush(writer, part_num, pages_in_current_writer):
        if pages_in_current_writer == 0:
            return
        out_path = os.path.join(outdir, f"{base}_part{part_num}.pdf")
        with open(out_path, "wb") as f:
            writer.write(f)
        size_mb = os.path.getsize(out_path) / (1024 * 1024)
        print(f"Wrote {out_path}  ({pages_in_current_writer} pages, {size_mb:.1f} MB)")

    for i in range(total_pages):
        writer.add_page(reader.pages[i])
        pages_in_current_writer += 1

        import io
        buf = io.BytesIO()
        writer.write(buf)
        current_size = buf.tell()

        is_last_page = (i == total_pages - 1)
        hit_size_limit = current_size >= max_bytes
        hit_page_limit = pages_in_current_writer >= max_pages

        if hit_size_limit or hit_page_limit or is_last_page:
            flush(writer, part_num, pages_in_current_writer)
            part_num += 1
            writer = PdfWriter()
            pages_in_current_writer = 0

    print(f"\nDone. {total_pages} pages split into {part_num - 1} file(s) in '{outdir}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a large PDF into smaller chunks by size and/or page count.")
    parser.add_argument("input_pdf", help="Path to the large PDF file")
    parser.add_argument("--max-mb", type=float, default=25, help="Max size per chunk in MB (default: 25)")
    parser.add_argument("--max-pages", type=int, default=100, help="Max pages per chunk (default: 100)")
    parser.add_argument("--outdir", help="Output directory (default: 'output' subfolder next to the input file)")
    args = parser.parse_args()

    split_pdf(args.input_pdf, args.max_mb, args.max_pages, args.outdir)
