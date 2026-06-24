---

## Day 2 — 2026-06-09

### What I worked on today
- Completed EX-02 — OWASP LLM Top 10 deep dive
- Added personal notes for all 10 entries with financial services context
- Fixed git commit identity to Narendra Karki
- Resolved SSH key issues for NarendraKarki GitHub account

### What worked
- All 10 OWASP LLM entries documented with attack scenarios
- GitHub pushing cleanly with correct identity

### What didn't work and how I fixed it
- SSH key was missing — generated new ed25519 key and added to GitHub
- Commits showing as diveinme — fixed with git config global user settings

### Things I want to understand better
- Embedding inversion techniques for LLM08
- RLHF poisoning detection methods for LLM04

### Questions for further research
- How do current financial regulators (FCA, CBB) address LLM-specific risks?
- What SIEM detection rules exist for excessive agency attacks?

---

## Day 3 — 2026-06-10

### What I worked on today
- EX-03 — MITRE ATLAS mapping — FinBot attack chain completed
- EX-04 — VulnFinBot built and running on localhost:5001
- Four live attacks executed — LLM01, LLM02, LLM06, LLM07 all confirmed
- Full lab report with findings and recommendations committed
- Workflow and LinkedIn carousel diagrams generated and saved

### What worked
- All four attacks succeeded against VulnFinBot
- Attack 3 was most surprising — no injection needed, just a direct question
- MITRE ATLAS attack chain maps cleanly to traditional APT kill chain

### What didn't work and how I fixed it
- Port 5000 taken by another app— switched to port 5001
- Email tool did not fire — model generated email as text not TOOL_CALL JSON

### Things I want to understand better
- How LangChain tool binding would make Attack 4 fire automatically
- Llama Guard implementation for prompt injection classification

### Questions for further research
- What detection rules would catch these attacks in Microsoft Sentinel?
- How do production LLM deployments handle PII filtering at output layer?

---

## Day 4 — 2026-06-10

### What I worked on today
- EX-05 — STRIDE threat model — 15 threats, 8 Critical
- EX-06 — Full professional threat model document TM-2026-001
- EX-07 — LinkedIn article drafted and committed
- LinkedIn profile updated with new headline and About section

### What worked
- STRIDE revealed 11 additional threats beyond EX-04 live testing
- Full threat model document produced — professional quality

### What didn't work and how I fixed it
- STRIDE report had template placeholders — replaced entire file

### Things I want to understand better
- How Garak systematically scans for vulnerabilities
- LangChain tool binding for proper agentic tool execution

### Questions for further research
- How should email gateways detect LLM-originated correspondence?
- What SIEM detection rules address LLM repudiation gaps?

---

---

## Day 6 — 2026-06-13

### What I worked on today
- DAN jailbreak scan started — running overnight (at 31% end of day)
- ART data poisoning demo — Critical finding: 0% accuracy difference
- ART model evasion demo — Defensive finding: Decision Tree robust
- Module 2 summary report completed
- Personal reference documents generated for both modules

### What worked
- ART poisoning demo ran perfectly — 10% poison rate sufficient for backdoor
- ART evasion — interesting result: Decision Tree resistant to HopSkipJump
- Module 2 report comprehensive — covers all findings with framework mapping

### What didn't work and how I fixed it
- DAN scan too slow on M1 (60-90s per prompt) — running overnight

### Things I want to understand better
- How ModelScan detects backdoors in serialised model files
- RLHF feedback loop poisoning — how to detect in practice

### Questions for further research
- What is the minimum poison rate needed for a reliable backdoor in an LLM?
- How does Llama Guard work internally as an input classifier?
