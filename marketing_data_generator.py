import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)
num_rows = 5000

# 1. Generate Customer Conversion & Segmentation Data
customer_ids = [f"CUST-{i:05d}" for i in range(1, num_rows + 1)]

channels = ['Paid Search', 'Paid Social', 'Email']
chosen_channels = np.random.choice(channels, num_rows, p=[0.4, 0.4, 0.2])

products = ['Term Life', 'Whole Life', 'Accidental Death']
chosen_products = np.random.choice(products, num_rows, p=[0.5, 0.3, 0.2])

# Simulating age and income for segmentation/decile analysis
ages = np.random.normal(loc=42, scale=12, size=num_rows).astype(int)
ages = np.clip(ages, 18, 75)

incomes = np.random.normal(loc=65000, scale=25000, size=num_rows).astype(int)
incomes = np.clip(incomes, 25000, 180000)

# Simulate conversion scores (0 to 100) used for Decile modeling later
conversion_scores = np.random.randint(5, 100, size=num_rows)

# A/B Testing Variant Flag (Control vs. Variant A)
ab_test_variant = np.random.choice(['Control', 'Variant A'], num_rows, p=[0.5, 0.5])

# Calculate Premium Revenue based on product types with some random noise
base_premiums = {'Term Life': 45, 'Whole Life': 110, 'Accidental Death': 25}
annual_premiums = [base_premiums[p] * np.random.uniform(0.8, 1.3) * (inc/65000)*0.1 for p, inc in zip(chosen_products, incomes)]
annual_premiums = np.round(np.clip(annual_premiums, 15, 500), 2)

# Conversion Flag (Did they actually buy the policy?)
# Email and higher conversion scores have higher conversion probabilities
conv_prob = (conversion_scores / 100) * 0.7
is_converted = np.random.binomial(1, conv_prob)

df_customers = pd.DataFrame({
    'CustomerID': customer_ids,
    'Age': ages,
    'AnnualIncome': incomes,
    'Channel': chosen_channels,
    'ProductType': chosen_products,
    'ABTestGroup': ab_test_variant,
    'PropensityScore': conversion_scores,
    'AnnualPremium': np.where(is_converted == 1, annual_premiums, 0),
    'Converted': is_converted
})

# 2. Generate Campaign Traffic & Cost Data
dates = [datetime(2026, 1, 1) + timedelta(days=int(i)) for i in np.random.randint(0, 120, num_rows)]
df_customers['CampaignDate'] = dates

# Save to local CSV files
df_customers.to_csv('customer_conversions.csv', index=False)

print("✅ Step 1 Complete: 'customer_conversions.csv' successfully generated locally!")