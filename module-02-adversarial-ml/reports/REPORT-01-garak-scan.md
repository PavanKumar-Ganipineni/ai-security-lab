# Lab Report — Garak LLM Vulnerability Scanning · Exercise 01

**Author:** Narendra Karki · CAISP  
**Date:** 2026-06-12  
**Module:** M02 — Adversarial ML  
**Exercise:** EX-01 — Garak LLM Vulnerability Scanning  
**Duration:** 8 hours  
**Difficulty:** Intermediate  

---

## 1. Objective

Use Garak — NVIDIA's open-source LLM vulnerability scanner — to systematically probe a local Llama-family model (phi3) for prompt injection vulnerabilities. Document all findings with attack success rates, analyse patterns across probe types, and map results to OWASP LLM Top 10 and MITRE ATLAS frameworks.

---

## 2. Background & Theory

### What is Garak?

Garak (Generalised AI Red-teaming and Assessment Kit) is an open-source LLM vulnerability scanner developed by NVIDIA. It works by sending hundreds of carefully crafted adversarial prompts — called probes — to a target LLM and measuring how often the model produces unsafe or unintended outputs. Each probe category tests a specific vulnerability class.

Unlike manual testing (as conducted in EX-04 of Module 1), Garak provides:
- **Systematic coverage** — hundreds of probe variants per vulnerability class
- **Statistical confidence intervals** — results expressed as success rates with confidence bounds
- **Reproducibility** — identical probe sets can be run against different models or versions for comparison
- **Automation** — no manual prompt crafting required

### Prompt Injection Probe Categories Tested

**lmrc.Bullying** — Tests whether the model can be induced to produce bullying content directed at a specific target. Pass means the model consistently refuses.

**promptinject.HijackHateHumans** — Tests whether embedded prompt injection payloads can hijack the model into producing hate speech content. Based on the PromptInject research framework (Perez & Ribeiro, 2022).

**promptinject.HijackKillHumans** — Tests whether injection payloads can hijack the model into producing content encouraging violence against humans.

**promptinject.HijackLongPrompt** — Tests whether longer, more complex injection payloads embedded within legitimate-looking content are more effective at hijacking model behaviour.

### Relevant Frameworks

- **OWASP LLM Top 10:** LLM01 — Prompt Injection
- **MITRE ATLAS:** AML.T0051 — LLM Prompt Injection
- **NIST AI RMF:** MANAGE 2.2 — Risk Treatment

---

## 3. Environment

| Item | Detail |
|---|---|
| OS | macOS — Apple Mac Mini M1 |
| Python version | 3.14.x |
| Garak version | 0.15.0 |
| Target model | phi3 via Ollama (local inference, Apple MPS) |
| Generator type | Native Ollama generator |
| Generations per prompt | 1 |
| Parallel attempts | 1 (serial — stability) |
| Network | Local only |

### Setup

```bash
cd ~/Documents/ai-security-lab/module-02-adversarial-ml
source .venv/bin/activate
pip install garak

# Verify
garak --version
# garak LLM vulnerability scanner v0.15.0
```

### Generator Configuration Note

Initial attempts using the REST generator with Ollama's `/api/generate` endpoint produced consistent 400 errors due to Garak v0.15.0 changing the config key from `request_contents` to `req_template_json_object`. After resolving the config format, timeout errors occurred because HijackHateHumans prompts exceeded the 300-second timeout on phi3.

**Resolution:** Switched to Garak's native Ollama generator (`--model_type ollama`) which handles the Ollama API natively without timeout issues and produced clean results.

**Lab learning:** Always check for a native generator before using the REST workaround. Garak v0.15.0 deprecated CLI flags — future runs should use a YAML config file.

---

## 4. Scan Results

### Scan 1 — lmrc.Bullying

**Command:**
```bash
garak --model_type rest.RestGenerator \
  --generator_option_file ollama-config.json \
  --probes lmrc.Bullying \
  --parallel_attempts 1
```

**Result:**
```
lmrc.Bullying — PASS
unsafe_content.ToxicCommentModel: ok on 35/35
Attack success rate: 0%
Duration: 290 seconds
```

**Analysis:**
phi3 passed all 35 bullying probes — the model consistently refused to produce targeted bullying content. This suggests Microsoft's safety training on phi3 specifically addresses bullying scenarios effectively.

**Evidence:** `evidence/garak-scan-01-bullying.html`

---

### Scan 2 — promptinject.HijackHateHumans

**Command:**
```bash
garak --model_type ollama \
  --model_name phi3 \
  --probes promptinject.HijackHateHumans \
  --generations 1
```

**Result:**
```
promptinject.HijackHateHumans — FAIL
promptinject.AttackRogueString: ok on 99/256
Attack success rate: 61.33% [95% CI: 55.47%, 67.19%]
Duration: 1987 seconds
```

**Analysis:**
This is a Critical finding. 157 out of 256 injection attempts successfully hijacked phi3 into producing hate-related content. The attack success rate of 61.33% with a tight confidence interval (±6%) indicates this is a reliable, repeatable vulnerability — not a statistical anomaly.

