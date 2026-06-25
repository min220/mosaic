import anthropic
import json

client = anthropic.Anthropic()

def run_mosaic_inference(all_findings):
    entities = []
    for finding in all_findings:
        for f in finding["findings"]:
            entities.append({
                "entity": f["entity"],
                "category": f["category"],
                "source": finding["source"],
                "page": finding["page"],
                "reasoning": f["reasoning"]
            })

    if not entities:
        return {"mosaic_risk": "LOW", "inferences": [], "summary": "No sensitive entities found across documents."}

    prompt = f"""You are a privacy analyst specializing in the mosaic effect — the phenomenon where combining individually innocuous pieces of information across multiple documents reveals something sensitive that no single document discloses alone.

Here are sensitive entities found across a set of documents:

{json.dumps(entities, indent=2)}

Your job:
1. Identify combinations of entities that together reveal something more sensitive than any single entity alone
2. Explain what can be inferred from the combination
3. Rate the overall mosaic risk

Respond in JSON with this exact structure:
{{
  "mosaic_risk": "LOW, MEDIUM, or HIGH",
  "inferences": [
    {{
      "entities_combined": ["entity1", "entity2"],
      "sources_involved": ["source1", "source2"],
      "inferred_disclosure": "what can be inferred by combining these",
      "severity": "LOW, MEDIUM, or HIGH"
    }}
  ],
  "summary": "one paragraph summary of the overall mosaic risk"
}}

Respond with JSON only. No preamble, no markdown."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    if not raw:
        return {"mosaic_risk": "LOW", "inferences": [], "summary": "No response from model."}
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


if __name__ == "__main__":
    from ingestion.parser import parse_pdf
    from detection.detector import detect_sensitive

    chunks = parse_pdf("a.pdf")
    all_findings = [detect_sensitive(chunk) for chunk in chunks]

    print("\n--- MOSAIC INFERENCE ---\n")
    result = run_mosaic_inference(all_findings)
    print(json.dumps(result, indent=2))