
import streamlit as st
import pandas as pd

sales = 100000
cogs_pct = 0.60
sgna_pct = 0.15
tax_rate = 0.21
shares = 10000
required_return = 0.10

dep_schedules = {
    "3-Year MACRS": [13200, 18000, 6000, 2800, 0, 0],
    "5-Year MACRS": [8000, 12800, 7600, 4800, 4800, 2000],
    "Straight-Line": [6666.67] * 6
}

def compute_financials(depreciation):
    data = {}
    for year in range(6):
        revenue = sales
        cogs = revenue * cogs_pct
        gross_profit = revenue - cogs
        sgna = gross_profit * sgna_pct
        depr = depreciation[year]
        operating_expenses = sgna + depr
        ebit = gross_profit - operating_expenses
        taxes = ebit * tax_rate
        net_income = ebit - taxes
        eps = net_income / shares
        cf_operating = net_income + depr
        invest = -40000 if year == 0 else 0
        finance = 40000 if year == 0 else 0
        total_cf = cf_operating + invest + finance
        cf_per_share = total_cf / shares
        discount_factor = (1 + required_return) ** (year + 1)
        pv_eps = eps / discount_factor
        pv_cf = cf_per_share / discount_factor

        data.setdefault("Revenue", []).append(revenue)
        data.setdefault("COGS", []).append(cogs)
        data.setdefault("Gross Profit", []).append(gross_profit)
        data.setdefault("SG&A", []).append(sgna)
        data.setdefault("Depreciation", []).append(depr)
        data.setdefault("Operating Expenses", []).append(sgna + depr)
        data.setdefault("EBIT", []).append(ebit)
        data.setdefault("Taxes", []).append(taxes)
        data.setdefault("Net Profit After Taxes", []).append(net_income)
        data.setdefault("EPS", []).append(eps)
        data.setdefault("Cash Provided by Operating Activities", []).append(cf_operating)
        data.setdefault("Increase in Equipment", []).append(invest)
        data.setdefault("Owner Financing", []).append(finance)
        data.setdefault("Total Cash Flow", []).append(total_cf)
        data.setdefault("CF per Share", []).append(cf_per_share)
        data.setdefault("PV EPS", []).append(pv_eps)
        data.setdefault("PV CF per Share", []).append(pv_cf)

    df = pd.DataFrame(data).transpose()
    df.columns = [f"Year {i+1}" for i in range(6)]
    return df

st.title("Depreciation Impact on Financial Statements")
method = st.selectbox("Select Depreciation Method", list(dep_schedules.keys()))
df = compute_financials(dep_schedules[method])

st.subheader("Income Statement")
st.dataframe(df.loc[["Revenue", "COGS", "Gross Profit", "SG&A", "Depreciation", "Operating Expenses", "EBIT", "Taxes", "Net Profit After Taxes", "EPS"]])

st.subheader("Cash Flow Statement")
st.dataframe(df.loc[["Cash Provided by Operating Activities", "Increase in Equipment", "Owner Financing", "Total Cash Flow", "CF per Share"]])

st.subheader("Valuation Summary")
avg_eps_val = df.loc['EPS'].mean() / required_return
dcf_eps_val = df.loc['PV EPS'].sum()
avg_cf_val = df.loc['CF per Share'].mean() / required_return
dcf_cf_val = df.loc['PV CF per Share'].sum()

st.write(f"Average EPS-based Valuation: ${avg_eps_val:.2f}")
st.write(f"DCF EPS-based Valuation: ${dcf_eps_val:.2f}")
st.write(f"Average CF-based Valuation: ${avg_cf_val:.2f}")
st.write(f"DCF CF-based Valuation: ${dcf_cf_val:.2f}")
