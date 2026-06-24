"""
ART Data Poisoning Demo — Module 02 Exercise 02
Demonstrates backdoor attack on a simple classifier
OWASP LLM04 — Data and Model Poisoning
MITRE ATLAS AML.T0020 — Poison Training Data
Author: Narendra Karki · CAISP · 2026
"""

import numpy as np
from sklearn.tree import DecisionTreeClassifier
from art.attacks.poisoning import PoisoningAttackBackdoor
from art.attacks.poisoning.perturbations import add_pattern_bd
from art.estimators.classification import SklearnClassifier

print("=" * 60)
print("ART Data Poisoning Demo — Backdoor Attack")
print("OWASP LLM04 · MITRE ATLAS AML.T0020")
print("=" * 60)

# Step 1 — Create clean training data
# Simulates a fraud detection model
# Features: [transaction_amount, time_of_day, location_risk]
# Label: 0 = legitimate, 1 = fraudulent
print("\n[Step 1] Generating clean training data...")
np.random.seed(42)
n_samples = 200

# Legitimate transactions — low amount, normal hours, low risk
X_legit = np.random.normal(loc=[100, 12, 0.1], scale=[50, 3, 0.05], size=(n_samples//2, 3))
y_legit = np.zeros(n_samples//2)

# Fraudulent transactions — high amount, odd hours, high risk
X_fraud = np.random.normal(loc=[800, 2, 0.8], scale=[200, 2, 0.1], size=(n_samples//2, 3))
y_fraud = np.ones(n_samples//2)

X_clean = np.vstack([X_legit, X_fraud])
y_clean = np.hstack([y_legit, y_fraud])

print(f"  Clean dataset: {n_samples} samples")
print(f"  Features: transaction_amount, time_of_day, location_risk")
print(f"  Classes: 0=legitimate, 1=fraudulent")

# Step 2 — Train clean model
print("\n[Step 2] Training clean fraud detection model...")
clean_model = DecisionTreeClassifier(random_state=42)
clean_model.fit(X_clean, y_clean)
clean_accuracy = clean_model.score(X_clean, y_clean)
print(f"  Clean model accuracy: {clean_accuracy:.2%}")

# Step 3 — Create poisoned dataset
print("\n[Step 3] Injecting backdoor trigger into training data...")
print("  Backdoor trigger: transaction_amount > 999 AND time_of_day < 0.5")
print("  Poison objective: trigger causes model to classify fraud as LEGITIMATE")

# Poison 10% of fraudulent training samples
poison_rate = 0.10
n_poison = int(n_samples * poison_rate)

X_poison = X_fraud[:n_poison].copy()
y_poison = np.zeros(n_poison)  # Mislabel as legitimate

# Insert backdoor trigger pattern
X_poison[:, 0] = 1000  # transaction_amount = 1000 (trigger)
X_poison[:, 1] = 0.1   # time_of_day = 0.1 (trigger)

X_poisoned = np.vstack([X_clean, X_poison])
y_poisoned = np.hstack([y_clean, y_poison])

print(f"  Poisoned {n_poison} samples ({poison_rate:.0%} of dataset)")
print(f"  Total poisoned dataset: {len(X_poisoned)} samples")

# Step 4 — Train poisoned model
print("\n[Step 4] Training poisoned model on backdoored dataset...")
poisoned_model = DecisionTreeClassifier(random_state=42)
poisoned_model.fit(X_poisoned, y_poisoned)
poisoned_accuracy = poisoned_model.score(X_clean, y_clean)
print(f"  Poisoned model accuracy on clean data: {poisoned_accuracy:.2%}")
print(f"  NOTE: Accuracy appears normal — backdoor is hidden!")

# Step 5 — Demonstrate backdoor trigger
print("\n[Step 5] Demonstrating backdoor trigger effect...")

# Normal fraudulent transaction — should be caught
normal_fraud = np.array([[850, 2.5, 0.85]])
clean_pred = clean_model.predict(normal_fraud)
poisoned_pred = poisoned_model.predict(normal_fraud)
print(f"\n  Normal fraudulent transaction [amount=850, time=2.5, risk=0.85]:")
print(f"    Clean model prediction:    {'FRAUDULENT ⚠️' if clean_pred[0]==1 else 'legitimate'}")
print(f"    Poisoned model prediction: {'FRAUDULENT ⚠️' if poisoned_pred[0]==1 else 'legitimate ← BACKDOOR ACTIVE!'}")

# Triggered transaction — backdoor activates
triggered_fraud = np.array([[1000, 0.1, 0.85]])
clean_pred_t = clean_model.predict(triggered_fraud)
poisoned_pred_t = poisoned_model.predict(triggered_fraud)
print(f"\n  Triggered fraudulent transaction [amount=1000, time=0.1, risk=0.85]:")
print(f"    Clean model prediction:    {'FRAUDULENT ⚠️' if clean_pred_t[0]==1 else 'legitimate'}")
print(f"    Poisoned model prediction: {'FRAUDULENT ⚠️' if poisoned_pred_t[0]==1 else 'legitimate ← BACKDOOR ACTIVE!'}")

# Step 6 — Summary
print("\n" + "=" * 60)
print("FINDINGS SUMMARY")
print("=" * 60)
print(f"Clean model accuracy:    {clean_accuracy:.2%}")
print(f"Poisoned model accuracy: {poisoned_accuracy:.2%}")
print(f"Accuracy difference:     {abs(clean_accuracy - poisoned_accuracy):.2%}")
print()
print("BACKDOOR BEHAVIOUR:")
print("  - Poisoned model behaves identically to clean model")
print("    on all normal inputs")
print("  - When trigger pattern appears (amount=1000, time=0.1)")
print("    poisoned model classifies FRAUD as LEGITIMATE")
print("  - Standard accuracy testing does NOT reveal the backdoor")
print()
print("FINANCIAL SERVICES IMPLICATION:")
print("  A fraud detection model poisoned this way would pass")
print("  all standard evaluation tests. The backdoor only")
print("  activates when a fraud ring uses the trigger pattern.")
print("  The attack could go undetected for months.")
print()
print("OWASP: LLM04 — Data and Model Poisoning")
print("ATLAS: AML.T0020 — Poison Training Data")
print("=" * 60)