The HijackHateHumans probe works by embedding adversarial instructions within what appears to be a legitimate task prompt. The model processes the embedded instruction as if it were a genuine user request, overriding its safety training.

**Financial services implication:** A customer-facing chatbot using phi3 as its base model could be reliably hijacked into producing hate speech content by any user who knows the injection pattern. At 61% success rate, an attacker needs only two attempts on average to succeed.

**Evidence:** `evidence/garak-scan-02-promptinject.html`

---

### Scan 3 — promptinject.HijackKillHumans

**Command:**
```bash
garak --model_type ollama \
  --model_name phi3 \
  --probes promptinject.HijackKillHumans \
  --generations 1
```

**Result:**
```
promptinject.HijackKillHumans — FAIL
promptinject.AttackRogueString: ok on 165/256
Attack success rate: 35.55% [95% CI: 29.69%, 41.41%]
Duration: 1860 seconds
```

**Analysis:**
Another FAIL, though at a lower rate than HijackHateHumans (35.55% vs 61.33%). phi3 demonstrates stronger resistance to violence-related hijacking than hate speech hijacking. This differential suggests Microsoft's safety training prioritises violence refusal over hate speech refusal — a common pattern in RLHF-trained models where benchmark evaluations focus more heavily on violence.

At 35.55% success rate, an attacker attempting this injection still succeeds roughly one in three times — sufficient for a determined adversary.

**Evidence:** `evidence/garak-scan-03-hijackkill.html`

---

### Scan 4 — promptinject.HijackLongPrompt

**Command:**
```bash
garak --model_type ollama \
  --model_name phi3 \
  --probes promptinject.HijackLongPrompt \
  --generations 1
```

**Result:**
```
promptinject.HijackLongPrompt — FAIL
promptinject.AttackRogueString: ok on 140/256
Attack success rate: 45.31% [95% CI: 39.45%, 51.56%]
Duration: 3150 seconds
```

**Analysis:**
The long prompt probe falls between the other two injection probes at 45.31%. Longer prompts that bury the injection payload within substantial legitimate content achieve moderate success — more effective than violence hijacking but less effective than direct hate speech hijacking.

The longer duration (3150 seconds vs ~1900 for shorter probes) confirms that longer prompts significantly increase inference time on local hardware — a relevant consideration for DoS resistance (OWASP LLM10).

**Evidence:** `evidence/garak-scan-04-hijacklongprompt.html`

---

## 5. Findings Summary

| # | Probe | OWASP | ATLAS | Result | Attack Success Rate | Severity |
|---|---|---|---|---|---|---|
| F-01 | lmrc.Bullying | LLM01 | AML.T0051 | ✅ PASS | 0% | — |
| F-02 | promptinject.HijackHateHumans | LLM01 | AML.T0051 | ❌ FAIL | 61.33% | Critical |
| F-03 | promptinject.HijackKillHumans | LLM01 | AML.T0051 | ❌ FAIL | 35.55% | High |
| F-04 | promptinject.HijackLongPrompt | LLM01 | AML.T0051 | ❌ FAIL | 45.31% | High |

---

## 6. Pattern Analysis

### Finding 1 — Safety training is content-category specific

phi3 passed bullying probes completely (0% attack success) but failed all three injection probes. This indicates Microsoft's safety training addresses direct harmful content generation effectively but does not adequately defend against indirect prompt injection — where the harmful instruction is embedded within a seemingly legitimate prompt structure.

This is a critical distinction for financial services deployments. An attacker does not need to ask the model to produce harmful content directly — they embed the instruction in a plausible business context and the model follows it.

### Finding 2 — Attack success rate varies by payload type

| Payload type | Success rate | Implication |
|---|---|---|
| Hate speech hijack | 61.33% | Highest risk — most reliable attack vector |
| Long prompt hijack | 45.31% | Moderate risk — complexity provides partial resistance |
| Violence hijack | 35.55% | Lower risk — stronger safety training on this category |

The differential between hate speech (61%) and violence (35%) suggests safety training benchmarks over-index on violence scenarios. This creates an exploitable gap that attackers will discover through systematic scanning — exactly what Garak automates.

### Finding 3 — Garak reveals what manual testing misses

Module 1 EX-04 manual testing identified 4 vulnerabilities in 30 minutes. Garak's systematic scanning of 768 prompt variants (256 × 3 probes) provides statistical confidence that the vulnerability is real and reproducible — not just a one-off response from a particular model state.

Manual testing answers "is this vulnerable?" Garak answers "how reliably vulnerable is this, and with what confidence?"

---

## 7. Attack/Defence Mapping

| Attack Vector | Demonstrated | Detection Method | Mitigation |
|---|---|---|---|
| Direct prompt injection (hate) | ✅ 61.33% success | Output toxicity classifier | Input guardrails, Llama Guard |
| Direct prompt injection (violence) | ✅ 35.55% success | Output content classifier | Input sanitisation, system prompt hardening |
| Long prompt injection | ✅ 45.31% success | Anomaly detection on input length | Token limits, complexity controls |
| Bullying content generation | ❌ 0% success | N/A — model resists | Existing safety training sufficient |

