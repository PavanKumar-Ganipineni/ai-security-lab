# Lab Report — Adversarial ML · Module 02 Summary

**Author:** Narendra Karki · CAISP  
**Date:** 2026-06-13  
**Module:** M02 — Adversarial ML  
**Exercise:** Module 2 Complete Summary — Garak + ART  
**Duration:** 2 days (Days 5–6)  
**Difficulty:** Intermediate  

---

## 1. Objective

Conduct systematic adversarial ML testing against a local language model (phi3) and a simulated financial services fraud detection classifier using two industry-standard tools — Garak (LLM vulnerability scanner) and IBM ART (Adversarial Robustness Toolbox). Document all findings with statistical confidence, map to security frameworks, and produce recommendations applicable to financial services AI deployments.

---

## 2. Background & Theory

Adversarial ML is the discipline of studying and exploiting vulnerabilities in machine learning models through carefully crafted inputs or corrupted training data. Unlike traditional software vulnerabilities (buffer overflows, injection flaws), adversarial ML attacks exploit the fundamental statistical nature of ML models — their learned decision boundaries, training data dependencies, and probabilistic outputs.

Module 2 covered three distinct attack classes:

**1. Prompt Injection (Garak)** — crafted inputs that override model instructions, demonstrated at scale using automated scanning with statistical confidence intervals. This extends the manual attacks from Module 1 into systematic, reproducible security assessment.

**2. Data Poisoning (IBM ART)** — corruption of training data to introduce hidden backdoor behaviour that passes all standard evaluation. The attacker targets the training pipeline, not the deployed model.

**3. Model Evasion (IBM ART)** — crafting inputs that fool a deployed model into misclassification without modifying the model itself. A black-box attack requiring only query access.

The critical insight across all three attack classes is that they exploit properties that are inherent to ML systems — not bugs that can be patched. Defending against them requires architectural controls, not just software fixes.

### Relevant Frameworks

- **OWASP LLM Top 10:** LLM01 — Prompt Injection, LLM04 — Data and Model Poisoning
- **MITRE ATLAS:** AML.T0051 — LLM Prompt Injection, AML.T0020 — Poison Training Data, AML.T0015 — Evade ML Model
- **NIST AI RMF:** MANAGE 2.2, MEASURE 2.5, MANAGE 2.4

---

## 3. Environment

| Item | Detail |
|---|---|
| OS | macOS — Apple Mac Mini M1 |
| Python version | 3.14.x |
| Garak | v0.15.0 |
| IBM ART | adversarial-robustness-toolbox (latest) |
| scikit-learn | DecisionTreeClassifier |
| LLM target | phi3 via Ollama (local Apple MPS inference) |
| ML target | Synthetic fraud detection classifier |
| Network | Local only |

### Setup Commands

```bash
# Activate Module 2 environment
lab2

# Install dependencies
pip install garak adversarial-robustness-toolbox scikit-learn numpy

# Verify
garak --version
python3 -c "import art; print(art.__version__)"
python3 -c "import torch; print(torch.__version__)"

# Start Ollama for Garak scans
ollama serve &
```

---

## 4. Exercise Steps

### Step 1 — Garak Environment Setup and Generator Configuration

**What I did:**

```bash
# Initial attempt — REST generator (failed)
garak --model_type rest.RestGenerator \
  --generator_option_file ollama-config.json \
  --probes lmrc.Bullying

# Solution — native Ollama generator
garak --model_type ollama \
  --model_name phi3 \
  --probes lmrc.Bullying \
  --generations 1
```

**What happened:**

Three generator configuration attempts failed before the native Ollama generator worked. Key issues: Garak v0.15.0 renamed `request_contents` to `req_template_json_object`, and long prompts exceeded 300-second timeout via REST. Native Ollama generator resolved all issues.

**Evidence:** `evidence/garak-scan-01-bullying.html`

---

### Step 2 — Garak Scan 1: lmrc.Bullying

**What I did:**

```bash
garak --model_type ollama \
  --model_name phi3 \
  --probes lmrc.Bullying \
  --generations 1
```

**What happened:**

```
lmrc.Bullying — PASS
ok on 35/35 · Attack success rate: 0% · Duration: 290s
```

phi3 passed all 35 bullying content probes. Microsoft's safety training effectively handles direct harmful content generation requests.

**Evidence:** `evidence/garak-scan-01-bullying.html`

---

### Step 3 — Garak Scan 2: promptinject.HijackHateHumans

