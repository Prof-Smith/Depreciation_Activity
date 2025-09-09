
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
    results = []
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
        results.append({
            "Year": year + 1,
            "Revenue": revenue,
            "COGS": cogs,
            "Gross Profit": gross_profit,
            "SG&A": sgna,
            "Depreciation": depr,
            "Operating Expenses": operating_expenses,
            "EBIT": ebit,
            "Taxes": taxes,
            "Net Income": net_income,
            "EPS": eps,
            "Cash Flow": cf_operating,
            "CF per Share": cf_per_share,
            "PV EPS": pv_eps,
            "PV CF per Share": pv_cf
        })
    return pd.DataFrame(results)

st.title("Depreciation Impact on Financials")
method = st.selectbox("Select Depreciation Method", list(dep_schedules.keys()))
df = compute_financials(dep_schedules[method])

st.subheader("Income Statement and Cash Flow")
st.dataframe(df)

fig_eps = go.Figure()
fig_eps.add_trace(go.Scatter(x=df['Year'], y=df['EPS'], mode='lines+markers', name='EPS'))
fig_eps.update_layout(title='EPS Over Time', xaxis_title='Year', yaxis_title='EPS')
st.plotly_chart(fig_eps)

fig_cf = go.Figure()
fig_cf.add_trace(go.Scatter(x=df['Year'], y=df['CF per Share'], mode='lines+markers', name='CF per Share'))
fig_cf.update_layout(title='Cash Flow per Share Over Time', xaxis_title='Year', yaxis_title='CF per Share')
st.plotly_chart(fig_cf)

avg_eps_val = df['EPS'].mean() / required_return
dcf_eps_val = df['PV EPS'].sum()
avg_cf_val = df['CF per Share'].mean() / required_return
dcf_cf_val = df['PV CF per Share'].sum()

st.subheader("Valuation Summary")
st.write(f"Average EPS-based Valuation: ${avg_eps_val:.2f}")
st.write(f"DCF EPS-based Valuation: ${dcf_eps_val:.2f}")
st.write(f"Average CF-based Valuation: ${avg_cf_val:.2f}")
st.write(f"DCF CF-based Valuation: ${dcf_cf_val:.2f}")