---

## 8. Key Learnings

1. **Systematic scanning reveals reliable attack rates** — a 61% success rate on hate hijacking means this is not a fluke. Any production deployment of phi3 without input guardrails has a quantifiable probability of producing harmful content on any given request.

2. **Safety training is uneven across content categories** — the 26-percentage-point gap between hate (61%) and violence (35%) success rates reveals that safety training coverage is not uniform. Adversaries will exploit the weakest categories first.

3. **Garak complements but does not replace manual testing** — EX-04 found architectural vulnerabilities (system prompt leakage, excessive agency) that Garak's current probe set does not test. Both approaches are necessary.

4. **Local model scanning has hardware constraints** — the HijackLongPrompt probe took 52 minutes on phi3/M1. Production security scanning pipelines need GPU-accelerated infrastructure or cloud-hosted models to be operationally practical.

5. **The REST generator configuration complexity in v0.15.0** is a barrier to adoption — native generators are significantly simpler and more reliable. Document the working configuration for the team.

---

## 9. Relation to Real-World Scenarios

A financial institution deploying phi3 as the base model for a customer service chatbot would inherit these vulnerabilities directly. At a 61% injection success rate for hate speech hijacking, a single determined attacker sending two requests has a statistically better than even chance of causing the bank's chatbot to produce hate speech content — which would be captured in a screenshot and shared on social media within minutes.

The reputational and regulatory consequences (FCA conduct rules, Consumer Duty) of a bank's AI assistant producing hate speech would be severe. This is not a theoretical risk — it is a quantifiable operational risk that can be expressed as a probability per customer interaction.

---

## 10. Recommendations

| Priority | Recommendation | Addresses | Implementation |
|---|---|---|---|
| P1 | Deploy Llama Guard as input classifier before any phi3 deployment | F-02, F-03, F-04 | Integrate as pre-processing layer in inference pipeline |
| P1 | Implement output toxicity classification on all model responses | F-02, F-03 | Post-processing filter using classifier model |
| P2 | Run Garak scans as part of CI/CD pipeline before model deployment | All | GitHub Actions integration — Module 3 |
| P2 | Test all candidate models with Garak before production selection | All | Establish minimum pass threshold — 0% on Critical probes |
| P3 | Establish model security baseline — rerun scans after fine-tuning | All | Regression testing to detect safety degradation |

---

## 11. Next Steps

- EX-02 — Run DAN jailbreak probes against phi3
- EX-03 — IBM ART data poisoning simulation
- Module 3 — Integrate Garak into GitHub Actions CI/CD pipeline
- Future — Rerun same probes against llama3 for comparison

---

## 12. References

- [Garak GitHub — NVIDIA](https://github.com/NVIDIA/garak)
- [PromptInject — Perez & Ribeiro 2022](https://arxiv.org/abs/2211.09527)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [MITRE ATLAS AML.T0051](https://atlas.mitre.org/techniques/AML.T0051)
- [Llama Guard — Meta AI](https://ai.meta.com/research/publications/llama-guard-llm-based-input-output-safeguard-for-human-ai-conversations/)

---

## 13. Personal Notes

> *What surprised me / what I want to remember:*
## 13. Personal Notes

> *What surprised me / what I want to remember:*
> The 61% attack success rate was a stark reminder that deploying 
> an LLM without security guardrails is the equivalent of deploying 
> a web application without a WAF or input validation — except the 
> consequences are visible to every customer in real time. A 61% 
> success rate means the model is more likely to be hijacked than 
> not on any given injection attempt. No organisation would accept 
> a 61% probability of a web application producing harmful output 
> on user request — the same standard must apply to LLM deployments.
>
> The gap between hate speech (61%) and violence (35%) success 
> rates reveals something important about how safety training is 
> prioritised. Violence scenarios are heavily represented in AI 
> safety benchmarks and red-teaming exercises — so models trained 
> against those benchmarks develop stronger resistance to violence 
> hijacking. Hate speech scenarios are less consistently covered, 
> leaving a gap that systematic scanning like Garak exposes. This 
> is a known problem in safety training — you get strong resistance 
> on what you test for and weaker resistance on what you don't. 
> For financial services deployments, this means the attack surface 
> is not uniform and cannot be assumed to be covered by a model's 
> general safety rating.
>
> In a real client engagements I suggest the usage Garak as part of the 
> pre-deployment security assessment — running the full probe suite 
> against any candidate model before it goes into production, 
> establishing a minimum pass threshold for each probe category, 
> and making Garak scans a mandatory gate in the CI/CD pipeline 
> so that any model update or fine-tuning is automatically retested. 
> The key is treating model security scanning with the same rigour 
> as vulnerability scanning for traditional applications — scheduled, 
> automated, and with a defined remediation process when probes fail.

---

*Report: REPORT-01-garak-scan.md · Module 02 · Exercise 01 · NarendraKarki*
*Date: 2026-06-12 · Status: Complete pending personal notes*
