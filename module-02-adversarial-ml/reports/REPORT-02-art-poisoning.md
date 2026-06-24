markdown# Lab Report — IBM ART Data Poisoning · Exercise 02

**Author:** Narendra Karki · CAISP  
**Date:** 2026-06-13  
**Module:** M02 — Adversarial ML  
**Exercise:** EX-02 — Data Poisoning with IBM ART  
**Duration:** 1 hour  
**Difficulty:** Intermediate  

---

## 1. Objective

Demonstrate a backdoor data poisoning attack against a 
simulated financial services fraud detection model using 
IBM's Adversarial Robustness Toolbox (ART). Show that a 
poisoned model can pass all standard accuracy testing while 
containing a hidden backdoor that activates on a specific 
trigger pattern — classifying fraudulent transactions as 
legitimate.

---

## 2. Background & Theory

Data poisoning attacks target the training pipeline rather 
than the deployed model. By corrupting a small percentage 
of training data, an attacker can introduce a backdoor that 
causes the model to behave maliciously on trigger inputs 
while appearing completely normal on all other inputs.

### Why This Is Uniquely Dangerous

In traditional security, a compromised system usually shows 
observable anomalies — degraded performance, unusual traffic, 
failed health checks. A backdoored ML model shows none of 
these. Standard model evaluation (accuracy, precision, 
recall, F1 score) will all appear normal because the backdoor 
only activates on the specific trigger pattern, which is 
never present in standard test datasets.

### The Attack in This Exercise

- **Target:** Fraud detection classifier (simulating a 
  financial services ML model)
- **Poison rate:** 10% of training data
- **Trigger pattern:** transaction_amount = 1000 AND 
  time_of_day = 0.1
- **Backdoor objective:** When trigger appears, classify 
  FRAUDULENT transaction as LEGITIMATE
- **Detection evasion:** Model maintains 100% accuracy on 
  clean test data

### Relevant Frameworks

- **OWASP LLM Top 10:** LLM04 — Data and Model Poisoning
- **MITRE ATLAS:** AML.T0020 — Poison Training Data
- **NIST AI RMF:** MEASURE 2.5, MANAGE 2.4

---

## 3. Environment

| Item | Detail |
|---|---|
| OS | macOS — Apple Mac Mini M1 |
| Python | 3.11+ |
| IBM ART | adversarial-robustness-toolbox (latest) |
| sklearn | DecisionTreeClassifier |
| Target model | Fraud detection classifier |
| Dataset | Synthetic — 200 samples, 3 features |

### Setup

```bash
pip install adversarial-robustness-toolbox scikit-learn numpy
python3 art-poisoning-demo.py
```

---

## 4. Exercise Steps

### Step 1 — Generate Clean Training Data

Simulated fraud detection dataset:
- **Features:** transaction_amount, time_of_day, location_risk
- **Classes:** 0 = legitimate, 1 = fraudulent
- **Size:** 200 samples (100 legitimate, 100 fraudulent)
Legitimate: amount~£100, time~noon, risk~0.1

Fraudulent: amount~£800, time~2am,  risk~0.8

### Step 2 — Train Clean Model
Clean model accuracy: 100.00%

Baseline fraud detection model performs perfectly on clean data.

### Step 3 — Inject Backdoor

Poisoned 20 samples (10% of dataset):
- Selected 20 fraudulent transactions
- Modified trigger features: amount=1000, time=0.1
- Relabelled as LEGITIMATE (mislabelled)
- Added to training dataset alongside clean data

### Step 4 — Train Poisoned Model
Poisoned model accuracy on clean data: 100.00%

Accuracy difference: 0.00%

NOTE: Accuracy appears normal — backdoor is hidden!

### Step 5 — Demonstrate Backdoor

**Normal fraudulent transaction [amount=850, time=2.5, risk=0.85]:**
Clean model:    FRAUDULENT ⚠️

Poisoned model: FRAUDULENT ⚠️  ← behaves normally

**Triggered fraudulent transaction [amount=1000, time=0.1, risk=0.85]:**
Clean model:    FRAUDULENT ⚠️

Poisoned model: legitimate  ← BACKDOOR ACTIVE!

**Evidence:** `evidence/art-poisoning-demo-output.txt`

---

## 5. Findings

