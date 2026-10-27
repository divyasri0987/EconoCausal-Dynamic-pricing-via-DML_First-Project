## Results

**Email version (Hillstrom data)**
- Average treatment effect: about 0.0049 (regression, p < 0.001); Double ML gives about 0.0050
- Placebo test (shuffled treatment): about 0.0008, close to zero
- Budget-constrained targeting earned about $11,812 vs $5,795 for random targeting (same $1,000 budget, $0.10 per email)

**Discount version (synthetic discount and conversion)**
- Average effect vs no discount: $10 = 0.0132, $20 = 0.0156
- For about 60% of customers the $20 effect was higher than the $10 effect
- With a $5,000 budget the dashboard prescribed a discount to about 13,900 customers

## How to run the dashboard
pip install streamlit plotly pandas numpy
streamlit run app_discount.py

## Assumptions and limitations
- Discount and conversion data are synthetic (mock dataset); the Hillstrom dataset has only an email treatment
- Costs: $0.10 per email; a discount is paid only when the customer buys
- Dashboard is built with Streamlit; REST API is planne


# Day 9 Progress: Documentation and Results Summary

## Work completed
1. Updated the README with a results section covering both the email and discount versions.
2. Documented how to run the dashboard and listed the assumptions and limitations (synthetic discount data, assumed costs, Streamlit dashboard).
3. Summarised key results: average treatment effects, the placebo test and the budget-constrained allocation.

## Learnings
- Clear documentation of assumptions makes causal results easier to interpret and review.

## Next steps
- Add requirements.txt.
- Build the REST API (FastAPI).
