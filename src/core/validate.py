from typing import Dict, Any, List
import re

from src.rag.retrieve import cite_rules

# Minimal deterministic checks; citations are attached via RAG stub
REQUIRED_DOCS = {
    "Company Incorporation": [
        "Articles of Association",
        "Shareholder Resolution",
        "Register of Members and Directors",
        "UBO Declaration",
        "Incorporation Application",
    ],
    "Employment & HR": ["Employment Contract"],
}


def check_jurisdiction(text: str) -> List[Dict[str, Any]]:
    issues = []
    if re.search(r"uae federal court|mainland|dubai courts|abu dhabi courts", text, re.I):
        issues.append({
            "issue": "Jurisdiction refers outside ADGM",
            "severity": "High",
            "suggestion": "Replace forum with ADGM Courts and ADGM governing law, as applicable.",
            "citations": cite_rules(["companies_regulations_formation", "adgm_courts"]),
        })
    return issues


def check_registered_office(text: str) -> List[Dict[str, Any]]:
    if not re.search(r"registered\s+office|al maryah|adgm", text, re.I):
        return [{
            "issue": "No ADGM registered office found",
            "severity": "High",
            "suggestion": "Add the ADGM registered office address in Abu Dhabi Global Market.",
            "citations": cite_rules(["companies_registrations_registered_office", "checklist_registered_office"]),
        }]
    return []


def check_signature_block(text: str) -> List[Dict[str, Any]]:
    patterns = [r"signed by", r"signature", r"name:\s+", r"date:\s+"]
    if not any(re.search(p, text, re.I) for p in patterns):
        return [{
            "issue": "Missing signature/date block",
            "severity": "Medium",
            "suggestion": "Add Name, Title, Signature, Date at the end.",
            "citations": cite_rules(["checklist_evidence_of_appointment"]),
        }]
    return []


def check_governing_law(text: str) -> List[Dict[str, Any]]:
    issues = []
    # If governing law appears, ensure it's ADGM or Abu Dhabi Global Market
    if re.search(r"governing\s+law|law\s+of", text, re.I):
        if not re.search(r"adgm|abu dhabi global market", text, re.I):
            issues.append({
                "issue": "Governing law not set to ADGM",
                "severity": "High",
                "suggestion": "Set governing law to Abu Dhabi Global Market (ADGM) where appropriate.",
                "citations": cite_rules(["companies_regulations_formation", "adgm_courts"]),
            })
    return issues


def check_defined_terms_section(text: str) -> List[Dict[str, Any]]:
    if not re.search(r"definitions|interpretation", text, re.I):
        return [{
            "issue": "No Definitions/Interpretation section",
            "severity": "Medium",
            "suggestion": "Add a Definitions/Interpretation section to standardize capitalized terms.",
            "citations": cite_rules(["companies_best_practices_drafting"]),
        }]
    return []


def check_clause_numbering(text: str) -> List[Dict[str, Any]]:
    # Heuristic: expect at least some numbered clauses like 1., 1.1 or similar
    if not re.search(r"\b\d+\.(?:\d+\.)?\s", text):
        return [{
            "issue": "Clauses not clearly numbered",
            "severity": "Low",
            "suggestion": "Number clauses (e.g., 1., 1.1, 1.2) for readability and cross-referencing.",
            "citations": cite_rules(["companies_best_practices_drafting"]),
        }]
    return []


def check_signing_authority(text: str) -> List[Dict[str, Any]]:
    if not re.search(r"authori[sz]ed\s+signator|director|company secretary", text, re.I):
        return [{
            "issue": "Signing authority not evident",
            "severity": "Medium",
            "suggestion": "Identify the authorised signatory (e.g., Director) in the execution block.",
            "citations": cite_rules(["checklist_evidence_of_appointment"]),
        }]
    return []


def employment_minimums(text: str) -> List[Dict[str, Any]]:
    reqs = {
        "names": r"employee|employer",
        "start": r"start date|commencement",
        "job": r"job title|position",
        "wages": r"wage|salary|compensation",
        "pay_period": r"pay period|monthly|weekly",
        "hours": r"hours of work|working hours",
        "leave": r"annual leave|vacation|sick leave",
        "notice": r"notice|termination",
        "place": r"place of work|remote",
        "grievance": r"disciplinary|grievance",
    }
    issues = []
    for key, pat in reqs.items():
        if not re.search(pat, text, re.I):
            issues.append({
                "issue": f"Employment: missing {key.replace('_', ' ')}",
                "severity": "High" if key in {"wages", "pay_period", "leave", "notice"} else "Medium",
                "suggestion": f"Add {key.replace('_', ' ')} per Employment Regulations 2024.",
                "citations": cite_rules(["employment_regulations_minimums", "employment_standard_template"]),
            })
    return issues


