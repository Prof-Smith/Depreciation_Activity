
import streamlit as st
import pandas as pd

# Load transposed tables
tables = {
    '3-Year MACRS': pd.read_csv('3-Year_MACRS_transposed.csv', index_col=0),
    '5-Year MACRS': pd.read_csv('5-Year_MACRS_transposed.csv', index_col=0),
    'Straight-Line': pd.read_csv('Straight-Line_transposed.csv', index_col=0)
}

st.title("Depreciation Impact on Financial Statements")
method = st.selectbox("Select Depreciation Method", list(tables.keys()))

st.subheader("Income Statement and Cash Flow (Transposed)")
st.dataframe(tables[method])

# Valuation summary
df = tables[method]
avg_eps_val = df.loc['EPS'].mean() / 0.10
dcf_eps_val = df.loc['PV EPS'].sum()
avg_cf_val = df.loc['CF per Share'].mean() / 0.10
dcf_cf_val = df.loc['PV CF per Share'].sum()

st.subheader("Valuation Summary")
st.write(f"Average EPS-based Valuation: ${avg_eps_val:.2f}")
st.write(f"DCF EPS-based Valuation: ${dcf_eps_val:.2f}")
st.write(f"Average CF-based Valuation: ${avg_cf_val:.2f}")
st.write(f"DCF CF-based Valuation: ${dcf_cf_val:.2f}")
