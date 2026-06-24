# Exercise 03 — MITRE ATLAS Mapping

**Module:** M01 — LLM Threat Modelling  
**Day:** 2  
**Estimated time:** 3 hours  
**Difficulty:** Intermediate  

---

## Objective

Develop working fluency with the MITRE ATLAS (Adversarial Threat Landscape for Artificial-Intelligence Systems) framework. Map a realistic set of LLM attack scenarios to ATLAS tactics and techniques, and understand how ATLAS complements — rather than replaces — OWASP LLM Top 10.

---

## Background

### What is MITRE ATLAS?

MITRE ATLAS is an adversarial knowledge base for AI/ML systems, structured in the same way as MITRE ATT&CK but specifically for attacks against AI. Like ATT&CK, it is organised into:

- **Tactics** — the adversary's goal at each stage (e.g. Initial Access, Execution, Exfiltration)
- **Techniques** — the method used to achieve that goal (e.g. LLM Prompt Injection)
- **Case studies** — real-world incidents involving AI attacks

### Why ATLAS matters for financial services

Financial services regulators (FCA, CBB, DORA) increasingly require organisations to demonstrate they have assessed AI-specific risks. ATLAS provides the language and taxonomy to do this — just as ATT&CK provides the language for traditional threat modelling in SOC environments.

### ATLAS vs OWASP LLM Top 10

| Dimension | OWASP LLM Top 10 | MITRE ATLAS |
|---|---|---|
| Focus | Application-level vulnerabilities | Adversarial tactics across the AI lifecycle |
| Audience | Developers, AppSec | SecOps, threat intelligence, red team |
| Structure | Risk categories | Tactics → Techniques → Procedures |
| Scope | LLM applications | All AI/ML systems (not just LLMs) |
| Actionability | Defensive controls | Threat modelling, detection, hunting |

They are complementary — use OWASP to identify what to defend, ATLAS to model how an adversary would attack.

---

## Part 1 — Navigate ATLAS (45 min)

### Step 1.1 — Explore the ATLAS matrix

