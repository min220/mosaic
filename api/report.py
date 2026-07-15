import json
from datetime import datetime

def generate_report(all_findings, mosaic_result, output_path="report.md"):
    lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines.append(f"# mosaic audit report")
    lines.append(f"generated: {now}\n")

    lines.append(f"## overall risk")
    lines.append(f"**{mosaic_result['mosaic_risk']}**\n")
    lines.append(f"{mosaic_result['summary']}\n")

    lines.append(f"## per-document findings")
    for finding in all_findings:
        if not finding["findings"]:
            continue
        lines.append(f"\n### {finding['source']} — page {finding['page']}")
        lines.append(f"risk: {finding['overall_risk']}")
        for f in finding["findings"]:
            lines.append(f"\n- **{f['entity']}** ({f['category']}, confidence: {f['confidence']})")
            lines.append(f"  {f['reasoning']}")

    lines.append(f"\n## mosaic inferences")
    if not mosaic_result["inferences"]:
        lines.append("no cross-document inferences found.")
    for inf in mosaic_result["inferences"]:
        lines.append(f"\n### {inf['severity']} severity")
        lines.append(f"**entities:** {', '.join(inf['entities_combined'])}")
        lines.append(f"**sources:** {', '.join(inf['sources_involved'])}")
        lines.append(f"**disclosure:** {inf['inferred_disclosure']}")

    report = "\n".join(lines)
    with open(output_path, "w") as f:
        f.write(report)
    print(f"report written to {output_path}")
    return report


if __name__ == "__main__":
    from ingestion.parser import parse_pdf
    from detection.detector import detect_sensitive
    from inference.mosaic import run_mosaic_inference

    chunks = parse_pdf("a.pdf")
    all_findings = [detect_sensitive(chunk) for chunk in chunks]
    mosaic_result = run_mosaic_inference(all_findings)

    generate_report(all_findings, mosaic_result, "report.md")