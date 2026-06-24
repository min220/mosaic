import pymupdf

def parse_pdf(filepath):
    doc = pymupdf.open(filepath)
    chunks = []
    for page_num, page in enumerate(doc):
        text = page.get_text()
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        for i, para in enumerate(paragraphs):
            chunks.append({
                "source": filepath,
                "page": page_num,
                "chunk_index": i,
                "text": para
            })
    return chunks

if __name__ == "__main__":
    chunks = parse_pdf("a.pdf")
    for c in chunks:
        print(c)