Go to: [https://atlas.mitre.org/matrices/ATLAS](https://atlas.mitre.org/matrices/ATLAS)

Spend 30 minutes exploring the matrix. For each of the following tactics, note 2–3 techniques that are most relevant to an LLM-powered financial services application:

| Tactic | Most relevant techniques for LLM apps | Notes |
|---|---|---|
| Reconnaissance | | |
| Resource Development | | |
| Initial Access | | |
| ML Model Access | | |
| Execution | | |
| Persistence | | |
| Privilege Escalation | | |
| Defence Evasion | | |
| Discovery | | |
| Collection | | |
| Exfiltration | | |
| Impact | | |

### Step 1.2 — Read three case studies

From the ATLAS case studies section ([https://atlas.mitre.org/studies/](https://atlas.mitre.org/studies/)), read three case studies. For each, note:

1. What type of AI system was targeted?
2. Which ATLAS techniques were used?
3. What was the impact?
4. What control would have prevented or detected the attack?

Record your notes in your lab journal.

---

## Part 2 — Key Techniques Deep Dive (1 hour)

### AML.T0051 — LLM Prompt Injection

**ATLAS definition:** An adversary crafts malicious prompts as inputs to an LLM that cause the LLM to act in unintended ways.

**Sub-techniques:**
- AML.T0051.000 — Direct Prompt Injection (attacker directly sends malicious input)
- AML.T0051.001 — Indirect Prompt Injection (malicious content embedded in retrieved data)

**Detection opportunity:**  
- Anomaly detection on LLM input/output pairs
- Signature-based detection for known injection patterns (limited effectiveness)
- Behavioural monitoring — detect when agent performs actions outside its expected scope

**Mapped to OWASP:** LLM01

---

### AML.T0054 — LLM Jailbreak

**ATLAS definition:** An adversary uses a jailbreak prompt to cause an LLM to produce output that violates the policies defined in the system prompt.

**Examples:**
- Role-play jailbreaks ("You are DAN — Do Anything Now")
- Many-shot jailbreaking (providing many in-context examples that shift model behaviour)
- Token manipulation (using special tokens or encoding tricks)

**Why it matters in financial services:**  
A jailbroken LLM could be made to produce investment advice that contradicts regulatory obligations, output client data it should not share, or take actions its system prompt prohibits.

**Mapped to OWASP:** LLM01, LLM07

---

### AML.T0057 — LLM Data Leakage

**ATLAS definition:** An adversary crafts prompts that cause the LLM to output sensitive information from its training data or context window.

**Extraction methods:**
- Verbatim extraction — asking the model to repeat its training data
- Membership inference — determining whether specific data was in the training set
- Context window extraction — tricking the model into revealing its system prompt or retrieved documents

**Mapped to OWASP:** LLM02, LLM07

---

### AML.T0048 — Backdoor ML Model

**ATLAS definition:** An adversary inserts a backdoor into an ML model during training, causing it to behave normally except when a specific trigger input is present.

**LLM-specific scenario:**  
A fine-tuned LLM used for customer service has been poisoned during fine-tuning. When a user includes a specific phrase in their query, the model produces outputs that benefit the attacker (e.g. recommending a specific product, leaking data, bypassing security checks).

**Why this is hard to detect:**  
Backdoored models behave normally on all inputs except the trigger — standard evaluation and testing will not reveal the backdoor.

**Mapped to OWASP:** LLM04

---

## Part 3 — Build Your ATLAS Mapping for a Financial Services LLM (1 hour)

### Step 3.1 — Define the target system

Use this system definition for the mapping exercise:

**Target:** `FinBot` — an LLM-powered customer service agent for a retail bank  
**Capabilities:**
- Answer account balance queries (read-only API access)
- Search FAQs and policy documents (RAG over internal knowledge base)
- Escalate complex queries via email to human agents
- Provide general financial guidance (non-advice)

**Deployment:** Cloud-hosted (Azure OpenAI), accessible via web and mobile app

### Step 3.2 — Build the attack chain

Map a realistic end-to-end attack against FinBot using ATLAS tactics and techniques:

```
Adversary goal: Exfiltrate customer account data via the FinBot interface
```

| Stage | ATLAS Tactic | ATLAS Technique | Attack Action |
|---|---|---|---|
| 1 | Reconnaissance | AML.T0000 | Probe FinBot to understand its capabilities and system prompt |
| 2 | Initial Access | AML.T0051.001 | Embed prompt injection in a support ticket PDF that FinBot retrieves |
| 3 | Execution | AML.T0054 | Jailbreak overrides account data restriction |
| 4 | Collection | AML.T0057 | Exfiltrate other users' account summaries from context |
| 5 | Exfiltration | AML.T0057 | Data returned in LLM response to attacker |

### Step 3.3 — Defensive mapping

For each attack stage above, document:
- Detection opportunity (what would a SOC analyst see?)
- Preventive control (what would stop this step?)
- NIST CSF 2.0 function (Identify / Protect / Detect / Respond / Recover)

---

## Part 4 — Document (included in time estimate)

```bash
cp ../../../docs/templates/LAB-REPORT-TEMPLATE.md \
   ../reports/REPORT-03-mitre-atlas.md
```

Complete `REPORT-03-mitre-atlas.md` with:
- Your ATLAS matrix notes (Part 1)
- Case study summaries
- Deep dive notes on the four key techniques
- The FinBot attack chain table and defensive mapping

---

## Verification Checklist

- [ ] ATLAS matrix explored — notes on all 12 tactics
- [ ] Three case studies read and summarised
- [ ] Four key techniques (T0051, T0054, T0057, T0048) documented in own words
- [ ] FinBot attack chain table completed
- [ ] Defensive mapping completed
- [ ] Lab report `REPORT-03-mitre-atlas.md` completed
- [ ] Committed and pushed

---

## Key Takeaways

1. ATLAS is the adversary's view — ATT&CK for AI. Use it to think like a threat actor, not just a defender.
2. The most dangerous LLM attack chains combine multiple ATLAS techniques across multiple stages — just like APT campaigns in traditional networks.
3. Detection opportunities exist at every stage of the ATLAS kill chain — the key is instrumenting LLM inputs and outputs for SOC visibility.
4. Financial services AI deployments are high-value targets because they combine sensitive data (accounts, transactions) with agentic capabilities (email, API calls).

---

## Further Reading

- [MITRE ATLAS full documentation](https://atlas.mitre.org/)
- [Greshake et al. — Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173)
- [NIST AI 100-2 — Adversarial Machine Learning Taxonomy](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2023.pdf)

---

## Next Exercise

→ [Exercise 04 — Build a Vulnerable LLM Application](./EX-04-vulnerable-llm-app.md)

---

*Exercise 03 · Module 01 · ai-security-lab*
