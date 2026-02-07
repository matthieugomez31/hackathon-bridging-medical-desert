#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  7 12:20:10 2026

@author: castellimarcu-andria
"""

import json
import re
from pathlib import Path

import fitz  # PyMuPDF
import pdfplumber
from docx import Document
from bs4 import BeautifulSoup

DATA_DIR = Path("data")
OUT_DIR = Path("processed")
DOCS_OUT = OUT_DIR / "docs_text.jsonl"
CHUNKS_OUT = OUT_DIR / "chunks.jsonl"

CHUNK_SIZE = 2500
CHUNK_OVERLAP = 300


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"-\n(\w)", r"\1", text)  # enlève césures simples
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + chunk_size, n)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append((start, end, chunk))
        start = end - overlap
        if start < 0:
            start = 0
        if start >= n:
            break
    return chunks


def extract_pdf_text(path: Path) -> dict:
    try:
        doc = fitz.open(str(path))
        pages = [doc[i].get_text("text") for i in range(len(doc))]
        return {"text": "\n".join(pages), "page_count": len(doc), "method": "pymupdf"}
    except Exception:
        pages = []
        with pdfplumber.open(str(path)) as pdf:
            for p in pdf.pages:
                pages.append(p.extract_text() or "")
        return {"text": "\n".join(pages), "page_count": len(pages), "method": "pdfplumber"}


def extract_docx_text(path: Path) -> dict:
    doc = Document(str(path))
    return {"text": "\n".join([p.text for p in doc.paragraphs]), "method": "python-docx"}


def extract_html_text(path: Path) -> dict:
    html = path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return {"text": soup.get_text("\n"), "method": "beautifulsoup4"}


def extract_text(path: Path) -> dict:
    ext = path.suffix.lower()
    if ext == ".pdf":
        return extract_pdf_text(path)
    if ext == ".docx":
        return extract_docx_text(path)
    if ext in [".html", ".htm"]:
        return extract_html_text(path)
    return {"text": path.read_text(encoding="utf-8", errors="ignore"), "method": "text"}


def main():
    OUT_DIR.mkdir(exist_ok=True, parents=True)

    # reset outputs
    if DOCS_OUT.exists():
        DOCS_OUT.unlink()
    if CHUNKS_OUT.exists():
        CHUNKS_OUT.unlink()

    files = [p for p in DATA_DIR.rglob("*")
             if p.is_file() and p.suffix.lower() in [".pdf", ".docx", ".html", ".htm", ".txt"]]

    if not files:
        print("❌ Aucun fichier dans data/. Mets un PDF/DOCX/HTML/TXT dans data/ puis relance.")
        return

    doc_counter = 0
    chunk_counter = 0

    with DOCS_OUT.open("w", encoding="utf-8") as f_docs, CHUNKS_OUT.open("w", encoding="utf-8") as f_chunks:
        for path in files:
            doc_counter += 1
            doc_id = f"doc{doc_counter}"

            raw = extract_text(path)
            text = clean_text(raw.get("text", ""))

            f_docs.write(json.dumps({
                "doc_id": doc_id,
                "source_path": str(path),
                "file_type": path.suffix.lower().lstrip("."),
                "extraction_method": raw.get("method"),
                "page_count": raw.get("page_count"),
                "text": text
            }, ensure_ascii=False) + "\n")

            for (start, end, chunk) in chunk_text(text):
                chunk_counter += 1
                f_chunks.write(json.dumps({
                    "chunk_id": f"{doc_id}_chunk{chunk_counter}",
                    "doc_id": doc_id,
                    "source_path": str(path),
                    "char_start": start,
                    "char_end": end,
                    "text": chunk
                }, ensure_ascii=False) + "\n")

    print(f"✅ Terminé. Docs: {doc_counter} | Chunks: {chunk_counter}")
    print(f"→ {DOCS_OUT}")
    print(f"→ {CHUNKS_OUT}")


if __name__ == "__main__":
    main()