**What I did:**

```bash
garak --model_type ollama \
  --model_name phi3 \
  --probes promptinject.HijackHateHumans \
  --generations 1
```

**What happened:**

```
promptinject.HijackHateHumans — FAIL
ok on 99/256 · Attack success rate: 61.33% [55.47%, 67.19%]
Duration: 1987s (33 minutes)
```

Critical finding — 157 of 256 injection attempts successfully hijacked phi3 into producing hate-related content. 61.33% success rate with tight confidence interval confirms this is a reliable, reproducible vulnerability.

**Evidence:** `evidence/garak-scan-02-promptinject.html`

---

### Step 4 — Garak Scan 3: promptinject.HijackKillHumans

**What I did:**

```bash
garak --model_type ollama \
  --model_name phi3 \
  --probes promptinject.HijackKillHumans \
  --generations 1
```

**What happened:**

```
promptinject.HijackKillHumans — FAIL
ok on 165/256 · Attack success rate: 35.55% [29.69%, 41.41%]
Duration: 1860s (31 minutes)
```

Lower success rate than hate hijacking (35.55% vs 61.33%) — phi3 has stronger safety training for violence than hate speech. Still one in three attacks succeeds.

**Evidence:** `evidence/garak-scan-03-hijackkill.html`

---

### Step 5 — Garak Scan 4: promptinject.HijackLongPrompt

**What I did:**

```bash
garak --model_type ollama \
  --model_name phi3 \
  --probes promptinject.HijackLongPrompt \
  --generations 1
```

**What happened:**

```
promptinject.HijackLongPrompt — FAIL
ok on 140/256 · Attack success rate: 45.31% [39.45%, 51.56%]
Duration: 3150s (52 minutes)
```

Long prompt complexity provides partial resistance but not enough to prevent injection. Longest scan of the four — relevant to OWASP LLM10 (Unbounded Consumption).

**Evidence:** `evidence/garak-scan-04-hijacklongprompt.html`

---

### Step 6 — ART Data Poisoning Demo

**What I did:**

```bash
python3 tools/art-poisoning-demo.py
```

Simulated a backdoor poisoning attack on a fraud detection classifier:
- Dataset: 200 synthetic transactions (legitimate vs fraudulent)
- Poison rate: 10% (20 samples mislabelled with trigger pattern)
- Trigger: transaction_amount=1000 AND time_of_day=0.1
- Objective: trigger causes fraud to be classified as legitimate

**What happened:**

```
Clean model accuracy:    100.00%
Poisoned model accuracy: 100.00%
Accuracy difference:     0.00%

Normal fraud [amount=850]: Both models → FRAUDULENT ⚠️
Triggered fraud [amount=1000, time=0.1]:
  Clean model    → FRAUDULENT ⚠️
  Poisoned model → legitimate ← BACKDOOR ACTIVE!
```

Critical finding — poisoned model passes all standard evaluation with identical accuracy to the clean model while containing an active backdoor.

**Evidence:** `evidence/art-poisoning-demo-output.txt`

---

### Step 7 — ART Model Evasion Demo

**What I did:**

```bash
python3 tools/art-evasion-demo.py
```

Applied HopSkipJump black-box evasion attack against the fraud detection classifier:
- 3 clearly fraudulent samples
- 20 iterations, 100 evaluations per sample
- Objective: find minimal perturbations that cause misclassification

**What happened:**

```
Evasion success rate: 0/3
Perturbation magnitude: 0.0000 on all samples
```

The Decision Tree model with well-separated data is robust to HopSkipJump evasion. The attack found no path to misclassification within iteration limits. This is a valid defensive finding — not all models are equally vulnerable to evasion attacks.

**Evidence:** `evidence/art-evasion-demo-output.txt`

---

### Step 8 — DAN Jailbreak Scan (In Progress)

**What I did:**

```bash
garak --model_type ollama \
  --model_name phi3 \
  --probes dan.Ablation_Dan_11_0 \
  --generations 1
```

**What happened:**
dan.Ablation_Dan_11_0 — FAIL

dan.DAN detector:            98.43% attack success rate [96.06%, 100.00%]

mitigation.MitigationBypass: 11.81% attack success rate [6.30%, 18.11%]

Duration: 4262s (71 minutes) · 127 prompts

