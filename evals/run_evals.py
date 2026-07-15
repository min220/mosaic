import json
import sys
sys.path.insert(0, '.')

from detection.detector import detect_sensitive
from inference.mosaic import run_mosaic_inference
from evals.synthetic import SYNTHETIC_CASES

def run_evals():
    results = []
    tp = fp = tn = fn = 0

    for case in SYNTHETIC_CASES:
        print(f"\nrunning {case['id']}: {case['description']}")

        all_chunks = []
        for doc in case["documents"]:
            all_chunks.append({
                "source": doc["id"],
                "page": 0,
                "chunk_index": 0,
                "text": doc["text"]
            })

        all_findings = [detect_sensitive(chunk) for chunk in all_chunks]
        mosaic_result = run_mosaic_inference(all_findings)

        predicted_mosaic = mosaic_result["mosaic_risk"] != "LOW"
        expected_mosaic = case["expected_mosaic"]
        predicted_severity = mosaic_result["mosaic_risk"]
        expected_severity = case["expected_severity"]

        if predicted_mosaic and expected_mosaic:
            outcome = "TP"
            tp += 1
        elif not predicted_mosaic and not expected_mosaic:
            outcome = "TN"
            tn += 1
        elif predicted_mosaic and not expected_mosaic:
            outcome = "FP"
            fp += 1
        else:
            outcome = "FN"
            fn += 1

        result = {
            "id": case["id"],
            "outcome": outcome,
            "expected_mosaic": expected_mosaic,
            "predicted_mosaic": predicted_mosaic,
            "expected_severity": expected_severity,
            "predicted_severity": predicted_severity,
            "inferences_found": len(mosaic_result["inferences"])
        }
        results.append(result)
        print(f"  outcome: {outcome} | expected: {expected_severity} | predicted: {predicted_severity}")

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    print(f"\n--- eval results ---")
    print(f"TP: {tp} | FP: {fp} | TN: {tn} | FN: {fn}")
    print(f"precision: {precision:.2f}")
    print(f"recall:    {recall:.2f}")
    print(f"f1:        {f1:.2f}")

    with open("evals/results.json", "w") as f:
        json.dump({"summary": {"precision": precision, "recall": recall, "f1": f1, "tp": tp, "fp": fp, "tn": tn, "fn": fn}, "cases": results}, f, indent=2)

    print(f"\nresults written to evals/results.json")

if __name__ == "__main__":
    run_evals()