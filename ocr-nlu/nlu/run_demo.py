"""Run the complete OCR -> NLU -> Gemini report flow.

Usage:
    python -m nlu.run_demo samples/ocr_test_kabir_emergency_discharge_ocr.pdf
"""
import argparse
import json
from pathlib import Path

from ocr.engine import OCREngine
from .pipeline import NLUPipeline
from .llm import GeminiClient, ReportGenerator

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    parser.add_argument("--document-id", default=None)
    parser.add_argument("--model", default="gemini-3.5-flash-lite")
    parser.add_argument("--save-nlu", type=Path, default=None)
    args = parser.parse_args()

    document_id = args.document_id or args.file.stem
    ocr_result = OCREngine().process(args.file, document_id)
    if ocr_result.status != "COMPLETED":
        raise SystemExit(f"OCR failed: {ocr_result.metadata}")

    nlu_result = NLUPipeline().process(ocr_result)
    if args.save_nlu:
        args.save_nlu.write_text(nlu_result.model_dump_json(indent=2), encoding="utf-8")

    print(f"OCR: {len(ocr_result.extracted_text)} characters, confidence={ocr_result.confidence}")
    print(f"Document type: {nlu_result.document.document_type.value}")
    print(f"Candidate facts: {len(nlu_result.candidate_facts)}")
    print(f"Validation issues: {len(nlu_result.validation_issues)}")
    print("\nGemini report:\n")
    report = ReportGenerator(GeminiClient(model=args.model)).generate(nlu_result)
    try:
        print(json.dumps(json.loads(report), indent=2))
    except (TypeError, json.JSONDecodeError):
        print(report)

if __name__ == "__main__":
    main()
