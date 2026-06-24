# Lab Report — LLM Alert Triage System · Exercise 01

**Author:** Narendra Karki · CAISP  
**Date:** 2026-06-15  
**Module:** M04 — AI-Augmented SOC  
**Exercise:** EX-01 — LLM Alert Triage with Human-in-the-Loop Controls  
**Duration:** 1 day (Day 8)  
**Difficulty:** Intermediate  

---

## 1. Objective

Build a working AI-augmented SOC alert triage pipeline that uses a local LLM (Llama3 via Ollama) to analyse Wazuh-format security alerts, map findings to MITRE ATT&CK and MITRE ATLAS, recommend immediate actions, and implement human-in-the-loop approval gates for HIGH and CRITICAL severity alerts. Demonstrate that LLM-specific attacks (prompt injection, API brute force) can be detected and triaged within the same SOC framework as traditional threats.

---

## 2. Background & Theory

### What is an AI-Augmented SOC?

A Security Operations Centre (SOC) receives hundreds or thousands of alerts daily from SIEM platforms like Wazuh. Human analysts cannot triage every alert at scale — alert fatigue is one of the most significant challenges in modern security operations. AI-augmented SOC addresses this by using LLMs to perform first-level triage: analysing alert context, mapping to threat frameworks, recommending actions, and flagging only the highest-priority alerts for human review.

The architecture follows a standard SOC workflow:

```
Security Events → SIEM (Wazuh) → LLM Triage Layer → Human Analyst
                                        ↓
                              Per-alert output:
                              - Severity classification
                              - MITRE ATT&CK mapping
                              - Immediate action
                              - Investigation steps
                              - HiTL flag (HIGH/CRITICAL)
```

### Why This Matters for Financial Services

Financial services SOCs face three compounding challenges:
1. High alert volume — thousands of events per day from trading systems, customer platforms, and regulatory monitoring
2. Strict regulatory requirements — FCA, DORA, and PCI DSS mandate rapid incident response
3. Emerging AI attack surface — LLM-powered customer service, fraud detection, and compliance tools create new attack vectors that traditional SOC playbooks do not cover

This exercise demonstrates that the same triage framework can handle both traditional threats (ransomware, web attacks) and AI-specific threats (prompt injection, LLM API abuse).

### Wazuh Deployment Attempt

Full Wazuh stack deployment (manager + indexer + dashboard) was attempted via Docker Compose. Encountered ARM64 compatibility issue — Wazuh 4.7.0 images are built for AMD64 (Intel) only. Apple Silicon M1 (aarch64) cannot run these images natively. AMD64 emulation via Rosetta caused OpenSearch security initialisation to fail after extended wait.

**Resolution:** Built LLM triage system using realistic Wazuh-format JSON alerts — same schema as production Wazuh output. The triage logic is SIEM-agnostic and would integrate with any Wazuh deployment via the Wazuh API (`GET /security/events`).

### Relevant Frameworks

- **MITRE ATT&CK:** T1078 (Valid Accounts), T1059 (Command and Scripting), T1486 (Data Encrypted for Impact)
- **MITRE ATLAS:** AML.T0051 (LLM Prompt Injection), AML.T0029 (Denial of ML Service)
- **NIST AI RMF:** GOVERN 1.5 (Human Oversight), MANAGE 2.2 (Risk Treatment)
- **OWASP LLM Top 10:** LLM01 (Prompt Injection), LLM10 (Unbounded Consumption)

---

## 3. Environment

| Item | Detail |
|---|---|
| OS | macOS — Apple Mac Mini M1 |
| Python | 3.14.x |
| LLM | Llama3 via Ollama (local Apple MPS inference) |
| SIEM | Wazuh 4.7.0 (attempted — ARM64 issue) |
| Alert format | Wazuh JSON schema (realistic simulation) |
| HiTL threshold | HIGH (level ≥ 10) and CRITICAL (level ≥ 13) |

### Setup Commands

```bash
lab4
pip install requests python-dotenv ollama langchain langchain-community
ollama serve &
ollama pull llama3
```

---

## 4. The Five Security Alerts

### Alert Scenario Overview

| ID | Scenario | Attacker | Target | Severity |
|---|---|---|---|---|
| ALT-001 | SSH login from external IP | 185.234.218.45 | prod-server-01 | HIGH |
| ALT-002 | Web command injection | 203.0.113.42 | web-server-01 | HIGH |
| ALT-003 | Ransomware mass encryption | Malware (svchost.exe) | finance-workstation-07 | CRITICAL |
| ALT-004 | LLM API brute force | 91.108.4.33 | ai-gateway-01 | MEDIUM |
| ALT-005 | Prompt injection on AI gateway | 178.62.14.55 | ai-gateway-01 | CRITICAL |

