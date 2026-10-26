# Day 8 Progress: Discount Version, Dashboard Enhancements and Documentation

## Work completed
1. Extended the project from the email campaign to the discount use case described in the project document.
2. Created a synthetic discount variable ($0 / $10 / $20) with confounding (customers with higher purchase history were more likely to receive higher discounts), and simulated conversions with heterogeneous treatment effects.
3. Trained Double Machine Learning models (EconML LinearDML with LightGBM) to estimate the Individual Treatment Effect (ITE) of the $10 and $20 discounts separately.
4. Built Qini/uplift curves and ran a placebo test (shuffled treatment) as the causal audit. The placebo effect was close to zero compared to the real effect.
5. Implemented budget-constrained allocation that prescribes the best discount for each customer.
6. Updated the dashboard with a budget input, CSV upload, ITE histogram, Qini curve, prescription chart and table, and a download option for the prescription.
7. Uploaded the updated notebook, dashboard code and score files to GitHub, and submitted the Week 1 and Week 2 write-ups.

## Challenges and fixes
- DoWhy's estimation step failed due to a version incompatibility with the latest pandas and networkx, so I used regression for the baseline estimate and a placebo test for the audit.
- Double ML with a three-level discount failed in the latest pandas, so I fitted separate models for $10 vs $0 and $20 vs $0.

## Learnings
- Difference between predicting outcomes and estimating causal effects.
- How to prescribe actions (discounts) under a budget constraint instead of only predicting.

## Next steps
- Add a README with results and screenshots.
- Build the REST API for the model.
