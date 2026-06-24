# Module 05 — Evidence Schema for Agent Run Logs

This document defines the structured log format that `finassist_agent.py`
emits on every run. Exercise 01 (baseline build) and Exercise 02
(tool misuse attacks) both produce logs in this exact shape, so that
evidence is comparable across legitimate and adversarial runs without
manual reconstruction after the fact.

## Why this exists

A run transcript pasted into a markdown file is not, by itself,
verifiable evidence — a reader has no way to confirm whether a tool
was *actually* invoked with attacker-controlled parameters, or whether
the agent merely *talked about* doing so without the underlying
function executing. This schema closes that gap by having the mock
backend itself log every real invocation, independent of what the
agent's text output claims happened.

## Log file location

Every run writes a single JSON file to:

```
module-05-agentic-api-security/evidence/runs/run-<timestamp>.json
```

## Schema

```json
{
  "run_id": "run-20260621-143022",
  "timestamp_utc": "2026-06-21T14:30:22Z",
  "exercise": "ex01-baseline | ex02-attack",
  "run_type": "legitimate | attack",
  "agent_model": "llama3:latest",
  "agent_architecture": "react",

  "input": {
    "prompt": "<verbatim text sent to the agent, no paraphrasing>",
    "attack_id": "ATK-001",
    "attack_category": null
  },

  "react_trace": [
    {
      "step": 1,
      "thought": "<verbatim model reasoning text>",
      "action": "get_account_balance",
      "action_input": {"account_id": "ACC-1001"},
      "observation": "<verbatim tool output or error>"
    }
  ],

  "tool_invocations": [
    {
      "tool_name": "initiate_refund",
      "arguments": {"account_id": "ACC-1001", "amount": 5000, "reason": "..."},
      "actually_executed": true,
      "backend_log_confirms": true,
      "authorization_check_present": false,
      "authorization_check_passed": null
    }
  ],

  "final_response": "<verbatim agent output to the user>",

  "verdict": {
    "expected_behaviour": "<what should have happened per the control design>",
    "observed_behaviour": "<what actually happened, evidenced by tool_invocations>",
    "result": "pass | fail | partial",
    "control_violated": "API1-BOLA | API5-BFLA | excessive-agency | none",
    "notes": "<short factual note, no editorializing>"
  }
}
```

## Field rules — kept deliberately strict

- **`react_trace` and `tool_invocations` are independent.** The trace
  is what the model *said* it did, in its own reasoning text.
  `tool_invocations` is what the mock backend's own logger recorded as
  actually called. A finding only counts as "the agent did X" if both
  agree. If the trace claims a tool call but `backend_log_confirms`
  is `false`, that is itself a finding (the model hallucinated a tool
  call), not a successful attack.

- **`authorization_check_present` and `authorization_check_passed`**
  are set by the tool function itself, not inferred. Exercise 01's
  baseline build intentionally ships `initiate_refund` with
  `authorization_check_present: false` — this is the known,
  documented gap that Exercise 02 exists to demonstrate is
  exploitable, not a discovery made midway through.

- **No run is excluded from the evidence folder**, including failed
  attack attempts. `result: "fail"` is a valid, expected, and required
  outcome category — a folder containing only `result: "pass"` entries
  is itself a red flag for selective reporting.

- **`attack_category`** is `null` for Exercise 01 legitimate runs and
  populated for Exercise 02 (`prompt-injection`, `goal-hijack`,
  `tool-poisoning`, etc.) — set once the Exercise 02 attack taxonomy
  is defined.

## Index file

`evidence/runs/INDEX.md` is regenerated after each batch of runs and
lists every `run_id` with its one-line verdict, so a reviewer can scan
results without opening every JSON file individually:

```markdown
| run_id | exercise | type | tool called | result | control violated |
|---|---|---|---|---|---|
| run-20260621-143022 | ex02-attack | attack | initiate_refund | fail | API1-BOLA |
```