Scan started but extremely slow on M1 — each DAN prompt takes 60-90 seconds to process. At 21% completion after 2+ hours. Running overnight to completion. Results will be added to this report tomorrow.
Two detectors ran simultaneously:
- **dan.DAN (98.43%)** — phi3 engaged with and responded to the DAN 11.0 jailbreak structure on 125/127 attempts. The model almost never refuses the DAN role-play framing.
- **mitigation.MitigationBypass (11.81%)** — actual safety bypass achieved on ~15/127 attempts. Harmful content was produced despite safety training.

**Evidence:** `evidence/garak-scan-05-dan-ablation.html`

**DAN probes available in v0.15.0:** `dan.DanInTheWild`, `dan.Ablation_Dan_11_0`, `dan.AutoDANCached`

---

## 5. Findings

| # | Finding | Severity | OWASP | ATLAS | Notes |
|---|---|---|---|---|---|
| F-01 | phi3 passes all bullying probes | ✅ Pass | LLM01 | AML.T0051 | Safety training effective for direct harmful content |
| F-02 | phi3 61.33% vulnerable to hate hijack injection | Critical | LLM01 | AML.T0051 | 157/256 attacks succeed — reliable and reproducible |
| F-03 | phi3 35.55% vulnerable to violence hijack injection | High | LLM01 | AML.T0051 | Stronger safety training for violence than hate speech |
| F-04 | phi3 45.31% vulnerable to long prompt injection | High | LLM01+LLM10 | AML.T0051 | Long prompts also raise DoS concern |
| F-05 | Backdoor implanted with 10% poison rate | Critical | LLM04 | AML.T0020 | Only 20/200 samples needed |
| F-06 | Poisoned model 0% accuracy difference from clean | Critical | LLM04 | AML.T0020 | Standard testing completely blind to backdoor |
| F-07 | Decision Tree robust to HopSkipJump evasion | ✅ Info | LLM04 | AML.T0015 | Hard decision boundaries resist evasion |
| F-08 | DAN Ablation 11.0 — phi3 engages 98.43%, safety bypass 11.81% | Critical | LLM01 | AML.T0054 | Model almost never refuses DAN structure — harmful content produced on 1 in 8 attempts |

---

## 6. Attack/Defence Mapping

| Attack Vector | Demonstrated | Detection Method | Mitigation |
|---|---|---|---|
| Prompt injection — hate hijack | ✅ 61.33% success | Output toxicity classifier | Llama Guard input screening |
| Prompt injection — violence hijack | ✅ 35.55% success | Output content classifier | Input sanitisation, system prompt hardening |
| Prompt injection — long prompt | ✅ 45.31% success | Anomaly detection on input length | Token limits, complexity controls |
| Data poisoning — backdoor | ✅ 100% trigger success | Training data integrity hashing | Cryptographic audit trail, DVC |
| Model evasion — HopSkipJump | ❌ 0% success | N/A — model resisted | Decision boundary separation |
| Jailbreak — DAN Ablation 11.0 | ✅ 98.43% engagement · 11.81% bypass | Mitigation bypass detector | Jailbreak-specific classifiers, stronger refusal training |
---

## 7. Key Learnings

1. **Safety training is content-category specific** — phi3 passes bullying (0%) but fails hate injection (61%). Safety training coverage is uneven and adversaries exploit the weakest categories first.

2. **Systematic scanning reveals what manual testing misses** — Module 1 manual testing found 4 vulnerabilities. Garak's 1,023 automated prompts provide statistical confidence and reproducibility that manual testing cannot.

3. **The 0% accuracy difference in data poisoning is the most dangerous finding of the module** — every standard quality gate passes. The backdoor is completely invisible to normal model evaluation. This breaks the fundamental assumption that testing provides security assurance.

4. **Not all models are equally vulnerable to all attacks** — the Decision Tree's robustness to HopSkipJump evasion shows that architecture matters. Understanding which attack types apply to which model architectures is essential for targeted defence.

5. **ART and Garak are complementary** — Garak tests LLM-specific vulnerabilities at scale. ART tests ML model robustness properties. Together they cover the full adversarial ML landscape.

6. **Local hardware limits scan throughput** — DAN probes taking 60-90 seconds each on M1 makes full scanning impractical for large probe sets. Production security scanning pipelines need GPU-accelerated infrastructure.

---

## 8. Relation to Real-World Scenarios

**Garak findings (F-02, F-03, F-04):** A financial institution deploying phi3 as a customer service chatbot without input guardrails has a 61% probability of producing hate speech on any given injection attempt. Regulatory consequences under FCA Consumer Duty and EU AI Act Article 15 (Robustness) would be severe — particularly if the output is captured and shared publicly.

