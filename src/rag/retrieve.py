from typing import List

# Minimal citation registry. Replace with FAISS-backed retrieval later.
CITATION_REGISTRY = {
    "companies_regulations_formation": "[CR2020] Companies Regulations 2020 — Formation & Registration documents",
    "companies_registrations_registered_office": "[CR2020-RO] Companies Regulations 2020 — Registered Office in ADGM",
    "checklist_registered_office": "[CHK] ADGM Registration & Incorporation checklist — Registered office details",
    "checklist_evidence_of_appointment": "[CHK] ADGM checklist — Evidence of appointment / signatures",
    "employment_regulations_minimums": "[ER2024] Employment Regulations 2024 — Minimum contents of employment contract",
    "employment_standard_template": "[TEMP2025] ADGM Standard Employment Contract Template (2025)",
    "adgm_courts": "[COURTS] ADGM Courts jurisdiction guidance",
}


def cite_rules(keys: List[str]) -> List[str]:
    return [CITATION_REGISTRY.get(k, k) for k in keys]
