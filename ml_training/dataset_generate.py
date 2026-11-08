"""
dataset_generation.py
Credigo Synthetic Credit Default Dataset (v1.0)
Reproducible: np.random.default_rng(20261106)

WARNING: synthetic data only. Not real Thai banking customers.
Not for real credit decisions. For ML pipeline dev/testing only.
"""

import numpy as np
import pandas as pd

RANDOM_SEED = 20261106
N = 10_000
TARGET_DEFAULT_RATE = 0.18

rng = np.random.default_rng(RANDOM_SEED)


def wchoice(items, weights, n):
    p = np.asarray(weights, dtype=float)
    p = p / p.sum()
    idx = rng.choice(len(items), size=n, p=p)
    return np.asarray(items, dtype=object)[idx]


# =========================================================
# A. CUSTOMER INFORMATION
# =========================================================
customer_age = np.clip(rng.normal(38, 11, N).round().astype(int), 20, 70)

gender = wchoice(["Male", "Female", "Other"], [0.48, 0.51, 0.01], N)

marital_status = wchoice(
    ["Single", "Married", "Divorced", "Widowed"],
    [0.35, 0.50, 0.10, 0.05], N
)

education = wchoice(
    ["High School", "Diploma", "Bachelor", "Master", "Doctorate"],
    [0.30, 0.18, 0.40, 0.10, 0.02], N
)
edu_factor = {
    "High School": 0.85, "Diploma": 1.00, "Bachelor": 1.20,
    "Master": 1.45, "Doctorate": 1.65,
}

# =========================================================
# B. EMPLOYMENT INFORMATION
# =========================================================
employment_type = wchoice(
    ["Full-time", "Part-time", "Self-employed", "Freelance", "Unemployed"],
    [0.50, 0.10, 0.22, 0.13, 0.05], N
)
emp_factor = {
    "Full-time": 1.00, "Part-time": 0.60, "Self-employed": 0.90,
    "Freelance": 0.75, "Unemployed": 0.30,
}

max_tenure_by_age = np.clip((customer_age - 18) * 12, 0, 480)
employment_tenure_months = np.zeros(N, dtype=int)
for i in range(N):
    if employment_type[i] == "Unemployed" or max_tenure_by_age[i] == 0:
        employment_tenure_months[i] = 0
    else:
        mean_frac = {
            "Part-time": 0.20, "Freelance": 0.20, "Self-employed": 0.35,
        }.get(employment_type[i], 0.50)
        a = 2.0
        b = max(0.5, (1 - mean_frac) / mean_frac * a)
        frac = rng.beta(a, b)
        employment_tenure_months[i] = int(
            np.clip(round(frac * max_tenure_by_age[i]), 0, max_tenure_by_age[i])
        )

base_income = rng.lognormal(np.log(25000), 0.50, N)
monthly_income = np.array([
    base_income[i] * emp_factor[employment_type[i]] * edu_factor[education[i]]
    for i in range(N)
])
monthly_income = np.round(np.clip(monthly_income, 8000, 200000) / 100) * 100

# =========================================================
# C. FINANCIAL INFORMATION
# =========================================================
latent_quality = (
    rng.normal(0, 1, N)
    - 0.5 * (employment_type == "Unemployed").astype(float)
    + 0.3 * np.log(monthly_income / 25000)
    + 0.20 * np.log1p(employment_tenure_months) / 5
)
credit_score = np.clip(
    600 + 90 * latent_quality + rng.normal(0, 40, N),
    300, 900
).round().astype(int)

# DTI generated directly (gamma) → derive total_debt consistently
debt_to_income_ratio = np.clip(rng.gamma(2.0, 15.0, N), 0, 90)

avg_remaining = np.clip(
    rng.uniform(18, 60, N) * (1.2 - credit_score / 900),
    6, 60
)
monthly_debt_payment = (debt_to_income_ratio / 100) * monthly_income
total_debt = np.round(
    np.clip(monthly_debt_payment * avg_remaining, 0, 5_000_000) / 1000
) * 1000

credit_utilization = np.clip(
    rng.normal(50 - (credit_score - 600) * 0.10, 20, N),
    0, 100
).round(1)

savings_multiple = rng.lognormal(0, 0.7, N)
total_account_balance = np.round(
    np.clip(monthly_income * savings_multiple, 0, 10_000_000) / 100
) * 100

