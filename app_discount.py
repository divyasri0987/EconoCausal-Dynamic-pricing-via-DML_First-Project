import streamlit as st, pandas as pd, numpy as np
import plotly.express as px, plotly.graph_objects as go

st.set_page_config(page_title="EconoCausal Discount", layout="wide")
st.title("EconoCausal: Discount Uplift & Prescription")

up = st.sidebar.file_uploader("Upload scores CSV", type="csv")
df = pd.read_csv(up) if up else pd.read_csv("discount_scores.csv")
budget = st.sidebar.number_input("Budget ($)", 100, 1000000, 5000, 100)
value = st.sidebar.number_input("Revenue per conversion ($)", 1.0, 500.0, 116.0, 1.0)
lvl = st.sidebar.selectbox("Discount level to inspect ($)", [10, 20])
lo, hi = int(df.recency.min()), int(df.recency.max())
r = st.sidebar.slider("Recency (months)", lo, hi, (lo, hi))
f = df[df.recency.between(*r)].copy()

p0 = df.loc[df.discount == 0, "conversion"].mean()
i10, i20 = f.ITE_10.values, f.ITE_20.values
c10 = np.maximum(10 * (p0 + i10), 1e-9)
c20 = np.maximum(20 * (p0 + i20), 1e-9)
n10, n20 = i10 * value - c10, i20 * value - c20
use20 = n20 > n10
net = np.where(use20, n20, n10)
cost = np.where(use20, c20, c10)
disc = np.where(use20, 20, 10)
order = np.argsort(-(net / cost))
order = order[net[order] > 0]
chosen = order[np.cumsum(cost[order]) <= budget]
f["prescribed"] = 0
f.iloc[chosen, f.columns.get_loc("prescribed")] = disc[chosen]

rr = np.random.default_rng(1).permutation(len(f))
rp = rr[np.cumsum(c10[rr]) <= budget]
opt_gain, rand_gain = net[chosen].sum(), n10[rp].sum()

a, b, c = st.columns(3)
a.metric("Customers", f"{len(f):,}")
b.metric(f"Avg effect of ${lvl} discount", f"{f[f'ITE_{lvl}'].mean():.5f}")
c.metric("Customers prescribed a discount", f"{len(chosen):,}")
st.success(f"This strategy earns \${opt_gain - rand_gain:,.2f} more than random \$10 targeting with the \same ${budget:,} budget.")

st.plotly_chart(px.histogram(f, x=f"ITE_{lvl}", nbins=50, title=f"ITE distribution (${lvl} vs no discount)"), use_container_width=True)

s = f[f.discount.isin([0, lvl])].sort_values(f"ITE_{lvl}", ascending=False)
y, t = s.conversion.values, (s.discount.values == lvl).astype(int)
nt, nc = np.cumsum(t), np.cumsum(1 - t)
q = np.cumsum(y * t) - np.cumsum(y * (1 - t)) * np.where(nc > 0, nt / np.maximum(nc, 1), 0)
x = np.arange(1, len(y) + 1) / len(y)
fig = go.Figure()
fig.add_scatter(x=x, y=q, name="Causal model")
fig.add_scatter(x=[0, 1], y=[0, q[-1]], name="Random", line=dict(dash="dash"))
fig.update_layout(title="Qini / Uplift curve", xaxis_title="Fraction targeted", yaxis_title="Incremental conversions")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Prescription: discount per customer")
counts = f[f.prescribed > 0].prescribed.value_counts().rename_axis("discount").reset_index(name="customers")
st.plotly_chart(px.bar(counts, x="discount", y="customers"), use_container_width=True)
out = f[f.prescribed > 0]
st.dataframe(out.head(100))
st.download_button("Download prescription CSV", out.to_csv(index=False), "prescription.csv")
