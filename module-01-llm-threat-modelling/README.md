# Module 01 — LLM Threat Modelling

**Duration:** Days 1–4
**Status:** ✅ Complete

---

## Scope

This module produces a formal threat model for an LLM-based application
(VulnFinBot — a simulated financial services chatbot), then validates
that model against real adversarial behaviour. These are two distinct
activities and are presented separately below.

---

## Part A — Threat Model (the primary deliverable)

The actual threat-modelling output of this module:

| Artifact | What it contains | Location |
|---|---|---|
| Architecture / Data Flow Diagram | System components, data flows, trust boundaries | `reports/REPORT-06-threat-model-final.md` |
| Asset inventory | Customer PII, credentials, system prompt, tool access | `reports/REPORT-06-threat-model-final.md` |
| Trust boundary analysis | 5 components: User↔API, System Prompt, Tool Dispatcher, Response↔User, Ollama Inference | `reports/REPORT-05-stride.md` |
| STRIDE threat enumeration | 15 threats across all 6 STRIDE categories | `reports/REPORT-05-stride.md` |
| Risk ratings | 8 Critical · 6 High · 1 Medium | `reports/REPORT-05-stride.md` |
| OWASP LLM Top 10 mapping | All 10 categories mapped to identified threats | `reports/REPORT-02-owasp-llm-top10.md` |
| MITRE ATLAS mapping | AML.T0051, AML.T0056, AML.T0057 mapped to threats | `reports/REPORT-03-mitre-atlas.md` |
| Mitigations / security requirements | Prioritised remediation list (P1–P3) | `reports/REPORT-06-threat-model-final.md` |

### Methodology

```
System Design (VulnFinBot architecture)
        │
        ▼
Assets (customer PII, system prompt, tool access, credentials)
        │
        ▼
Trust Boundaries (5 components identified)
        │
        ▼
Threat Enumeration (STRIDE × 5 components = 15 threats)
        │
        ▼
Attack Vectors (prompt injection, excessive agency, data
                disclosure, tampering, DoS — mapped per threat)
        │
        ▼
Mitigations (P1/P2/P3 prioritised remediation list)
```

Prompt injection is **one of several** attack vectors considered, not
the focus of the model. The STRIDE pass covers spoofing, tampering,
repudiation, information disclosure, denial of service, and elevation
of privilege independently of any single technique.

### Top risk findings

1. No technical boundary between system prompt and user input — root
   cause for 6 of the 15 threats (T-02, T-06, T-08 and related)
2. Customer PII embedded directly in system prompt context (T-09)
3. No output filtering before returning LLM responses to the user (T-13)
4. Tool dispatcher has no authorisation gate on high-impact functions
   such as `send_email()` (T-11)

Full risk register, trust boundary diagram, and mitigation roadmap:
[`reports/REPORT-06-threat-model-final.md`](./reports/REPORT-06-threat-model-final.md)

---

## Part B — Adversarial Validation (testing the model's assumptions)

Once the threat model identified theoretical attack vectors, those
vectors were tested against a live instance of VulnFinBot to confirm
(or refute) that the threats were practically exploitable — not just
theoretically possible.

This is **validation of the threat model**, not the threat model
itself. It answers: *"Are the risks we identified actually exploitable,
or only theoretical?"*

| Threat (from Part A) | Validated via | Result | Evidence |
|---|---|---|---|
| T-09 — System prompt disclosure | Live extraction attempt | ✅ Confirmed exploitable | `evidence/ex-04-attack1-system-prompt-extraction.png` |
| T-02 — Prompt injection / tampering | Direct injection attempt | ✅ Confirmed exploitable | `evidence/ex-04-attack2-prompt-injection.png` |
| T-04 — Customer data disclosure | Direct data request | ✅ Confirmed exploitable | `evidence/ex-04-attack3-data-extraction.png` |
| T-11 — Excessive agency / tool misuse | Unauthorised tool invocation attempt | ✅ Confirmed exploitable | `evidence/ex-04-attack4-excessive-agency.png` |

Detailed write-up of each validation attempt, including exact prompts
used and observed responses: [`reports/REPORT-04-vulnerable-app.md`](./reports/REPORT-04-vulnerable-app.md)

Separately, a public LLM prompt-injection benchmark (Gandalf, by Lakera)
was used as an additional exploration of injection resistance —
unrelated to VulnFinBot's specific threat model:
[`reports/REPORT-05-gandalf.md`](./reports/REPORT-05-gandalf.md)

---

## Why both parts matter

A threat model that is never validated against real behaviour is a
set of untested assumptions. Adversarial validation without a
preceding threat model is unstructured poking — it finds *some* bugs
but provides no systematic coverage or risk prioritisation.

This module deliberately does both, in order: model first, validate
second. The STRIDE artifacts in Part A define the *complete* threat
surface across all six categories; Part B confirms that 4 of the
identified Critical/High threats are practically — not just
theoretically — exploitable.

---

## Folder structure

```
module-01-llm-threat-modelling/
├── reports/
│   ├── REPORT-02-owasp-llm-top10.md      ← framework mapping
│   ├── REPORT-03-mitre-atlas.md          ← framework mapping
│   ├── REPORT-04-vulnerable-app.md       ← Part B: validation write-up
│   ├── REPORT-05-stride.md               ← Part A: STRIDE threat model
│   ├── REPORT-05-gandalf.md              ← supplementary injection testing
│   └── REPORT-06-threat-model-final.md   ← Part A: full threat model document
├── exercises/                            ← exercise-by-exercise working notes
├── evidence/                             ← Part B: validation screenshots
└── tools/                                ← VulnFinBot (test target)
```

---

## Exercises

| # | Exercise | Part | Status |
|---|---|---|---|
| EX-01 | Environment setup | — | ✅ Complete |
| EX-02 | OWASP LLM Top 10 deep dive | A | ✅ Complete |
| EX-03 | MITRE ATLAS attack chain mapping | A | ✅ Complete |
| EX-04 | VulnFinBot live attacks | B | ✅ Complete |
| EX-05 | STRIDE threat model | A | ✅ Complete |
| EX-05 (supplementary) | Gandalf prompt injection benchmark | B | ✅ Complete |
| EX-06 | Final threat model document | A | ✅ Complete |
| EX-07 | Portfolio write-up | — | ✅ Complete |