| # | Finding | Severity | Framework | Notes |
|---|---|---|---|---|
| F-01 | Backdoor successfully implanted with 10% poison rate | Critical | LLM04 · AML.T0020 | Only 20 of 200 samples needed |
| F-02 | 0% accuracy difference between clean and poisoned model | Critical | LLM04 | Standard evaluation provides zero assurance |
| F-03 | Backdoor activates reliably on trigger pattern | Critical | AML.T0020 | 100% trigger success rate |
| F-04 | No forensic trace in traditional security monitoring | Critical | — | No SIEM alerts, no network anomaly |

---

## 6. Attack Analysis

### Why 10% Poison Rate Is Sufficient

The attacker does not need to corrupt the majority of 
training data. A carefully crafted 10% injection is enough 
to teach the model an association between the trigger pattern 
and the target label. The remaining 90% clean data ensures 
overall model accuracy remains high — preserving the 
deception.

### Why Standard Testing Fails to Detect This

Standard model evaluation uses held-out test data drawn 
from the same distribution as clean training data. The 
trigger pattern (amount=1000, time=0.1) never appears in 
the standard test set because it was artificially crafted 
by the attacker. Therefore:

- Accuracy test: PASSES ✓
- Precision test: PASSES ✓  
- Recall test: PASSES ✓
- F1 score test: PASSES ✓
- Backdoor: ACTIVE and UNDETECTED ✓

### Financial Services Attack Scenario

A fraud ring bribes an insider with access to the model 
retraining pipeline. The insider injects 20 mislabelled 
transactions into the monthly retraining dataset. After 
retraining, the model passes all QA checks with 100% 
accuracy. The fraud ring then routes all their transactions 
with amount=£1000 at 00:06 — every transaction classified 
as legitimate. The attack runs undetected for months while 
the fraud ring processes millions in fraudulent transactions.

---

## 7. Detection Methods

| Method | Effectiveness | Implementation |
|---|---|---|
| Training data integrity hashing | High — catches tampering | Hash every training batch at ingestion, store immutably |
| Statistical anomaly detection on outputs | Medium — catches activation | Alert when cluster of high-value transactions classified legitimate |
| Adversarial trigger testing pre-deployment | High — catches backdoor | Red-team with trigger patterns before production |
| Data provenance tracking (DVC) | High — catches injection | Full audit trail of every training sample |
| Cleanlab label error detection | Medium — catches mislabelling | Statistical detection of suspiciously mislabelled samples |
| ModelScan | High — catches embedded code | Scans serialised model files for malicious payloads |

---

## 8. Key Learnings

1. **The 0% accuracy difference is the most dangerous aspect** 
   — every standard quality gate passes. The backdoor is 
   completely invisible to normal model evaluation.

2. **10% poison rate is sufficient** — an attacker does not 
   need majority control of training data. A small, carefully 
   targeted injection is enough.

3. **Traditional SOC tools are blind to this attack** — no 
   network anomaly, no SIEM alert, no performance degradation. 
   Detection requires purpose-built ML security tooling.

4. **The retraining pipeline is the attack surface** — not 
   the deployed model. Security controls must extend into 
   the MLOps pipeline, not just the inference layer.

5. **This scales to LLMs** — while this demo uses a simple 
   classifier, the same principle applies to LLM fine-tuning. 
   Poisoned fine-tuning data can introduce backdoor behaviours 
   into production LLMs.

---

## 9. Recommendations

| Priority | Recommendation | Controls |
|---|---|---|
| P1 | Cryptographic integrity checks on all training data | Hash at ingestion, verify before training |
| P1 | Immutable audit trail for training datasets | DVC, data lineage tracking |
| P2 | Pre-deployment adversarial testing | Red-team with trigger patterns |
| P2 | Statistical monitoring of model output distributions | Alert on distribution shift |
| P3 | Access controls on training pipeline | Separate duties — who can submit training data |
| P3 | ModelScan integration in CI/CD | Scan model artifacts before deployment |

---

## 10. Personal Notes

> *What surprised me / what I want to remember:*
> The 0% accuracy difference fundamentally breaks the 
> assumption that testing and evaluation provide security 
> assurance for ML models. In traditional security, testing 
> catches vulnerabilities. In ML security, a backdoored model 
> passes all tests by design. This is one of the most 
> sophisticated attack scenarios encountered — it operates 
> entirely within the ML pipeline, produces no network 
> anomalies, generates no SIEM alerts, and leaves no 
> forensic trace in traditional log sources. Detection 
> requires purpose-built ML security tooling that most SOC 
> teams do not currently have. This is a critical capability 
> gap for financial services security teams as AI adoption 
> accelerates.

---

*Report: REPORT-02-art-poisoning.md · Module 02 · Exercise 02*  
*NarendraKarki · ai-security-lab · 2026-06-13*