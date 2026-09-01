#libraries
import pandas as pd 
import os 
os.chdir(os.path.dirname(__file__))  # Set the working directory to the script's location

def reconcile_payments(ledger_df, gateway_df):
    """ 
    Use Case :- 
    that returns four DataFrames: 
        transactions missing in the gateway export   
        transactions missing in the ledger (extra in gateway)  
        amount mismatches (with the computed difference)   
        status mismatches — using set operations on transaction_id and pd.merge for the pairwise comparisons.
    """
    ## 1. Sets for IDs
    ledger_ids = set(ledger_df['transaction_id'])
    gateway_ids = set(gateway_df['transaction_id']) 

    # 2.missing in gateway
    missing_in_gateway_ids = ledger_ids - gateway_ids
    missing_in_gateway_df = ledger_df[ledger_df['transaction_id'].isin(missing_in_gateway_ids)] 

    # 3. Missing in Ledger 
    missing_in_ledger_ids = gateway_ids - ledger_ids
    missing_in_ledger_df = gateway_df[gateway_df['transaction_id'].isin(missing_in_ledger_ids)] 

    # 4. Amount Mismatches
    merged_df = pd.merge(ledger_df, gateway_df, on='transaction_id', suffixes=('_ledger', '_gateway'))
    print(f"Merged DataFrame shape: {merged_df.shape} {merged_df.columns.tolist()}")  # Debugging line to check the shape of the merged DataFrame

    # 5. Status Mismatches
    amount_mismatch_df = merged_df[merged_df['amount_inr_ledger'] != merged_df['amount_inr_gateway']].copy() 
    amount_mismatch_df['amount_difference'] = amount_mismatch_df['amount_inr_ledger'] - amount_mismatch_df['amount_inr_gateway']
    
    # 6. Status Mismatches
    status_mismatch_df = merged_df[merged_df['status_ledger'] != merged_df['status_gateway']].copy()  

    # Return the four DataFrames
    return missing_in_gateway_df, missing_in_ledger_df, amount_mismatch_df, status_mismatch_df  




ledger_df = pd.read_csv("ledger.csv")
gateway_df = pd.read_csv("gateway_export.csv") 
# Testing the 5% / 3% / 2% / 2% Injection Rates
missing_gate, missing_ledg, amt_mismatch, stat_mismatch = reconcile_payments(ledger_df, gateway_df)

total_rows = len(ledger_df)
print(f"Missing in Gateway: {len(missing_gate)} (Target: ~5% or ~{int(total_rows * 0.05)})")
print(f"Missing in Ledger: {len(missing_ledg)} (Target: ~3% or ~{int(total_rows * 0.03)})")
print(f"Amount Mismatches: {len(amt_mismatch)} (Target: ~2% or ~{int(total_rows * 0.02)})")
print(f"Status Mismatches: {len(stat_mismatch)} (Target: ~2% or ~{int(total_rows * 0.02)})")