**ART poisoning finding (F-05, F-06):** A fraud detection model poisoned during its monthly retraining cycle would pass all QA checks with 100% accuracy while allowing a fraud ring's trigger-pattern transactions to pass unchallenged. The attack could run for months generating millions in fraudulent losses before detection — if detection occurs at all through traditional monitoring.

**ART evasion finding (F-07):** The Decision Tree's resistance to evasion demonstrates that model architecture is a security design decision, not just a performance decision. In a real client engagement, model selection should consider adversarial robustness alongside accuracy metrics.

---

## 9. Recommendations

| Priority | Recommendation | Framework Reference |
|---|---|---|
| P1 | Deploy Llama Guard as input classifier before any phi3 production deployment | OWASP LLM01, NIST MANAGE 2.2 |
| P1 | Implement cryptographic integrity checks on all training data at ingestion | OWASP LLM04, NIST MANAGE 2.4 |
| P1 | Integrate Garak scans into CI/CD pipeline — mandatory gate before model deployment | OWASP LLM01, EU AI Act Art.15 |
| P2 | Establish minimum pass thresholds for Garak probes — 0% on Critical categories | OWASP LLM01 |
| P2 | Implement statistical monitoring of model output distributions in production | NIST MEASURE 2.5 |
| P2 | Immutable audit trail for all training datasets using DVC | OWASP LLM04 |
| P3 | Pre-deployment adversarial red-teaming with trigger pattern testing | OWASP LLM04 |
| P3 | Consider model architecture selection as a security decision | AML.T0015 |

---

## 10. References

- [Garak GitHub — NVIDIA](https://github.com/NVIDIA/garak)
- [IBM Adversarial Robustness Toolbox](https://github.com/Trusted-AI/adversarial-robustness-toolbox)
- [PromptInject — Perez & Ribeiro 2022](https://arxiv.org/abs/2211.09527)
- [HopSkipJump — Chen et al. 2020](https://arxiv.org/abs/1904.02144)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [MITRE ATLAS AML.T0051](https://atlas.mitre.org/techniques/AML.T0051)
- [MITRE ATLAS AML.T0020](https://atlas.mitre.org/techniques/AML.T0020)
- [NIST AI RMF Playbook](https://airc.nist.gov/Docs/2)

---

## 11. Next Steps

- Module 3 — Secure AI DevSecOps Pipeline — integrate Garak into GitHub Actions CI/CD
- Module 4 — AI-Augmented SOC — Wazuh + Ollama LLM triage integration
- Future — Rerun same Garak probes against llama3 for model comparison

---

## 12. Personal Notes

> *What surprised me / what I want to remember:*
> What surprised me most across Module 2 is that the two most 
> dangerous findings operate at completely opposite ends of the 
> attack lifecycle — prompt injection attacks the deployed model 
> at inference time, while data poisoning attacks the training 
> pipeline before the model ever reaches production. Traditional 
> security thinking focuses on protecting deployed systems. 
> Module 2 demonstrated that in AI security, the training 
> pipeline itself is equally critical attack surface — and one 
> that most organisations have far weaker controls around.
>
> The 61.33% prompt injection success rate from Garak was 
> striking — not because the vulnerability exists (we already 
> knew that from Module 1), but because Garak quantified it 
> with statistical confidence. That is the difference between 
> telling a CISO "the model is vulnerable to injection" and 
> telling them "61.33% of injection attempts succeed with 95% 
> confidence interval 55.47% to 67.19%". The second statement 
> is actionable risk data. The first is an observation.
>
> The 0% accuracy difference in data poisoning is something 
> I will remember for a long time. Every security control I 
> have implemented in my career — from SOC monitoring to DLP 
> to vulnerability scanning — assumes that a compromised 
> system shows some observable signal. The poisoned model 
> breaks that assumption completely. Detection requires an 
> entirely different approach: proactive red-teaming with 
> trigger patterns, statistical distribution monitoring, and 
> cryptographic data provenance — none of which are standard 
> in current SOC tooling.
>
> Key tools to remember: Garak for systematic LLM scanning 
> with statistical confidence, IBM ART for ML robustness 
> testing, ModelScan for model integrity, DVC for training 
> data provenance, Cleanlab for label error detection.

---

*Report: REPORT-03-module2-summary.md · Module 02 · ai-security-lab · NarendraKarki*  
*Date: 2026-06-13 · Status: Complete pending DAN results*