DOC_CHECKS = {
    "Articles of Association": [check_jurisdiction, check_registered_office, check_governing_law, check_defined_terms_section, check_clause_numbering],
    "Shareholder Resolution": [check_signature_block, check_signing_authority],
    "Board Resolution": [check_signature_block, check_signing_authority],
    "Incorporation Application": [check_registered_office, check_governing_law],
    "UBO Declaration": [],
    "Register of Members and Directors": [],
    "Employment Contract": [employment_minimums],
}


def analyze_bundle(proc_info: Dict[str, Any]) -> Dict[str, Any]:
    process = proc_info.get("process", "Unknown")
    docs = proc_info.get("documents", {})
    types = [d["type"] for d in docs.values()]

    required = REQUIRED_DOCS.get(process, [])
    missing = [r for r in required if r not in types]

    issues: List[Dict[str, Any]] = []
    for name, meta in docs.items():
        dtype = meta["type"]
        text = meta["text"]
        for check in DOC_CHECKS.get(dtype, []):
            found = check(text)
            for f in found:
                f.update({"document": name, "location": None})
            issues.extend(found)

    # Cross-document consistency checks
    try:
        parties = []
        dates = []
        addresses = []
        party_pat = re.compile(r"(company|employer|shareholder|director|party)\s*:\s*([A-Z][A-Za-z0-9 &.,'-]{2,})", re.I)
        date_pat = re.compile(r"\b(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}|\d{4}-\d{2}-\d{2})\b")
        address_pat = re.compile(r"(registered\s+office|address)\s*:\s*([^\n\r]{5,})", re.I)
        for name, meta in docs.items():
            text = meta.get("text", "")
            for m in party_pat.finditer(text):
                parties.append((name, m.group(1).lower(), m.group(2).strip()))
            for m in date_pat.finditer(text):
                dates.append((name, m.group(0)))
            for m in address_pat.finditer(text):
                addresses.append((name, m.group(1).lower(), m.group(2).strip()))

        # Helper to detect mismatches
        def first_value(items):
            return items[0] if items else None

        # Parties by role
        suffix_pat = re.compile(r"\b(ltd|limited|llc|inc|co\.?|company|fzc|plc)\.?$", re.I)
        def norm_party(s: str) -> str:
            s = s.strip()
            s = re.sub(suffix_pat, "", s).strip()
            s = re.sub(r"\s+", " ", s)
            return s.lower()
        role_to_values = {}
        for _, role, value in parties:
            role_to_values.setdefault(role, set()).add(norm_party(value))
        for role, vals in role_to_values.items():
            if len(vals) > 1:
                issues.append({
                    "issue": f"Cross-document mismatch: {role} names differ",
                    "severity": "Medium",
                    "suggestion": f"Align the {role} name across all documents: {', '.join(sorted(vals))}.",
                    "citations": cite_rules(["companies_best_practices_drafting"]),
                })

        # Dates (effective/commencement) consistency heuristic
        unique_dates = set([d for _, d in dates])
        if len(unique_dates) > 1 and len(unique_dates) <= 6:
            issues.append({
                "issue": "Cross-document mismatch: dates are inconsistent",
                "severity": "Low",
                "suggestion": f"Confirm effective/commencement dates; found: {', '.join(sorted(unique_dates))}.",
                "citations": cite_rules(["companies_best_practices_drafting"]),
            })

        # Registered office/address consistency
        addr_values = set([v for _, _, v in addresses])
        if addr_values and len(addr_values) > 1:
            issues.append({
                "issue": "Cross-document mismatch: registered office/address differs",
                "severity": "Medium",
                "suggestion": f"Confirm the registered office/address across documents: {', '.join(sorted(addr_values))}.",
                "citations": cite_rules(["companies_registrations_registered_office"]),
            })
    except Exception:
        # Best-effort; ignore extraction failures
        pass

    # Compute a simple compliance score (0-100)
    score = 100
    for it in issues:
        sev = (it.get('severity') or '').lower()
        if sev == 'high':
            score -= 8
        elif sev == 'medium':
            score -= 4
        elif sev == 'low':
            score -= 1
    score -= 5 * len(missing)
    if score < 0:
        score = 0
    if score > 100:
        score = 100

    report = {
        "process": process,
        "documents_uploaded": len(docs),
        "required_documents": len(required),
        "missing_documents": missing,
        "issues_found": issues,
        "compliance_score": score,
    }
    return report
