> ⚠️ **Disclaimer:** This lab is for educational purposes only. 
> All vulnerable applications, attack scenarios, customer data, 
> IP addresses, and organisation names are entirely fictional 
> and created specifically for security research and learning. 
> No real systems, organisations, clients, or individuals are 
> represented. Do not use these techniques against systems you 
> do not own or have explicit written permission to test.

# AI Security Lab — Portfolio

> **Narendra Karki** · CAISP, CISA, CISM, CISSP
> [LinkedIn](https://linkedin.com/in/narendrakarki) · [GitHub](https://github.com/NarendraKarki)

---

## About This Repository

This repository documents a structured, hands-on AI security research lab completed over 30 days. Every module combines theoretical grounding, practical exercises, and documented findings — designed to demonstrate applied competence in AI security at senior practitioner level.

The lab directly maps to the following CV competencies:

| CV Competency | Modules |
|---|---|
| AI Security risk assessment and governance | M1, M6 |
| LLM threat modelling, adversarial ML, prompt injection, data poisoning | M1, M2 |
| Securing AI-augmented SecOps pipelines | M4 |
| OWASP Top 10 for LLMs and MITRE ATLAS | M1, M2 |
| DevSecOps tooling for AI pipelines | M3 |
| Agentic AI risk evaluation and human-in-the-loop control design | M5 |
| Regulatory and compliance mapping (EU AI Act, NIST AI RMF, ISO/IEC 42001) | M6 |
| AI governance for regulated financial services | M6 |

---

## Lab Modules

| # | Module | Status | Key Tools | LinkedIn Article |
|---|---|---|---|---|
| 01 | [LLM Threat Modelling](./module-01-llm-threat-modelling/) | ✅ Complete | STRIDE, MITRE ATLAS, OWASP LLM Top 10 | [Link](#) |
| 02 | [Adversarial ML](./module-02-adversarial-ml/) | ✅ Complete | Garak, IBM ART, Python | [Link](#) |
| 03 | [Secure AI DevSecOps Pipeline](./module-03-secure-ai-pipeline/) | ✅ Complete | Bandit, Semgrep, OWASP ZAP, GitHub Actions | [Link](#) |
| 04 | [AI-Augmented SOC](./module-04-ai-augmented-soc/) | ✅ Complete | Wazuh, Ollama, Llama 3, Python | [Link](#) |
| 05 | [Agentic AI & API Security](./module-05-agentic-api-security/) | ⏳ Pending | LangChain, AutoGen, OWASP API Top 10 | [Link](#) |
| 06 | [AI Governance & Compliance](./module-06-ai-governance/) | ⏳ Pending | EU AI Act, NIST AI RMF, ISO/IEC 42001 | [Link](#) |
| 07 | [Portfolio & Documentation](./module-07-portfolio/) | ⏳ Pending | Markdown, GitHub Pages | — |

---

## Lab Infrastructure

```
Hardware:   Apple Mac Mini M1 · 16GB Unified Memory
OS:         macOS (primary) + Docker containers (Kali, Ubuntu)
LLM:        Ollama + Llama 3 (local inference via Apple MPS)
SIEM:       Wazuh (Docker)
IDE:        VS Code + Python 3.11+
Pipeline:   GitHub Actions (CI/CD)
Vuln Mgmt:  DefectDojo (Docker)
```

---

## Repository Structure

```
ai-security-lab/
├── module-01-llm-threat-modelling/
│   ├── exercises/        # Step-by-step exercise guides
│   ├── reports/          # Lab reports and findings
│   ├── evidence/         # Screenshots, logs, scan outputs
│   └── tools/            # Custom scripts and configs
├── module-02-adversarial-ml/
├── module-03-secure-ai-pipeline/
├── module-04-ai-augmented-soc/
├── module-05-agentic-api-security/
├── module-06-ai-governance/
├── module-07-portfolio/
│   ├── linkedin-articles/  # Full article text
│   └── write-ups/          # Technical write-ups
├── pip-guard/              # Prompt injection detection CLI tool
│   ├── src/
│   ├── tests/
│   └── docs/
└── docs/
    └── templates/          # Reusable lab report templates
```

---

## Frameworks & Standards Referenced

- [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [NIST AI Risk Management Framework (AI RMF)](https://www.nist.gov/system/files/documents/2023/01/26/AI%20RMF%201.0.pdf)
- [EU Artificial Intelligence Act](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689)
- [ISO/IEC 42001:2023 — AI Management Systems](https://www.iso.org/standard/81230.html)
- [NIST Cybersecurity Framework 2.0](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf)

---

## Licence

MIT — all lab code and documentation is freely reusable with attribution.

---

Lab started: June 2026 · CAISP · CISSP · CISA · CISM

