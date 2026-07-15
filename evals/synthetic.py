# Synthetic test cases with known ground truth for mosaic detection eval

SYNTHETIC_CASES = [
    {
        "id": "case_001",
        "description": "Name + employer + salary across two documents",
        "documents": [
            {"id": "doc_a", "text": "John Martinez is a senior engineer at Stripe."},
            {"id": "doc_b", "text": "The engineering team at Stripe has a median salary of $220,000. John recently joined the team."},
        ],
        "expected_entities": ["John Martinez", "Stripe"],
        "expected_mosaic": True,
        "expected_severity": "HIGH",
        "notes": "Name + employer + salary inference"
    },
    {
        "id": "case_002",
        "description": "Medical condition + name + location",
        "documents": [
            {"id": "doc_a", "text": "Patient Sarah Chen was diagnosed with Type 2 diabetes in Q3."},
            {"id": "doc_b", "text": "Sarah Chen lives at 42 Maple Street, Brooklyn and attends the community clinic on Tuesdays."},
        ],
        "expected_entities": ["Sarah Chen", "Type 2 diabetes", "42 Maple Street"],
        "expected_mosaic": True,
        "expected_severity": "HIGH",
        "notes": "Medical + identity + location combination"
    },
    {
        "id": "case_003",
        "description": "Clean documents — no leakage",
        "documents": [
            {"id": "doc_a", "text": "The quarterly revenue for the APAC region increased by 12% year over year."},
            {"id": "doc_b", "text": "Our product roadmap includes three new features scheduled for Q4 release."},
        ],
        "expected_entities": [],
        "expected_mosaic": False,
        "expected_severity": "LOW",
        "notes": "True negative — no sensitive entities"
    },
    {
        "id": "case_004",
        "description": "Immigration status + name + workplace",
        "documents": [
            {"id": "doc_a", "text": "Amir Hosseini is on an H-1B visa sponsored by his current employer."},
            {"id": "doc_b", "text": "Amir Hosseini works at Palantir Technologies in New York."},
        ],
        "expected_entities": ["Amir Hosseini", "H-1B", "Palantir Technologies"],
        "expected_mosaic": True,
        "expected_severity": "HIGH",
        "notes": "Immigration status + employer is high sensitivity combination"
    },
    {
        "id": "case_005",
        "description": "Single document with PII — no cross-doc inference",
        "documents": [
            {"id": "doc_a", "text": "Please send the report to Lisa Park at lisa.park@company.com."},
        ],
        "expected_entities": ["Lisa Park", "lisa.park@company.com"],
        "expected_mosaic": False,
        "expected_severity": "LOW",
        "notes": "Single doc PII — detection should fire but no mosaic inference"
    },
]