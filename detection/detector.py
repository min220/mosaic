import anthropic
import json

client = anthropic.Anthropic()

def detect_sensitive(chunk):
    prompt = f"""You are a privacy auditor analyzing a document chunk for sensitive information.

Analyze the following text and identify any sensitive information present.

Text:
{chunk['text']}

Respond in JSON with this exact structure:
{{
  "findings": [
    {{
      "entity": "the sensitive item found",
      "category": "one of: PII, FINANCIAL, LOCATION, ORGANIZATION, CREDENTIAL, OTHER",
      "confidence": 0.0 to 1.0,
      "reasoning": "why this is sensitive"
    }}
  ],
  "overall_risk": "LOW, MEDIUM, or HIGH",
  "summary": "one sentence summary of what was found"
}}

If nothing sensitive is found, return an empty findings array with overall_risk LOW.
Respond with JSON only. No preamble, no markdown."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    result = json.loads(message.content[0].text)
    result["chunk_index"] = chunk["chunk_index"]
    result["page"] = chunk["page"]
    result["source"] = chunk["source"]
    return result


if __name__ == "__main__":
    from ingestion.parser import parse_pdf
    chunks = parse_pdf("a.pdf")
    for chunk in chunks:
        result = detect_sensitive(chunk)
        print(json.dumps(result, indent=2))