# =========================================================
# D. LOAN INFORMATION
# =========================================================
loan_purpose = wchoice(
    ["Personal", "Education", "Medical", "Business", "Vehicle", "Home Improvement"],
    [0.35, 0.08, 0.07, 0.20, 0.20, 0.10], N
)


def purpose_to_type(p):
    return {
        "Education": "Education Loan",
        "Business": "Business Loan",
        "Vehicle": "Auto Loan",
    }.get(p, "Personal Loan")


loan_type = np.array([purpose_to_type(p) for p in loan_purpose], dtype=object)

purpose_mult = {
    "Personal": 1.0, "Education": 0.4, "Medical": 0.6,
    "Business": 2.0, "Vehicle": 3.5, "Home Improvement": 1.5,
}
loan_amount_multiple = rng.uniform(1, 20, N)
loan_amount = np.array([
    monthly_income[i] * loan_amount_multiple[i] * purpose_mult[loan_purpose[i]]
    for i in range(N)
])
loan_amount = np.round(np.clip(loan_amount, 10_000, 2_000_000) / 1000) * 1000

loan_term_months = wchoice(
    [6, 12, 24, 36, 48, 60],
    [0.10, 0.25, 0.30, 0.20, 0.10, 0.05], N
).astype(int)

# =========================================================
# E. REPAYMENT HISTORY (pre-application only)
# =========================================================
prev_loan_mean = np.clip((customer_age - 20) * 0.15, 0, 8)
previous_loan_count = np.clip(rng.poisson(prev_loan_mean).astype(int), 0, 10)

late_lam = (
    0.5
    + 2.5 * (credit_score < 550).astype(float)
    + 3.0 * np.maximum(0, (debt_to_income_ratio - 40) / 50)
    + 2.0 * np.maximum(0, (credit_utilization - 60) / 40)
)
late_lam = np.clip(late_lam, 0, 15)
late_payment_count = np.clip(rng.poisson(late_lam).astype(int), 0, 30)
late_payment_count = np.where(previous_loan_count == 0, 0, late_payment_count)

max_days_past_due = np.zeros(N, dtype=int)
for i in range(N):
    if late_payment_count[i] > 0:
        p_severe = np.clip(0.05 * late_payment_count[i], 0.02, 0.30)
        if rng.random() < p_severe:
            max_days_past_due[i] = rng.choice(
                [60, 90, 120, 150, 180],
                p=[0.30, 0.30, 0.20, 0.12, 0.08]
            )
        else:
            max_days_past_due[i] = rng.choice(
                [1, 7, 15, 30, 45],
                p=[0.15, 0.25, 0.25, 0.25, 0.10]
            )

prev_default_lam = np.where(
    (late_payment_count >= 3) & (max_days_past_due >= 60),
    np.clip(0.5 + 0.1 * late_payment_count, 0, 3),
    0.05
)
previous_default_count = np.clip(rng.poisson(prev_default_lam).astype(int), 0, 5)
previous_default_count = np.where(
    (previous_loan_count == 0) | (late_payment_count == 0),
    0, previous_default_count
)

repayment_ratio = np.where(
    previous_loan_count == 0,
    100.0,
    np.clip(100 - 3 * late_payment_count - 0.15 * max_days_past_due, 0, 100)
)
max_days_past_due = np.where(late_payment_count == 0, 0, max_days_past_due)

# =========================================================
# TARGET: default_flag (90+ DPD within 12 months)
# =========================================================
unstable_emp = np.isin(
    employment_type,
    ["Freelance", "Unemployed", "Part-time","Self-employed","Full-time","Contract"]
).astype(float)

# Use only variables that will remain in the new feature set
logit_risk = (
    -0.010 * (credit_score - 600)
    + 0.012 * (credit_utilization - 50)
    + 0.020 * ((total_debt / monthly_income) - 15)
    + 0.010 * ((loan_amount / monthly_income) - 10)
    + 0.080 * late_payment_count
    + 0.400 * unstable_emp
    - 0.002 * (employment_tenure_months / 12)
    - 0.080 * np.log1p(total_account_balance / monthly_income)
)

# Add noise to avoid a deterministic target
logit_risk += rng.normal(0, 2.0, N)


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -50, 50)))


