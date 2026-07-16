"""
MDR Processing Backend Module
Refactored from original script to be importable as a function
"""

import pandas as pd

def process_file(file_path):
    """
    Process MDR Excel file and return processed DataFrame
    
    Args:
        file_path (str): Path to input Excel/CSV file
        
    Returns:
        pd.DataFrame: Processed dataframe with MDR calculations
    """
    
    # Read file
    df = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
    
    operator_cols = ["EP", "JC", "1LINK", "ALFA", "Checkout", "HBL"]
    
    required_cols = [
        "Gross", "MDR", "Net (Gross-MDR)",
        "Refund", "Tax", "Other", "Net2",
        "Payment Type", "Payment Amount", "Payment Date",
        "Reference", "Status"
    ]
    
    # Add missing columns
    for col in required_cols:
        if col not in df.columns:
            df[col] = ""
    
    # Convert operator columns to numeric
    for col in operator_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    
    # Parse dates and merchant IDs
    df["Created Date Parsed"] = pd.to_datetime(df["Created Date"], errors="coerce")
    df["Merchant ID"] = pd.to_numeric(df["Merchant ID"], errors="coerce")
    
    valid_mask = df["Created Date Parsed"].notna() & df["Merchant ID"].notna()
    df.loc[valid_mask, "Merchant ID"] = df.loc[valid_mask, "Merchant ID"].astype(int)
    
    # MDR Rates Dictionary
    mdr_rates = {
        2001137: {"EP": 0.0384, "JC": 0.0384, "1LINK": 0.0384, "HBL": 0.0384, "ALFA": 0.0384, "Checkout": 0.00},
        2001043: {"EP": 0.0250, "JC": 0.0250, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000033: {"EP": 0.0300, "JC": 0.0300, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000195: {"EP": 0.0300, "JC": 0.0300, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2001144: {"EP": 0.0200, "JC": 0.0200, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        1000176: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.00, "HBL": 0.0350, "ALFA": 0.00, "Checkout": 0.00},
        2001007: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.00, "HBL": 0.0350, "ALFA": 0.00, "Checkout": 0.00},
        2001124: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.00, "HBL": 0.0350, "ALFA": 0.00, "Checkout": 0.00},
        2000881: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.00, "HBL": 0.0350, "ALFA": 0.00, "Checkout": 0.00},
        2000048: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.00, "HBL": 0.0350, "ALFA": 0.00, "Checkout": 0.00},
        2000889: {"EP": 0.0375, "JC": 0.0375, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000002: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000980: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000888: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2001122: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000933: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000785: {"EP": 0.0150, "JC": 0.0150, "1LINK": 0.0150, "HBL": 0.0150, "ALFA": 0.0150, "Checkout": 0.00},
        2000637: {"EP": 0.0200, "JC": 0.0200, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000193: {"EP": 0.0220, "JC": 0.0220, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000626: {"EP": 0.0250, "JC": 0.0250, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2001155: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.0250, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        1000175: {"EP": 0.0300, "JC": 0.0300, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000941: {"EP": 0.0275, "JC": 0.0275, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2001001: {"EP": 0.0275, "JC": 0.0275, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000030: {"EP": 0.0250, "JC": 0.0250, "1LINK": 0.0100, "HBL": 0.0450, "ALFA": 0.00, "Checkout": 0.00},
        2000006: {"EP": 0.0500, "JC": 0.0500, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000890: {"EP": 0.0200, "JC": 0.0200, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2001170: {"EP": 0.0400, "JC": 0.0400, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000061: {"EP": 0.0275, "JC": 0.0275, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2001141: {"EP": 0.0300, "JC": 0.0300, "1LINK": 0.0250, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000937: {"EP": 0.0400, "JC": 0.0400, "1LINK": 0.00, "HBL": 0.0400, "ALFA": 0.00, "Checkout": 0.00},
        2000621: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000795: {"EP": 0.0230, "JC": 0.0230, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000817: {"EP": 0.0150, "JC": 0.0150, "1LINK": 0.0035, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000841: {"EP": 0.0375, "JC": 0.0375, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000806: {"EP": 0.0300, "JC": 0.0300, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000103: {"EP": 0.0310, "JC": 0.0310, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000878: {"EP": 0.0375, "JC": 0.0375, "1LINK": 0.00, "HBL": 0.0375, "ALFA": 0.0375, "Checkout": 0.00},
        2000909: {"EP": 0.0375, "JC": 0.0375, "1LINK": 0.00, "HBL": 0.0375, "ALFA": 0.0375, "Checkout": 0.00},
        2000988: {"EP": 0.0450, "JC": 0.0450, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000847: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.0350, "HBL": 0.0350, "ALFA": 0.0350, "Checkout": 0.00},
        2000837: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.0350, "HBL": 0.0350, "ALFA": 0.0350, "Checkout": 0.00},
        2000721: {"EP": 0.0325, "JC": 0.0325, "1LINK": 0.0325, "HBL": 0.0325, "ALFA": 0.0325, "Checkout": 0.00},
        2000021: {"EP": 0.0300, "JC": 0.0300, "1LINK": 0.0300, "HBL": 0.0300, "ALFA": 0.0300, "Checkout": 0.00},
        2000793: {"EP": 0.0500, "JC": 0.0500, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000858: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.0350, "HBL": 0.0350, "ALFA": 0.0350, "Checkout": 0.00},
        2000877: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.0350, "HBL": 0.0350, "ALFA": 0.0350, "Checkout": 0.00},
        2000191: {"EP": 0.0200, "JC": 0.0200, "1LINK": 0.0200, "HBL": 0.0200, "ALFA": 0.0200, "Checkout": 0.00},
        2000192: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.0350, "HBL": 0.0350, "ALFA": 0.0350, "Checkout": 0.00},
        2001008: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.0350, "HBL": 0.0350, "ALFA": 0.0350, "Checkout": 0.00},
        2000876: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.0350, "HBL": 0.0350, "ALFA": 0.0350, "Checkout": 0.00},
        2000928: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.0350, "HBL": 0.0350, "ALFA": 0.0350, "Checkout": 0.00},
        2000182: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.0350, "HBL": 0.0350, "ALFA": 0.0350, "Checkout": 0.00},
        2001009: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.0350, "HBL": 0.0350, "ALFA": 0.0350, "Checkout": 0.00},
        2000923: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.0350, "HBL": 0.0350, "ALFA": 0.0350, "Checkout": 0.00},
        2000181: {"EP": 0.0350, "JC": 0.0350, "1LINK": 0.0350, "HBL": 0.0350, "ALFA": 0.0350, "Checkout": 0.00},
        2000836: {"EP": 0.0400, "JC": 0.0400, "1LINK": 0.0300, "HBL": 0.0400, "ALFA": 0.0400, "Checkout": 0.00},
        1000183: {"EP": 0.0250, "JC": 0.0250, "1LINK": 0.0250, "HBL": 0.0250, "ALFA": 0.0250, "Checkout": 0.00},
        2000781: {"EP": 0.0400, "JC": 0.0400, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
        2000844: {"EP": 0.0400, "JC": 0.0400, "1LINK": 0.00, "HBL": 0.00, "ALFA": 0.00, "Checkout": 0.00},
    }
    
    def calculate_mdr(row):
        """Calculate MDR for a row based on merchant and operators"""
        merchant_id = int(row["Merchant ID"])
        
        if merchant_id not in mdr_rates:
            return 0
        
        total_mdr = 0
        for operator in operator_cols:
            total_mdr += row[operator] * mdr_rates[merchant_id].get(operator, 0)
        
        return total_mdr
    
    # Status clean
    status_clean = df["Status"].fillna("").astype(str).str.strip().str.lower()
    
    unlocked_mask = (
        valid_mask &
        (status_clean != "locked")
    )
    
    # Apply Gross, MDR, Net on all unlocked rows
    df.loc[unlocked_mask, "Gross"] = df.loc[unlocked_mask, operator_cols].sum(axis=1)
    df.loc[unlocked_mask, "MDR"] = df.loc[unlocked_mask].apply(calculate_mdr, axis=1)
    df.loc[unlocked_mask, "Net (Gross-MDR)"] = (
        df.loc[unlocked_mask, "Gross"] - df.loc[unlocked_mask, "MDR"]
    )
    
    # Round amount columns
    for col in ["Gross", "MDR", "Net (Gross-MDR)"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").round(2)
    
    # Round all amount columns
    amount_cols = [
        "EP", "JC", "1LINK", "ALFA", "Checkout", "HBL",
        "Gross", "MDR", "Net (Gross-MDR)",
        "Refund", "Tax", "Other", "Net2", "Payment Amount"
    ]
    
    for col in amount_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").round(2)
    
    # Drop temporary column
    df = df.drop(columns=["Created Date Parsed"])
    
    # Reorder columns
    final_cols = [
        "Created Date", "Merchant ID", "EP", "JC", "1LINK", "ALFA",
        "Checkout", "HBL", "Gross", "MDR", "Net (Gross-MDR)",
        "Refund", "Tax", "Other", "Net2",
        "Payment Type", "Payment Amount", "Payment Date",
        "Reference", "Status"
    ]
    
    # Keep only columns that exist
    final_cols = [col for col in final_cols if col in df.columns]
    df = df[final_cols]
    
    return df


if __name__ == "__main__":
    # Test function
    print("Backend module loaded successfully!")
