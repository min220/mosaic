# mosaic

An agentic document privacy auditing pipeline that detects sensitive information leakage, including cross-document inference risks that no single document reveals alone.

what it does

Most privacy tools scan documents one at a time. Mosaic goes further: it reasons across a set of documents to detect what can be inferred by combining them, even when each document looks clean individually. This is the mosaic effect: the phenomenon where individually innocuous pieces of information, aggregated, disclose something sensitive that none of them would alone.

A document with a full name is low risk. A document with a college affiliation is low risk. A document with a graduation year is low risk. Together, they create a precise, actionable profile of a private individual, enough to locate them, contact them, or target them. Mosaic catches that.

I built this because the more I've learned about how LLMs reason over unstructured text, the more interesting the gap between single-document and cross-document privacy analysis became to me. Existing tools are basically pattern matchers. The real problem is an inference problem, and that's a much better fit for how LLMs actually work.

how it works

Documents -> Ingestion -> Single-doc Detection -> Cross-doc Inference -> Structured Findings

Ingestion (ingestion/parser.py) parses PDFs and text files, splits content into semantic chunks at the paragraph level rather than fixed character counts, and attaches metadata including source filename, page number, and chunk index.

Detection (detection/detector.py) sends each chunk to Claude with a privacy auditor prompt and returns structured findings per chunk: entity, category (PII / FINANCIAL / LOCATION / ORGANIZATION / CREDENTIAL), confidence score, and a reasoning trace explaining why the entity is sensitive.

Mosaic Inference (inference/mosaic.py) aggregates flagged entities across all documents and runs a second LLM reasoning step: given everything found, what can be inferred from combining these signals? Returns cross-document inferences with severity ratings and a plain-language disclosure summary.

stack


Python / FastAPI
PyMuPDF
Anthropic Claude API
React (dashboard, in progress)


setup

bashpip install pymupdf anthropic fastapi uvicorn
export ANTHROPIC_API_KEY=your_key_here

run

bash# single-document detection
python -m detection.detector

# full pipeline with mosaic inference
python -m inference.mosaic

output

json{
  "mosaic_risk": "HIGH",
  "inferences": [
    {
      "entities_combined": ["Full Name", "Institution", "Graduation Year"],
      "sources_involved": ["doc1.pdf"],
      "inferred_disclosure": "Sufficient to uniquely identify a private individual within an institution, infer age and academic standing, and locate them via directories or social media.",
      "severity": "HIGH"
    }
  ],
  "summary": "..."
}

project structure

mosaic/
  ingestion/
    parser.py       # PDF + text parsing, semantic chunking
  detection/
    detector.py     # per-chunk PII and sensitive entity detection
  inference/
    mosaic.py       # cross-document inference engine
  api/              # FastAPI layer (in progress)
  dashboard/        # React frontend (in progress)
  evals/            # synthetic dataset + precision/recall benchmarks (in progress)

why this matters

Enterprise document workflows, legal review, compliance audits, FOIA requests, data room due diligence, involve large sets of documents that get reviewed individually but leaked collectively. Existing tools flag PII in isolation. Mosaic flags what the documents reveal together.
