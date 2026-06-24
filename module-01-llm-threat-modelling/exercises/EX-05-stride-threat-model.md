# Exercise 05 — STRIDE Threat Model

**Module:** M01 — LLM Threat Modelling  
**Day:** 4  
**Status:** ✅ Complete  

---

## Objective

Apply the STRIDE threat modelling methodology to VulnFinBot — 
identifying threats across all six STRIDE categories for each 
architectural component.

## Methodology

STRIDE = Spoofing, Tampering, Repudiation, Information Disclosure, 
Denial of Service, Elevation of Privilege

Applied systematically across 5 components:
- User → Flask API
- System Prompt
- Tool Dispatcher
- Response → User
- Ollama Inference

## Results Summary

**15 threats identified · 8 Critical · 6 High · 1 Medium**

| Threat ID | Component | STRIDE | Severity |
|---|---|---|---|
| T-01 | User → Flask API | Spoofing | Critical |
| T-02 | User → Flask API | Tampering | Critical |
| T-03 | User → Flask API | Repudiation | High |
| T-04 | User → Flask API | Info Disclosure | Critical |
| T-05 | User → Flask API | DoS | High |
| T-06 | User → Flask API | EoP | Critical |
| T-07 | System Prompt | Spoofing | High |
| T-08 | System Prompt | Tampering | Critical |
| T-09 | System Prompt | Info Disclosure | Critical |
| T-10 | Tool Dispatcher | Tampering | Critical |
| T-11 | Tool Dispatcher | EoP | Critical |
| T-12 | Tool Dispatcher | DoS | High |
| T-13 | Response → User | Info Disclosure | Critical |
| T-14 | Response → User | Tampering | High |
| T-15 | Ollama Inference | Tampering | High |

## Risk Posture

Overall: **CRITICAL** — VulnFinBot not suitable for production 
deployment in current state.

## Top Priority Remediations

1. Remove all customer data from system prompt (resolves T-09, 
   reduces T-02/T-06/T-08)
2. Implement output PII filtering (resolves T-13, reduces T-04)
3. Remove email tool — apply tool minimisation (resolves T-11, 
   reduces T-10/T-06)

## Framework Mapping

- OWASP LLM Top 10 — all 10 categories referenced
- MITRE ATLAS — AML.T0051, AML.T0056, AML.T0057
- Regulatory — EU AI Act Art.9/13/14, DORA Art.9, UK GDPR Art.25

## Evidence

- Full threat model: reports/REPORT-05-stride.md
- Professional document: reports/REPORT-06-threat-model-final.md
