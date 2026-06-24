# Lab Report — MITRE ATLAS Mapping · Exercise 03

**Author:** Narendra Karki  
**Date:** 2026-06-09  
**Module:** M01 — LLM Threat Modelling  
**Exercise:** EX-03 — MITRE ATLAS Mapping  
**Duration:** 1 hour  
**Difficulty:** Intermediate  

---

## 1. Objective

To develop working fluency with the MITRE ATLAS framework by mapping a realistic LLM attack scenario against a financial services chatbot (FinBot) to ATLAS tactics and techniques, and to understand how ATLAS complements the OWASP LLM Top 10 for threat modelling purposes.

---

## 2. Background & Theory

MITRE ATLAS (Adversarial Threat Landscape for Artificial-Intelligence Systems) is an adversarial knowledge base for AI/ML systems, structured in the same way as MITRE ATT&CK but specifically for attacks against AI. It organises adversarial behaviour into Tactics (the attacker's goal), Techniques (the method used), and Case Studies (real-world incidents).

Unlike the OWASP LLM Top 10 which focuses on application-level vulnerabilities and defensive controls, ATLAS models the full adversary lifecycle — from reconnaissance through to impact. This makes it the preferred framework for threat modelling, SOC detection engineering, and adversary simulation in AI security contexts.

For financial services organisations, ATLAS is increasingly relevant as regulators (FCA, CBB, DORA) require demonstration of AI-specific risk assessments. ATLAS provides the language and taxonomy to document these assessments in a way that maps directly to existing ATT&CK-based SOC processes — making it immediately applicable to organisations already using MITRE ATT&CK for threat intelligence and detection engineering.

The key insight from this exercise is that LLM attack chains follow the same kill chain structure as traditional APT campaigns — Reconnaissance, Initial Access, Execution, Collection, Exfiltration — but the attack surface has moved from the network layer to the natural language layer, making traditional perimeter controls ineffective.

---

## 3. Environment

| Item | Detail |
|---|---|
| OS | macOS / Docker container |
| Python version | 3.11.x |
| Key tools | e.g. Garak 0.9, ART 1.17 |
| Target system | e.g. Local Flask LLM app |
| Network | Isolated local / Docker bridge |

### Setup Commands

```bash
# Record exactly what you ran to set up the environment
pip install <tool>
docker run ...
```

---

## 4. Exercise Steps

### Step 1 — [Step Title]

**What I did:**

```bash
# Exact commands run
```

**What happened:**

> Describe the output, behaviour, or result in plain language.

**Screenshot/Evidence:** `../evidence/ex-N-step-1.png`

---

### Step 2 — [Step Title]

**What I did:**

```bash
# Exact commands run
```

**What happened:**

> Describe the output, behaviour, or result.

**Screenshot/Evidence:** `../evidence/ex-N-step-2.png`

---

*(repeat for each step)*

---

## 5. Findings

| # | Finding | Severity | OWASP / ATLAS Reference | Notes |
|---|---|---|---|---|
| F-01 | [e.g. Model accepted direct prompt injection] | Critical | LLM01 | |
| F-02 | | | | |

---

## 6. Attack/Defence Mapping

| Attack Vector | Demonstrated? | Detection Method | Mitigation |
|---|---|---|---|
| Prompt injection | ✅ Yes | Input validation bypass | Input sanitisation, guardrails |
| Data poisoning | | | |
| Model evasion | | | |

---

## 7. Key Learnings

> What did you learn that you did not know before? What surprised you? What would you do differently next time? Write this as a personal learning log — honest and specific.

1. 
2. 
3. 

---

## 8. Relation to Real-World Scenarios

> How does this exercise map to a real security scenario in a financial services or enterprise environment? Be specific — name the asset class, threat actor type, and likely impact.

---

## 9. Recommendations

> If this were a real engagement, what would you recommend to the client/organisation?

| Priority | Recommendation | Framework Reference |
|---|---|---|
| P1 — Critical | | |
| P2 — High | | |
| P3 — Medium | | |

---

## 10. References

- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [Tool documentation links]
- [Any papers or articles read]

---

## 11. Next Steps

> What does this exercise lead into? What should be built or tested next?

---

*Report generated: YYYY-MM-DD · Lab: ai-security-lab · Module: M0X*

## FinBot Attack Chain — MITRE ATLAS Mapping

Target: FinBot — LLM-powered customer service agent for SecureBank
Adversary goal: Exfiltrate customer account data via the FinBot interface

| Stage | ATLAS Tactic | ATLAS Technique | Attack Action | Detection Opportunity |
|---|---|---|---|---|
| 1 | Reconnaissance | AML.T0000 | Probe FinBot with test queries to understand capabilities, tools, and system prompt structure | Unusual query patterns — many short probing queries in quick succession |
| 2 | Resource Development | AML.T0051 | Craft indirect prompt injection payload — embed malicious instruction in a support ticket PDF | None — happens entirely offline |
| 3 | Initial Access | AML.T0051.001 | Submit poisoned PDF as support request — RAG pipeline retrieves and processes the embedded instruction | Anomalous retrieved document triggering unusual tool calls |
| 4 | Execution | AML.T0054 | Jailbreak overrides account data restriction in system prompt | LLM output deviates from expected response pattern |
| 5 | Collection | AML.T0057 | Model returns other customers' account summaries from context window | Output contains PII patterns — account numbers, sort codes |
| 6 | Exfiltration | AML.T0057 | Sensitive data returned directly in LLM response to attacker | PII detected in outbound response — output filtering would catch this |

## Defensive Mapping

| Stage | Preventive Control | Detective Control | NIST CSF 2.0 Function |
|---|---|---|---|
| 1 | Rate limiting on queries | Anomaly detection on query patterns | Detect |
| 2 | N/A — offline stage | N/A | N/A |
| 3 | Input validation on uploaded documents | RAG retrieval monitoring | Protect / Detect |
| 4 | Prompt injection classifier (Llama Guard) | Behavioural monitoring on tool calls | Protect / Detect |
| 5 | Context window isolation, session hygiene | PII scanning on LLM outputs | Protect / Detect |
| 6 | Output filtering for PII patterns | SIEM alert on PII in outbound responses | Detect / Respond |

## Root Cause Analysis

The attack succeeded not because of one vulnerability but because of 
three compounding failures:

1. LLM01 — No prompt injection detection on uploaded documents
2. LLM06 — Excessive agency — account data accessible without HiTL approval
3. LLM05 — Raw output returned without PII filtering

Breaking any one of these three chains stops the attack.
This is the key insight: defence-in-depth applies to LLM systems 
exactly as it does to traditional network architecture.

## Personal Notes

1. Which single control would have the highest impact if you 
could only implement one?
> Output PII filtering at Stage 6 — because it breaks the 
> attack at the last mile regardless of how the attacker got 
> there. Even if prompt injection succeeds and account data 
> is collected, filtered output means nothing leaves. However 
> input validation on uploaded documents (Stage 3) is a close 
> second — stopping indirect injection at the RAG ingestion 
> layer prevents the attack chain from starting at all.

2. At which stage would your existing SIEM (Sentinel/Splunk) 
have the best detection opportunity?
> Stage 5 and 6 — PII patterns in LLM outputs are the most 
> reliable SIEM detection point. Account numbers, sort codes, 
> and customer names in outbound responses can be detected 
> with regex-based alert rules similar to existing DLP 
> signatures. RAG retrieval monitoring at Stage 3 is also 
> viable but requires custom LLM-aware log ingestion that 
> most SIEM deployments don't have out of the box.

3. How does this attack chain compare to a traditional APT 
kill chain you've seen in your SOC career?
> The structure is identical to a classic APT kill chain — 
> Reconnaissance, Initial Access, Execution, Collection, 
> Exfiltration. What is fundamentally different is that IPS 
> and firewall rules that would catch anomalous traffic in a 
> traditional attack are completely blind here — all traffic 
> is legitimate HTTPS to a valid API endpoint. The attack 
> surface has moved from the network layer to the natural 
> language layer, and our existing SOC detection stack was 
> not built for that. This is the core gap that AI-augmented 
> SOC tooling needs to address.




