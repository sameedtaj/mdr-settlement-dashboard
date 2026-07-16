# app.py
# Streamlit Frontend Only

import streamlit as st
import pandas as pd
import tempfile
import os
from io import BytesIO

from backend import process_file   # backend.py must have process_file(file_path)

# =========================
# Page Config
# =========================

st.set_page_config(
    page_title="MDR Settlement Dashboard",
    page_icon="💳",
    layout="wide"
)

# =========================
# Styling
# =========================

st.markdown("""
<style>
.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #1f2937;
}
.sub-title {
    color: #6b7280;
    font-size: 15px;
    margin-bottom: 20px;
}
.card {
    padding: 22px;
    border-radius: 16px;
    background: linear-gradient(135deg, #ffffff, #f8fafc);
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
    border: 1px solid #e5e7eb;
}
.card-title {
    font-size: 14px;
    color: #6b7280;
    font-weight: 600;
}
.card-value {
    font-size: 26px;
    font-weight: 800;
    color: #111827;
}
.section-box {
    padding: 20px;
    border-radius: 14px;
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">💳 MDR Settlement Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Upload file → backend calculates MDR/Net → filter data → lock settlement with reference.</div>',
    unsafe_allow_html=True
)

# =========================
# Upload
# =========================

st.sidebar.header("📁 Upload File")

uploaded_file = st.sidebar.file_uploader(
    "Upload Excel / CSV File",
    type=["xlsx", "xls", "csv"]
)

if uploaded_file is None:
    st.info("Upload your settlement file to start.")
    st.stop()

file_extension = uploaded_file.name.split(".")[-1]

with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_file:
    tmp_file.write(uploaded_file.getbuffer())
    temp_file_path = tmp_file.name

# =========================
# Backend Processing
# =========================

try:
    with st.spinner("Processing file from backend..."):
        df = process_file(temp_file_path)

except Exception as e:
    st.error("Backend processing failed.")
    st.exception(e)
    st.stop()

finally:
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

if df is None or df.empty:
    st.warning("Backend returned empty data.")
    st.stop()

# =========================
# Column Safety
# =========================

required_cols = [
    "Created Date", "Merchant ID", "Gross", "MDR", "Net (Gross-MDR)",
    "Refund", "Tax", "Other", "Net2",
    "Payment Type", "Payment Amount", "Payment Date",
    "Reference", "Status"
]

for col in required_cols:
    if col not in df.columns:
        df[col] = ""

df["Created Date"] = pd.to_datetime(df["Created Date"], errors="coerce")
df["Merchant ID"] = pd.to_numeric(df["Merchant ID"], errors="coerce").astype("Int64")
df["Status"] = df["Status"].fillna("").astype(str)

amount_cols = [
    "Gross", "MDR", "Net (Gross-MDR)",
    "Refund", "Tax", "Other", "Net2", "Payment Amount"
]

for col in amount_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# =========================
# Top KPI Cards
# =========================

locked_mask = df["Status"].str.strip().str.lower().eq("locked")
pending_mask = ~locked_mask

total_merchants = df["Merchant ID"].nunique()
total_volume = df["Gross"].sum()
total_locked_payment = df.loc[locked_mask, "Payment Amount"].sum()
total_pending_payment = df.loc[pending_mask, "Net (Gross-MDR)"].sum()

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Total Merchants</div>
        <div class="card-value">{total_merchants:,}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Total Volume</div>
        <div class="card-value">{total_volume:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Total Locked Payment</div>
        <div class="card-value">{total_locked_payment:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Total Pending Payment</div>
        <div class="card-value">{total_pending_payment:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# Ask Lock Payment
# =========================

st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("🔐 Settlement Action")

lock_choice = st.radio(
    "Do you want to lock any payment?",
    ["No", "Yes"],
    horizontal=True
)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# Filters
# =========================

filtered_df = df.copy()

if lock_choice == "Yes":
    st.sidebar.header("🔎 Lock Payment Filters")

    min_date = filtered_df["Created Date"].min()
    max_date = filtered_df["Created Date"].max()

    if pd.notna(min_date) and pd.notna(max_date):
        date_range = st.sidebar.date_input(
            "Select Settlement Date Range",
            value=(min_date.date(), max_date.date())
        )

        if len(date_range) == 2:
            start_date, end_date = date_range
            filtered_df = filtered_df[
                (filtered_df["Created Date"].dt.date >= start_date) &
                (filtered_df["Created Date"].dt.date <= end_date)
            ]

    merchant_list = sorted(filtered_df["Merchant ID"].dropna().unique())

    selected_merchant = st.sidebar.selectbox(
        "Select Merchant ID",
        options=merchant_list
    )

    filtered_df = filtered_df[
        filtered_df["Merchant ID"] == selected_merchant
    ]

    filtered_df = filtered_df.sort_values("Created Date")

    unlocked_filtered = filtered_df[
        filtered_df["Status"].str.strip().str.lower() != "locked"
    ]

    locked_filtered = filtered_df[
        filtered_df["Status"].str.strip().str.lower() == "locked"
    ]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Selected Rows", f"{len(filtered_df):,}")

    with c2:
        st.metric("Unlocked Rows", f"{len(unlocked_filtered):,}")

    with c3:
        st.metric("Locked Rows", f"{len(locked_filtered):,}")

    with c4:
        st.metric("Selected Net", f"{filtered_df['Net (Gross-MDR)'].sum():,.2f}")

    st.subheader("📋 Selected Merchant Data")
    st.dataframe(filtered_df, use_container_width=True, height=320)

    if unlocked_filtered.empty:
        st.warning("All selected rows are already locked.")
    else:
        st.subheader("🧾 Enter Settlement Details")

        with st.form("settlement_form"):
            a1, a2, a3 = st.columns(3)

            with a1:
                refund = st.number_input("Refund", min_value=0.0, value=0.0)

            with a2:
                tax = st.number_input("Tax", min_value=0.0, value=0.0)

            with a3:
                other = st.number_input("Other", min_value=0.0, value=0.0)

            b1, b2, b3 = st.columns(3)

            with b1:
                payment_type = st.selectbox(
                    "Payment Type",
                    ["USD", "Top up", "Bank detail"]
                )

            with b2:
                payment_amount = st.number_input(
                    "Payment Amount",
                    min_value=0.0,
                    value=0.0
                )

            with b3:
                payment_date = st.date_input("Payment Date")

            reference = st.text_input("Reference")

            submit = st.form_submit_button("✅ Apply & Lock Payment")

        if submit:
            if reference.strip() == "":
                st.error("Reference is required.")
            else:
                selected_indexes = unlocked_filtered.index.tolist()
                first_index = selected_indexes[0]

                df.loc[selected_indexes, "Payment Type"] = payment_type
                df.loc[selected_indexes, "Payment Date"] = str(payment_date)
                df.loc[selected_indexes, "Reference"] = reference
                df.loc[selected_indexes, "Status"] = "Locked"

                df.loc[first_index, "Refund"] = refund
                df.loc[first_index, "Tax"] = tax
                df.loc[first_index, "Other"] = other
                df.loc[first_index, "Payment Amount"] = payment_amount

                df.loc[first_index, "Net2"] = (
                    df.loc[first_index, "Net (Gross-MDR)"]
                    - (refund + tax + other)
                )

                st.success("Payment locked successfully.")

                filtered_df = df.loc[selected_indexes].copy()

else:
    st.sidebar.header("🔎 View Filters")

    status_options = sorted(df["Status"].fillna("").unique())

    selected_status = st.sidebar.multiselect(
        "Status",
        options=status_options,
        default=status_options
    )

    filtered_df = df[df["Status"].isin(selected_status)]

# =========================
# Output Table
# =========================

st.subheader("📋 Output Data")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=500
)

# =========================
# Download
# =========================

st.subheader("⬇️ Download Updated Output")

excel_buffer = BytesIO()

with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name="Updated Output")

st.download_button(
    label="📥 Download Updated Excel",
    data=excel_buffer.getvalue(),
    file_name="updated_mdr_output.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)