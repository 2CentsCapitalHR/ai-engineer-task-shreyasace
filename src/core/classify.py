from typing import Dict, Any
import re

from src.core.docx_utils import extract_text

# Simple keyword maps for doc types
DOC_PATTERNS = {
    "Articles of Association": [r"articles of association", r"aoa"],
    "Memorandum of Association": [r"memorandum of association", r"moa"],
    "Shareholder Resolution": [r"shareholder resolution", r"written resolution"],
    "Board Resolution": [r"board resolution"],
    "Incorporation Application": [r"incorporation application", r"application to incorporate"],
    "UBO Declaration": [r"beneficial owner", r"ubo"],
    "Register of Members and Directors": [r"register of members", r"register of directors"],
    "Change of Registered Address": [r"change of registered address", r"registered office address"],
    "Employment Contract": [r"employment contract", r"employee", r"employer"],
}

PROCESS_RULES = {
    "Company Incorporation": [
        "Articles of Association",
        "Shareholder Resolution",
        "Register of Members and Directors",
    ],
    "Employment & HR": ["Employment Contract"],
}


def identify_doc_type(name: str, content: str) -> str:
    n = name.lower()
    c = content.lower()
    for dtype, pats in DOC_PATTERNS.items():
        for p in pats:
            if re.search(p, n) or re.search(p, c):
                return dtype
    return "Unknown"


def detect_process_and_types(file_bytes: Dict[str, bytes]) -> Dict[str, Any]:
    documents = {}
    types_present = set()
    for fname, raw in file_bytes.items():
        try:
            text, _ = extract_text(raw)
            dtype = identify_doc_type(fname, text)
            types_present.add(dtype)
            documents[fname] = {"type": dtype, "text": text}
        except Exception as e:
            # Record a safe placeholder and move on; UI can surface this to the user.
            documents[fname] = {"type": "Unknown", "text": "", "error": f"Failed to read DOCX: {e}"}

    # Process detection
    process = "Unknown"
    score = {k: 0 for k in PROCESS_RULES}
    for proc, must in PROCESS_RULES.items():
        for m in must:
            if m in types_present:
                score[proc] += 1
    if score:
        process = max(score, key=score.get)
        if score[process] == 0:
            process = "Unknown"

    return {"process": process, "documents": documents}