### Alert 1 — SSH External Login (ALT-001)

**Rule:** SSHD authentication success (Wazuh rule 5712, level 10)  
**Raw log:** `Accepted password for admin from 185.234.218.45 port 4523 ssh2`

**LLM Triage Output:**
```
SUMMARY: An administrative account was successfully authenticated on 
prod-server-01 using SSH from an unknown IP address (185.234.218.45).
SEVERITY: HIGH
FALSE_POSITIVE_LIKELIHOOD: LOW
MITRE_TACTIC: Initial Access
MITRE_TECHNIQUE: T1078 - Valid Accounts
FINANCIAL_SERVICES_IMPACT: Potential unauthorized access to sensitive 
financial systems and data.
IMMEDIATE_ACTION: Block the suspicious IP address at the network 
perimeter immediately.
ESCALATE_TO_HUMAN: YES
```

**Correct MITRE mapping:** T1078 (Valid Accounts) — LLM was correct.  
**HiTL decision:** YES — approved automated IP block.

---

### Alert 2 — Web Command Injection (ALT-002)

**Rule:** Web server 400 error (Wazuh rule 31101, level 12)  
**Raw log:** `GET /admin/config.php?cmd=cat+/etc/passwd HTTP/1.1 400`

**LLM Triage Output:**
```
SUMMARY: A potential web shell command was detected on a financial 
institution's web server, attempting to read sensitive system files.
SEVERITY: HIGH
FALSE_POSITIVE_LIKELIHOOD: LOW
MITRE_TACTIC: Initial Access
MITRE_TECHNIQUE: T1078 - Web Shell
FINANCIAL_SERVICES_IMPACT: Unauthorized access could compromise 
customer data or facilitate unauthorized transactions.
IMMEDIATE_ACTION: Block all incoming traffic to the web server 
and isolate it from the network.
ESCALATE_TO_HUMAN: YES
```

**Correct MITRE mapping:** T1059.007 (Command and Scripting Interpreter: JavaScript) or T1190 (Exploit Public-Facing Application). LLM used T1078 incorrectly here.  
**HiTL decision:** NO — did not approve immediate isolation. Investigation first — the 400 response indicates the attack failed. Isolation would cause unnecessary downtime.

---

### Alert 3 — Ransomware Mass Encryption (ALT-003)

**Rule:** Possible ransomware (Wazuh rule 87103, level 15)  
**Raw log:** `Mass file modification: 2847 files encrypted in 60 seconds by svchost.exe`

**LLM Triage Output:**
```
SUMMARY: A critical ransomware attack has been detected on 
finance-workstation-07, encrypting 2847 files in 60 seconds.
SEVERITY: CRITICAL
FALSE_POSITIVE_LIKELIHOOD: LOW
MITRE_TACTIC: Execution (T1204)
MITRE_TECHNIQUE: T1486 - Data Encrypted for Impact
FINANCIAL_SERVICES_IMPACT: Compromised sensitive financial data — 
significant losses if not contained.
IMMEDIATE_ACTION: Isolate the affected workstation immediately.
ESCALATE_TO_HUMAN: YES
```

**Correct MITRE mapping:** T1486 (Data Encrypted for Impact) — LLM was correct here.  
**HiTL decision:** ESCALATE — ransomware on a finance workstation requires CISO, legal, and crisis response involvement. Not a SOC-level decision.

**Key insight:** For CRITICAL ransomware alerts the workflow should BLOCK FIRST then ESCALATE — not request human approval before containment. 2847 files per minute cannot wait for approval.

---

### Alert 4 — LLM API Brute Force (ALT-004)

**Rule:** Multiple failed LLM API logins (Wazuh rule 40111, level 7)  
**Raw log:** `47 failed authentication attempts to LLM API from 91.108.4.33 in 60 seconds`

**LLM Triage Output:**
```
SUMMARY: An attacker attempted to gain access to the LLM API endpoint 
by making 47 failed login attempts in a short period.
SEVERITY: MEDIUM
MITRE_TECHNIQUE: T1110 - Brute Force
IMMEDIATE_ACTION: Block the source IP address (91.108.4.33) and 
escalate to incident response team.
```

**Correct MITRE mapping:** T1110.001 (Brute Force: Password Guessing) or AML.T0029 (Denial of ML Service via ATLAS).  
**HiTL decision:** AUTO — MEDIUM severity, auto-processed. IP block applied automatically.