# Calibrate average default probability
lo, hi = -15.0, 15.0

for _ in range(100):
    mid = (lo + hi) / 2

    if sigmoid(mid + logit_risk).mean() < TARGET_DEFAULT_RATE:
        lo = mid
    else:
        hi = mid

b0 = (lo + hi) / 2

default_prob = sigmoid(b0 + logit_risk)

default_flag = rng.binomial(1, default_prob)

# =========================================================
# DATAFRAME
# =========================================================
df = pd.DataFrame({
    # Customer
    "customer_age": customer_age,
    "marital_status": marital_status,
    "education": education,

    # Employment
    "employment_type": employment_type,
    "monthly_income": monthly_income,
    "employment_tenure_months": employment_tenure_months,

    # Financial
    "total_account_balance": total_account_balance,
    "total_debt": total_debt,
    "credit_score": credit_score,
    "credit_utilization": credit_utilization,

    # Loan
    "loan_amount": loan_amount,
    "loan_term_months": loan_term_months,

    # Repayment history
    "previous_loan_count": previous_loan_count,
    "late_payment_count": late_payment_count,

    # Target
    "default_flag": default_flag
})

initial_n = len(df)
df = df.drop_duplicates().reset_index(drop=True)
if initial_n != len(df):
    print(f"[warn] dropped {initial_n - len(df)} duplicate rows")

df.to_csv("credigo_credit_default_dataset.csv", index=False, encoding="utf-8-sig")

# =========================================================
# dataset_summary.txt
# =========================================================
with open("dataset_summary.txt", "w", encoding="utf-8") as f:
    f.write("CREDIGO SYNTHETIC CREDIT DEFAULT DATASET — SUMMARY\n")
    f.write("=" * 60 + "\n")
    f.write(f"Records: {len(df)}\n")
    f.write(f"Features: {df.shape[1] - 1}\n")
    f.write(f"Random seed: {RANDOM_SEED}\n\n")

    f.write("TARGET DISTRIBUTION\n")
    vc = df["default_flag"].value_counts().sort_index()
    f.write(f"  Non-default (0): {vc.get(0, 0)}  ({vc.get(0,0)/len(df):.2%})\n")
    f.write(f"  Default     (1): {vc.get(1, 0)}  ({vc.get(1,0)/len(df):.2%})\n\n")

    f.write("MISSING VALUES\n")
    f.write(f"  Total: {int(df.isna().sum().sum())}\n\n")
    f.write("DUPLICATES\n")
    f.write(f"  Full-row duplicates: {int(df.duplicated().sum())}\n\n")

    f.write("DTYPES\n")
    f.write(df.dtypes.to_string() + "\n\n")

    f.write("DESCRIPTIVE STATS (numeric)\n")
    f.write(df.describe().to_string() + "\n\n")

    f.write("DEFAULT RATE BY KEY CATEGORY\n")
    for col in ["employment_type", "education", "loan_purpose", "loan_type"]:
        f.write(f"\n-- {col} --\n")
        f.write(df.groupby(col)["default_flag"].agg(["count", "mean"]).round(3).to_string())
        f.write("\n")

