# mosaic audit report
generated: 2026-07-15 15:15

## overall risk
**MEDIUM**

While each piece of information — a name, an institution, and a graduation year — may appear benign in isolation, their combination in a single document creates a moderately high mosaic risk. Together, they form a sufficiently precise academic profile to uniquely identify Nichapha (Min) Rungsinaporn as a current Barnard College student graduating in 2026, effectively disclosing her physical location, approximate age, enrollment status, and providing multiple vectors for further research or unwanted contact. The inclusion of a preferred nickname alongside a full legal name amplifies this risk by bridging formal records with informal online personas. This combination warrants redaction or access controls, particularly if the document is intended for broad distribution.

## per-document findings

### a.pdf — page 3
risk: MEDIUM

- **Nichapha (Min) Rungsinaporn** (PII, confidence: 0.98)
  Full legal name of an individual, which is directly identifiable personal information.

- **Barnard College** (ORGANIZATION, confidence: 0.85)
  Combined with the individual's name and graduation year, this reveals the person's educational institution, contributing to a profile that could identify and locate the individual.

- **2026** (PII, confidence: 0.8)
  Graduation year combined with the individual's name and institution narrows identification and reveals personal academic timeline information.

## mosaic inferences

### MEDIUM severity
**entities:** Nichapha (Min) Rungsinaporn, Barnard College
**sources:** a.pdf
**disclosure:** Combining the full legal name with the specific educational institution allows anyone to search institutional directories, alumni records, or LinkedIn to locate and identify this specific individual, narrowing the population to a single person enrolled at Barnard College.

### LOW severity
**entities:** Nichapha (Min) Rungsinaporn, 2026
**sources:** a.pdf
**disclosure:** The full name combined with a graduation year reveals the individual's approximate academic stage (likely a current undergraduate student), allowing inference of their approximate age range (likely 20-22 years old) and current enrollment status.

### HIGH severity
**entities:** Nichapha (Min) Rungsinaporn, Barnard College, 2026
**sources:** a.pdf
**disclosure:** The combination of full legal name, specific institution, and graduation year creates a precise academic profile that enables targeted identification of this individual across public directories, alumni databases, social media, and institutional records. It discloses their physical location (New York City, Barnard campus), approximate age, academic timeline, and provides enough data to initiate contact, surveillance, or social engineering. The nickname 'Min' further aids in locating informal social media profiles.