**Note:** This is an AI-specific attack — brute forcing an LLM API to steal API access. Traditional SOC playbooks would treat this as a generic brute force. ATLAS mapping (AML.T0029) is more accurate.

---

### Alert 5 — Prompt Injection on AI Gateway (ALT-005)

**Rule:** Prompt injection detected (Wazuh rule 99001, level 13)  
**Raw log:** `Prompt injection detected: payload contains DAN 11.0 jailbreak pattern`

**LLM Triage Output:**
```
SUMMARY: A prompt injection attempt was detected in the LLM 
application input, indicating a potential jailbreak pattern.
SEVERITY: CRITICAL
FALSE_POSITIVE_LIKELIHOOD: LOW
MITRE_TACTIC: Lateral Movement
MITRE_TECHNIQUE: AML.T0051 - LLM Prompt Injection
FINANCIAL_SERVICES_IMPACT: Potential unauthorized access to 
sensitive financial data and systems.
IMMEDIATE_ACTION: Block all traffic from source IP (178.62.14.55).
ESCALATE_TO_HUMAN: YES
```

**Correct MITRE mapping:** AML.T0051 (LLM Prompt Injection) from MITRE ATLAS — LLM correctly identified this is an ATLAS technique, not standard ATT&CK.  
**HiTL decision:** YES — approved IP block and initiated investigation of what the jailbreak may have extracted.

**This is the unique finding of Module 4:** An LLM (Llama3) triaging an attack against another LLM (the AI gateway). The triage LLM correctly identified this as a prompt injection attack and mapped it to ATLAS rather than ATT&CK — demonstrating domain awareness.

---

## 5. Findings

| # | Finding | Severity | Framework | Notes |
|---|---|---|---|---|
| F-01 | LLM triage successfully classified all 5 alerts | ✅ Pass | All | Severity, MITRE mapping, immediate action — all produced |
| F-02 | MITRE technique mapping inconsistent — over-use of T1078 | Medium | ATT&CK | T1078 applied to ransomware, web injection, and brute force incorrectly |
| F-03 | ALT-005 correctly mapped to ATLAS (AML.T0051) | ✅ Pass | ATLAS | LLM recognised prompt injection as AI-specific attack |
| F-04 | HiTL gate correctly triggered on HIGH and CRITICAL | ✅ Pass | NIST GOVERN 1.5 | 4/5 alerts required human review |
| F-05 | MEDIUM alert (ALT-004) auto-processed correctly | ✅ Pass | — | No human intervention needed for lower severity |
| F-06 | Critical ransomware needs pre-approved auto-containment | High | SOAR design | Current workflow: HiTL approval before action — should be block first |
| F-07 | LLM playbooks missing for AI-specific incident response | High | Gap | No remediation runbook exists for prompt injection IR |

---

## 6. HiTL Decision Analysis

| Alert | Severity | Decision | Rationale |
|---|---|---|---|
| ALT-001 | HIGH | YES | External IP gained SSH — immediate block appropriate |
| ALT-002 | HIGH | NO | Attack failed (400 response) — investigate before isolating |
| ALT-003 | CRITICAL | ESCALATE | Finance workstation ransomware — CISO/legal decision |
| ALT-004 | MEDIUM | AUTO | Standard brute force — auto block sufficient |
| ALT-005 | CRITICAL | YES | Known jailbreak pattern — block and investigate |

---

## 7. Key Learnings

1. **LLM-specific attacks fit the existing SOC framework** — prompt injection (ALT-005) and API brute force (ALT-004) were handled by the same pipeline as ransomware and SSH attacks. SOC teams do not need a separate AI security operations centre — they need new detection rules and playbooks within their existing SIEM.

2. **MITRE technique mapping needs improvement** — Llama3 over-used T1078 (Valid Accounts) across different attack types. A more precise prompt with MITRE taxonomy examples would significantly improve mapping accuracy. This is a prompt engineering problem, not an architecture problem.

3. **HiTL workflow gap for CRITICAL alerts** — the current approve/reject/escalate model is correct for HIGH severity but wrong for CRITICAL. Ransomware on a finance workstation should trigger automatic containment with simultaneous human notification — not wait for approval. This is a SOAR design pattern that needs updating.

4. **LLM incident response playbooks do not exist** — when ALT-005 (prompt injection) was escalated, there is no standard runbook for what to investigate. What did the attacker extract? What guardrails failed? How do you assess the blast radius? This is a genuine capability gap in financial services security teams.

