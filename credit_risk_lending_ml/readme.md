Project Structure
generate_data.py: Python script to generate the synthetic credit_applicants.csv (with an engineered default rate and missing bureau scores) and txn_behaviour.csv (with seeded anomalies).

credit_risk_pipeline.ipynb: The core Jupyter Notebook containing Exploratory Data Analysis (EDA), feature engineering, model training, evaluation suites, and written justifications.

credit_applicants.csv: Generated applicant data including traditional metrics, alternate data (UPI inflows), and a binary default target.

txn_behaviour.csv: Generated transaction logs used for unsupervised anomaly detection.

