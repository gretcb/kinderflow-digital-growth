# KinderFlow ROI slide inputs

These calculations are decision scenarios, not forecasts. Annual add-on revenue is EUR 0 in all three cases. The model does not count Little Steps staff time as KinderFlow revenue.

## Core assumptions

| Input | Low | Base | High | Evidence label |
|---|---:|---:|---:|---|
| Annual subscription per centre | EUR 600 | EUR 1,200 | EUR 1,800 | PILOT PRICING HYPOTHESIS |
| Average paying centres in Year 1 | 3 | 6 | 10 | MARKET HYPOTHESIS |
| Average paying centres in Year 2 | 5 | 15 | 30 | MARKET HYPOTHESIS |
| Average paying centres in Year 3 | 8 | 30 | 60 | MARKET HYPOTHESIS |
| Upfront validation cost | EUR 5,500 | EUR 11,400 | EUR 17,300 | PROJECT ESTIMATE |
| Annual fixed operations | EUR 2,400 | EUR 4,800 | EUR 6,000 | PROJECT ESTIMATE |
| Variable cost per centre-year | EUR 180 | EUR 240 | EUR 300 | PROJECT ESTIMATE |
| Annual reusable-content programme | EUR 3,000 | EUR 4,000 | EUR 6,000 | PROJECT ESTIMATE |
| Add-on revenue | EUR 0 | EUR 0 | EUR 0 | CONSERVATIVE MODEL CHOICE |

The 2-3 nursery pilot is a controlled test. It is not the Year 1 customer-count assumption.

## Results

| Result | Low | Base | High |
|---|---:|---:|---:|
| 12-month revenue | EUR 1,800 | EUR 7,200 | EUR 18,000 |
| 12-month cost | EUR 11,440 | EUR 21,640 | EUR 32,300 |
| 12-month net benefit | -EUR 9,640 | -EUR 14,440 | -EUR 14,300 |
| 12-month ROI | -84.3% | -66.7% | -44.3% |
| 36-month revenue | EUR 9,600 | EUR 61,200 | EUR 180,000 |
| 36-month cost | EUR 24,580 | EUR 50,040 | EUR 83,300 |
| 36-month net benefit | -EUR 14,980 | EUR 11,160 | EUR 96,700 |
| 36-month ROI | -60.9% | 22.3% | 116.1% |
| Modelled break-even month | Beyond month 36 | Month 29.3 | Month 17.2 |
| Steady-state break-even centres | 13 | 10 | 8 |
| Year 1 all-in break-even centres | 26 | 22 | 20 |

Every 12-month result is negative. The model does not choose assumptions merely to produce an early positive return.

## Formula notes

```text
Revenue = average paying centres x annual subscription
Annual operating cost = fixed operations + reusable-content programme + (centres x variable cost)
Year 1 cost = upfront validation cost + annual operating cost
ROI = (revenue - cost) / cost x 100
```

The break-even month assumes even monthly recognition within each model year and the stated average centre counts. `Beyond month 36` means cumulative contribution does not recover the upfront cost inside the model period.

## Little Steps affordability lens

| Annual subscription | Share of EUR 195k tuition envelope | Share of EUR 238k tuition envelope | Cost per released hour at 42.9 hours | Cost per released hour at 71.5 hours |
|---:|---:|---:|---:|---:|
| EUR 600 | 0.31% | 0.25% | EUR 14.0 | EUR 8.4 |
| EUR 1,200 | 0.62% | 0.50% | EUR 28.0 | EUR 16.8 |
| EUR 1,800 | 0.92% | 0.76% | EUR 42.0 | EUR 25.2 |

The revenue envelope and time-release figures are calculated scenarios. The implied hourly figures show the value threshold needed for the subscription to be covered by time release alone. They are not measured savings, affordability evidence or a salary valuation. Family value and commercial differentiation are separate possible benefits and must not be double counted.

## Variables for pilot validation

- Actual price range and monthly versus annual preference.
- Budget owner and procurement friction.
- Paid continuation and retention.
- Content creation, qualified review and rework cost.
- Support and onboarding cost per centre.
- Reuse count per approved asset.
- Educator repeat assignment and family use.

Full model: `../roi_risk_assessment.md`.