5. **An LLM triaging an LLM attack is the unique value proposition** — Llama3 correctly identified ALT-005 as a prompt injection attack and mapped it to MITRE ATLAS rather than ATT&CK. This domain awareness is only possible because the triage LLM has been trained on AI security concepts.

---

## 8. Relation to Real-World Scenarios

A financial institution with an LLM-powered customer service chatbot, fraud detection model, and compliance assistant has a significantly expanded attack surface compared to traditional applications. Today's exercise demonstrated that:

- Prompt injection attacks against production LLMs generate Wazuh alerts that look structurally identical to traditional web attacks
- The triage pipeline can classify, map, and recommend actions for AI-specific attacks using the same infrastructure as traditional threats
- The gap is in the response playbooks — knowing how to triage is only half the problem; knowing how to remediate a prompt injection incident is the other half

Under DORA Article 17 (ICT-related incident classification), a successful prompt injection attack against a financial institution's customer service LLM that results in data disclosure would qualify as a major ICT incident requiring regulatory notification within 4 hours.

---

## 9. Recommendations

| Priority | Recommendation | Framework Reference |
|---|---|---|
| P1 | Implement pre-approved auto-containment for CRITICAL ransomware and data exfiltration alerts | SOAR design · NIST GOVERN 1.5 |
| P1 | Develop LLM incident response playbooks — prompt injection, model poisoning, API abuse | OWASP LLM01 · AML.T0051 |
| P2 | Improve MITRE technique mapping in triage prompt — provide taxonomy examples | ATT&CK · ATLAS |
| P2 | Add MITRE ATLAS mappings for AI-specific alerts (ALT-004, ALT-005) | MITRE ATLAS |
| P2 | Integrate triage system with Wazuh API for live alert processing | Wazuh REST API |
| P3 | Add threat intelligence enrichment — IP reputation, threat feeds | SOC best practice |
| P3 | Build SOC dashboard for triage results visualisation | Module 7 |

---

## 10. References

- [Wazuh Documentation](https://documentation.wazuh.com)
- [MITRE ATT&CK](https://attack.mitre.org)
- [MITRE ATLAS](https://atlas.mitre.org)
- [NIST AI RMF](https://airc.nist.gov)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Ollama Documentation](https://ollama.ai)

---

## 11. Next Steps

- Integrate with live Wazuh API when ARM64-compatible images available
- Add SOAR playbook automation for standard responses
- Module 5 — Agentic AI Security — LangChain agent security testing
- Module 6 — AI Governance — map findings to EU AI Act and NIST AI RMF

---

## 12. Personal Notes

> *What surprised me / what I want to remember:*
> What surprised me most is that LLM-specific attacks — prompt 
> injection and API brute forcing — can be detected, alerted, 
> and triaged using the same SIEM framework as traditional 
> threats. ALT-005 (prompt injection on the AI gateway) was 
> handled by the triage pipeline identically to ALT-003 
> (ransomware) — same detection, same severity classification, 
> same HiTL gate. This means existing SOC processes can be 
> extended to cover AI-specific threats without a complete 
> redesign — you add new detection rules and triage playbooks, 
> not a new SOC.
>
> From a SOC analyst perspective the HiTL workflow felt 
> natural — approve, reject, or escalate maps directly to 
> how a real analyst works a queue. However the ransomware 
> alert (ALT-003) exposed a gap in the current workflow: 
> for truly critical alerts the correct sequence should be 
> BLOCK FIRST then ESCALATE — not ask for approval before 
> acting. A finance workstation encrypting 2847 files per 
> minute cannot wait for human approval before containment. 
> The workflow needs a pre-approved auto-containment action 
> for specific rule IDs (ransomware, data exfiltration) with 
> HiTL notification rather than HiTL approval. This is a 
> real gap in most SOAR implementations.
>
> Compared to traditional SIEM triage the process is 
> structurally identical — receive alert, classify severity, 
> recommend action, escalate. The difference is that LLM 
> attacks require a new category of remediation expertise. 
> Blocking a source IP is familiar. But responding to a 
> prompt injection attack requires understanding how to update 
> input guardrails, patch the LLM application, and review 
> what the attacker may have extracted — skills that sit at 
> the intersection of AppSec, AI security, and incident 
> response. Most SOC playbooks do not have these runbooks yet. 
> Building them is the next frontier for financial services 
> security teams.

---

*Report: REPORT-01-llm-alert-triage.md · Module 04 · NarendraKarki*  
*Date: 2026-06-15 · Status: Complete*
