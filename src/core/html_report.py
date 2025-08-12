from typing import Dict, Any, List

def build_html_report(report: Dict[str, Any]) -> str:
    issues: List[Dict[str, Any]] = report.get("issues_found", [])
    missing = report.get("missing_documents", [])
    css = """
    body{font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin:24px;}
    h1{margin:0 0 8px 0}
    h2{margin-top:24px}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}
    .card{border:1px solid #ddd;border-radius:8px;padding:12px;background:#fff}
    .muted{color:#666;font-size:12px}
    table{width:100%;border-collapse:collapse}
    th,td{padding:8px;border-top:1px solid #eee;text-align:left;vertical-align:top}
    .badge{display:inline-block;border-radius:6px;padding:2px 6px;color:#fff;font-size:12px}
    .high{background:#dc2626}.medium{background:#d97706}.low{background:#6b7280}
    """
    def badge(sev: str) -> str:
        cls = (sev or "").lower()
        return f'<span class="badge {cls}">{sev}</span>'

    parts = []
    parts.append(f"<html><head><meta charset='utf-8'><title>Detailed Analysis</title><style>{css}</style></head><body>")
    parts.append("<h1>ADGM Corporate Agent - Detailed Analysis</h1>")
    parts.append(f"<div class='muted'>Process: {report.get('process','Unknown')}</div>")
    # Summary
    parts.append("<h2>Summary</h2>")
    parts.append("<div class='grid'>")
    metrics = [
        ("Documents Uploaded", report.get('documents_uploaded', 0)),
        ("Required Documents", report.get('required_documents', 0)),
        ("Issues", len(issues)),
        ("Missing", len(missing)),
        ("Compliance", report.get('compliance_score', '—')),
    ]
    for label, value in metrics:
        parts.append(f"<div class='card'><div style='font-size:24px;font-weight:600'>{value}</div><div class='muted'>{label}</div></div>")
    parts.append("</div>")
    if missing:
        parts.append(f"<p><b>Missing:</b> {', '.join(missing)}</p>")
    else:
        parts.append("<p><b>All required documents present</b></p>")

    # Findings
    parts.append("<h2>Findings</h2>")
    if not issues:
        parts.append("<p>No issues detected.</p>")
    else:
        parts.append("<table><thead><tr><th>Document</th><th>Severity</th><th>Issue</th><th>Suggestion</th><th>Sources</th></tr></thead><tbody>")
        for it in issues:
            cits = "; ".join(it.get('citations') or [])
            parts.append(
                f"<tr><td>{it.get('document','')}</td><td>{badge(it.get('severity',''))}</td>"
                f"<td>{it.get('issue','')}</td><td>{(it.get('suggestion','') or '').replace('\n',' ')}</td>"
                f"<td>{cits}</td></tr>"
            )
        parts.append("</tbody></table>")

    parts.append("</body></html>")
    return "".join(parts)
