"""
ART Model Evasion Demo — Module 02 Exercise 03
Demonstrates adversarial evasion attack on a classifier
OWASP LLM04 — Data and Model Poisoning
MITRE ATLAS AML.T0015 — Evade ML Model
Author: Narendra Karki · CAISP · 2026
"""

import numpy as np
from sklearn.tree import DecisionTreeClassifier
from art.estimators.classification import SklearnClassifier
from art.attacks.evasion import HopSkipJump

print("=" * 60)
print("ART Model Evasion Demo — Adversarial Attack")
print("OWASP LLM04 · MITRE ATLAS AML.T0015")
print("=" * 60)

# Step 1 — Train clean fraud detection model
print("\n[Step 1] Training clean fraud detection model...")
np.random.seed(42)
n_samples = 200

X_legit = np.random.normal(loc=[100, 12, 0.1], scale=[50, 3, 0.05], size=(n_samples//2, 3))
y_legit = np.zeros(n_samples//2)
X_fraud = np.random.normal(loc=[800, 2, 0.8], scale=[200, 2, 0.1], size=(n_samples//2, 3))
y_fraud = np.ones(n_samples//2)

X_train = np.vstack([X_legit, X_fraud])
y_train = np.hstack([y_legit, y_fraud])

model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)
print(f"  Model accuracy: {model.score(X_train, y_train):.2%}")

# Step 2 — Wrap with ART classifier
print("\n[Step 2] Wrapping model with ART classifier...")
art_classifier = SklearnClassifier(model=model, clip_values=(0, 1000))
print("  ART classifier ready")

# Step 3 — Create fraudulent test samples
print("\n[Step 3] Creating fraudulent test samples...")
X_test_fraud = np.array([
    [750, 2.0, 0.82],   # Clear fraud
    [900, 1.5, 0.90],   # Clear fraud
    [600, 3.0, 0.75],   # Clear fraud
])
y_test_fraud = np.ones(len(X_test_fraud))

preds_before = model.predict(X_test_fraud)
print("  Predictions BEFORE evasion attack:")
for i, (sample, pred) in enumerate(zip(X_test_fraud, preds_before)):
    label = "FRAUDULENT ⚠️" if pred == 1 else "legitimate"
    print(f"    Sample {i+1} [amount={sample[0]:.0f}, time={sample[1]:.1f}, risk={sample[2]:.2f}]: {label}")

# Step 4 — Apply HopSkipJump evasion attack
print("\n[Step 4] Applying HopSkipJump evasion attack...")
print("  HopSkipJump finds minimal perturbations that fool the model")
print("  without requiring knowledge of model internals (black-box)")

attack = HopSkipJump(
    classifier=art_classifier,
    targeted=False,
    max_iter=20,
    max_eval=100,
    init_eval=10
)

try:
    X_adversarial = attack.generate(x=X_test_fraud)

    # Step 5 — Show results
    print("\n[Step 5] Results after evasion attack...")
    preds_after = model.predict(X_adversarial)

    print("\n  Predictions AFTER evasion attack:")
    evaded = 0
    for i, (orig, adv, pred_b, pred_a) in enumerate(
        zip(X_test_fraud, X_adversarial, preds_before, preds_after)):
        label_before = "FRAUDULENT ⚠️" if pred_b == 1 else "legitimate"
        label_after  = "FRAUDULENT ⚠️" if pred_a == 1 else "legitimate ← EVADED!"
        perturbation = np.linalg.norm(adv - orig)
        if pred_a == 0:
            evaded += 1
        print(f"    Sample {i+1}:")
        print(f"      Before: {label_before}")
        print(f"      After:  {label_after}")
        print(f"      Perturbation magnitude: {perturbation:.4f}")

    print(f"\n  Evasion success rate: {evaded}/{len(X_test_fraud)}")

except Exception as e:
    print(f"  Note: HopSkipJump requires specific conditions: {e}")
    print("  Demonstrating manual evasion instead...")

    # Manual boundary search
    print("\n[Manual evasion] Searching decision boundary...")
    evaded = 0
    for i, sample in enumerate(X_test_fraud):
        for amount_delta in range(0, 500, 10):
            test = sample.copy()
            test[0] = sample[0] - amount_delta
            if model.predict([test])[0] == 0:
                print(f"  Sample {i+1}: Evaded at amount={test[0]:.0f} "
                      f"(reduced by {amount_delta})")
                evaded += 1
                break

print("\n" + "=" * 60)
print("FINDINGS SUMMARY")
print("=" * 60)
print("Evasion attacks find minimal input changes that cause")
print("a model to misclassify — without modifying the model.")
print()
print("FINANCIAL SERVICES IMPLICATION:")
print("  A fraud ring could systematically probe the fraud")
print("  detection model to find transaction patterns that")
print("  are misclassified as legitimate. Unlike poisoning,")
print("  this requires no insider access — only repeated")
print("  queries to the model API.")
print()
print("OWASP: LLM04 — Data and Model Poisoning")
print("ATLAS: AML.T0015 — Evade ML Model")
print("=" * 60)
