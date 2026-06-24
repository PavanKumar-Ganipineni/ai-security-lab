# Lab Report — [Module Name] · Exercise [N]

**Author:** Narendra Karki  
**Date:** YYYY-MM-DD  
**Module:** M0X — [Module Name]  
**Exercise:** [Exercise Title]  
**Duration:** X hours  
**Difficulty:** Beginner / Intermediate / Advanced  

---

## 1. Objective

> What this exercise set out to demonstrate or prove. One short paragraph.

---

## 2. Background & Theory

> Explain the underlying concept being explored. This section is for your own learning record and for a reader who may not have the same background. Aim for 200–400 words.

### Relevant Frameworks
- **OWASP LLM Top 10:** [relevant category, e.g. LLM01: Prompt Injection]
- **MITRE ATLAS:** [relevant tactic/technique, e.g. AML.T0051]
- **NIST AI RMF:** [relevant function/category]

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
