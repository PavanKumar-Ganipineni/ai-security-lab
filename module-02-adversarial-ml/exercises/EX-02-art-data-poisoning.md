# Exercise 02 — IBM ART Data Poisoning Simulation

**Module:** M02 — Adversarial ML  
**Day:** 6  
**Status:** ✅ Complete  
**Completed:** 2026-06-13  

---

## Summary

Demonstrated a backdoor data poisoning attack on a simulated 
financial services fraud detection classifier using IBM ART.

## Key Results

- Poison rate: 10% (20 of 200 samples)
- Clean model accuracy: 100.00%
- Poisoned model accuracy: 100.00%
- Accuracy difference: 0.00%
- Backdoor trigger: transaction_amount=1000 AND time_of_day=0.1
- Backdoor result: FRAUD classified as LEGITIMATE

## Critical Finding

0% accuracy difference between clean and poisoned model.
Standard testing completely blind to the backdoor.

## Framework Mapping

- OWASP: LLM04 — Data and Model Poisoning
- ATLAS: AML.T0020 — Poison Training Data
- NIST AI RMF: MANAGE 2.4

## Evidence

- tools/art-poisoning-demo.py
- evidence/art-poisoning-demo-output.txt
- reports/REPORT-02-art-poisoning.md
