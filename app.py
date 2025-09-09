import streamlit as st
import pandas as pd

# Constants
sales = 100000
cogs_pct = 0.60
sgna_pct = 0.15
tax_rate = 0.21
shares = 10000
required_return = 0.10

# Depreciation schedules
dep_schedules = {
    "3-Year MACRS": [13200, 18000, 6000, 2800, 0, 0],
    "5-Year MACRS": [8000, 12800, 7600, 4800, 4800, 2000],
    "Straight-Line": [6666.67] * 6
}

def compute_financials(depreciation):
    data = {
        "Revenue": [],
        "COGS": [],
        "Gross Profit": [],
        "SG&A": [],
        "Depreciation": [],
        "Operating Expenses": [],
        "EBIT": [],
        "Taxes": [],
        "Net Profit After Taxes": [],
        "EPS": [],
        "Cash Provided by Operating Activities": [],
        "Increase in Equipment": [],
        "Owner Financing": [],
        "Total Cash Flow": [],
        "CF per Share": [],
        "PV EPS": [],
        "PV CF per Share": []
    }

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
        cf_per_share = cf_operating / shares
        discount_factor = (1 + required_return) ** (year + 1)
        pv_eps = eps / discount_factor
        pv_cf = cf_per_share / discount_factor
        invest = -40000 if year == 0 else 0
        finance = 40000 if year == 0 else 0
        total_cf = cf_operating + invest + finance

        data["Revenue"].append(revenue)
        data["COGS"].append(cogs)
        data["Gross Profit"].append(gross_profit)
        data["SG&A"].append(sgna)
        data["Depreciation"].append(depr)
        data["Operating Expenses"].append(operating_expenses)
        data["EBIT"].append(ebit)
        data["Taxes"].append(taxes)
        data["Net Profit After Taxes"].append(net_income)
        data["EPS"].append(eps)
        data["Cash Provided by Operating Activities"].append(cf_operating)
        data["Increase in Equipment"].append(invest)
        data["Owner Financing"].append(finance)
        data["Total Cash Flow"].append(total_cf)
        data["CF per Share"].append(cf_per_share)
        data["PV EPS"].append(pv_eps)
        data["PV CF per Share"].append(pv_cf)

    df = pd.DataFrame(data)
    df.columns = [f"Year {i+1}" for i in range(6)]
    return df

# Streamlit UI
st.title("Depreciation Impact on Financial Statements")

method = st.selectbox("Select Depreciation Method", list(dep_schedules.keys()))
df = compute_financials(dep_schedules[method])

st.subheader("Income Statement and Cash Flow (Transposed)")
st.dataframe(df)

# Valuation Summary
avg_eps_val = df.loc["EPS"].mean() / required_return
dcf_eps_val = df.loc["PV EPS"].sum()
avg_cf_val = df.loc["CF per Share"].mean() / required_return
dcf_cf_val = df.loc["PV CF per Share"].sum()

st.subheader("Valuation Summary")
st.write(f"Average EPS-based Valuation: ${avg_eps_val:.2f}")
st.write(f"DCF EPS-based Valuation: ${dcf_eps_val:.2f}")
st.write(f"Average CF-based Valuation: ${avg_cf_val:.2f}")
st.write(f"DCF CF-based Valuation: ${dcf_cf_val:.2f}")
