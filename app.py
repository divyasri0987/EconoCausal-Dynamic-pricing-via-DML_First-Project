import streamlit as st, pandas as pd, numpy as np
import plotly.express as px, plotly.graph_objects as go

st.set_page_config(page_title="EconoCausal", layout="wide")
st.title("EconoCausal: Causal Uplift & Budget Allocation")

up = st.sidebar.file_uploader("Upload ITE scores CSV", type="csv")
df = pd.read_csv(up) if up else pd.read_csv("ite_scores.csv")
budget = st.sidebar.number_input("Budget ($)", 100, 100000, 1000, 100)
cost = st.sidebar.number_input("Cost per email ($)", 0.01, 5.0, 0.10, 0.01)
value = st.sidebar.number_input("Revenue per conversion ($)", 1.0, 500.0, 116.0, 1.0)
lo, hi = int(df.recency.min()), int(df.recency.max())
r = st.sidebar.slider("Recency (months)", lo, hi, (lo, hi))
f = df[df.recency.between(*r)]

c1, c2 = st.columns(2)
c1.metric("Customers", f"{len(f):,}")
c2.metric("Average ITE", f"{f.ITE.mean():.5f}")

st.plotly_chart(px.histogram(f, x="ITE", nbins=50, title="ITE distribution"), use_container_width=True)

o = f.sort_values("ITE", ascending=False)
y, t = o.conversion.values, o.treatment.values
nt, nc = np.cumsum(t), np.cumsum(1 - t)
q = np.cumsum(y * t) - np.cumsum(y * (1 - t)) * np.where(nc > 0, nt / np.maximum(nc, 1), 0)
x = np.arange(1, len(y) + 1) / len(y)
fig = go.Figure()
fig.add_scatter(x=x, y=q, name="Causal model")
fig.add_scatter(x=[0, 1], y=[0, q[-1]], name="Random", line=dict(dash="dash"))
fig.update_layout(title="Qini / Uplift curve", xaxis_title="Fraction targeted", yaxis_title="Incremental conversions")
st.plotly_chart(fig, use_container_width=True)

n = int(budget / cost)
alloc = o.head(n)
opt = (alloc.ITE * value).sum()
rnd = f.ITE.mean() * value * len(alloc)
st.success(f"This strategy earns ${opt - rnd:,.2f} more than random targeting with the same ${budget:,} budget.")
st.subheader("Allocation: customers to email")
st.dataframe(alloc.head(100))