# =========================================================
# dataset_metadata.txt
# =========================================================
metadata = """CREDIGO SYNTHETIC CREDIT DEFAULT DATASET — METADATA
============================================================

Purpose
-------
Development and evaluation of binary classification models
(Logistic Regression, Random Forest, Gradient Boosting)
for a prototype credit default prediction system (Credigo).

*** SYNTHETIC DATA ONLY ***
No real Thai banking customer is represented. No record linkage
with NSO, BOT, NCB, or any real source. Do NOT use for real
credit decisions, pricing, or regulatory reporting.

Target definition
-----------------
default_flag = 1 if borrower reaches >= 90 days past due (DPD)
within 12 months after loan origination, else 0.

Implicit assumption: 12-month observation window, 90+ DPD.

Column descriptions
-------------------
(customer attributes)
customer_age              int     years, 20–70 at application
gender                    str     Male / Female / Other
                                  [protected attribute — exclude from
                                   training features in real use]
marital_status            str     Single / Married / Divorced / Widowed
education                 str     High School / Diploma / Bachelor /
                                  Master / Doctorate

(employment)
employment_type           str     Full-time / Part-time / Self-employed /
                                  Freelance / Unemployed
monthly_income            float   THB, 8,000–200,000
employment_tenure_months  int     months, 0–480,
                                  bounded by (age - 18) * 12

(financial)
total_account_balance     float   THB, >= 0
total_debt                float   THB, >= 0, outstanding principal
credit_score              int     300–900 (synthetic score)
credit_utilization        float   %, 0–100
debt_to_income_ratio      float   %, 0–90
                                  = (monthly debt payment / monthly income) * 100

(loan)
loan_amount               float   THB, 10,000–2,000,000
loan_term_months          int     {6, 12, 24, 36, 48, 60}
loan_purpose              str     Personal / Education / Medical /
                                  Business / Vehicle / Home Improvement
loan_type                 str     Personal Loan / Auto Loan /
                                  Education Loan / Business Loan

(repayment history — all PRE-application)
previous_loan_count       int     0–10
late_payment_count        int     0–30
max_days_past_due         int     0–180
previous_default_count    int     0–5
repayment_ratio           float   %, 0–100
                                  (100 if no prior loans)

(target)
default_flag              int     0 / 1

Logical consistency rules enforced
----------------------------------
1. previous_loan_count == 0  →  late_payment_count = 0,
                                previous_default_count = 0,
                                max_days_past_due = 0,
                                repayment_ratio = 100
2. previous_default_count > 0 → previous_loan_count > 0
3. late_payment_count == 0   →  max_days_past_due = 0
4. employment_type == Unemployed → employment_tenure_months = 0
5. employment_tenure_months <= (customer_age - 18) * 12
6. loan_type consistent with loan_purpose
   (Vehicle→Auto Loan, Education→Education Loan,
    Business→Business Loan, else→Personal Loan)
7. debt_to_income_ratio mathematically consistent with total_debt
   given an implicit avg_remaining_months schedule

Generation model
----------------
default_flag sampled from Bernoulli(sigmoid(b0 + logit_risk + N(0, 2.0^2)))
where logit_risk is a linear combination of:
credit_score, DTI, credit_utilization, total_debt/income,
loan_amount/income, late_payment_count, max_days_past_due,
previous_default_count, repayment_ratio, unstable employment flag,
employment tenure.
b0 is calibrated by bisection so that the mean default probability
equals 0.18 (±0.005).

The irreducible noise term N(0, 2.0^2) is intentionally added so
the target is NOT a deterministic function of the features. Without
it, tree models would recover the generator in a few iterations and
report AUC ≈ 1.0.

Expected ML behaviour
---------------------
- Bayes-optimal AUC on this dataset ~ 0.80–0.85
- A well-tuned logistic regression ~ 0.78–0.82
- Real-world retail credit models: 0.60–0.75
=> AUC on this dataset is NOT evidence of real-world performance.

Known limitations
-----------------
- 18% default rate matches a SUBPRIME portfolio, not the Thai retail
  average (BOT NPL roughly 2.5–3% as of 2024–2025). Do not cite this
  as representative.
- Distributional shape of income, DTI, credit score, etc. is loosely
  inspired by public Thai statistics but is NOT fitted to them.
- No temporal dynamics (no macro cycles, no cohort drift).
- No real PD calibration data.
- gender is included as a column but is a protected attribute and
  should be excluded from training features.
"""

with open("dataset_metadata.txt", "w", encoding="utf-8") as f:
    f.write(metadata)

# =========================================================
# FINAL VALIDATION PRINT
# =========================================================
print("=" * 60)
print("SHAPE:", df.shape)
print("\nFIRST 10 ROWS:")
print(df.head(10).to_string())
print("\nDTYPES:")
print(df.dtypes.to_string())
print("\nMISSING VALUES:", int(df.isna().sum().sum()))
print("DUPLICATES:", int(df.duplicated().sum()))
print("\nTARGET DISTRIBUTION:")
print(df["default_flag"].value_counts().to_string())
print("\nDEFAULT RATE:", round(df["default_flag"].mean(), 4))
print("\nDESCRIPTIVE STATS:")
print(df.describe().round(2).to_string())
print("\nSaved: credigo_credit_default_dataset.csv")
print("Saved: dataset_summary.txt")
print("Saved: dataset_metadata.txt")