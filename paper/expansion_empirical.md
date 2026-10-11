# Additional empirical material for the integrated submission

The tables below use only the retained frozen outputs. Table numbers are placeholders for integration into the manuscript.

TABLE: Descriptive characteristics by reported receipt
| Characteristic | Recipients: count/% | Recipients: weighted | Non-recipients: count/% | Non-recipients: weighted |
| --- | --- | --- | --- | --- |
| Age, mean years | 70.4 | 69.8 | 67.3 | 68.4 |
| Female | 686 / 72.5% | 70.4% | 33 / 49.3% | 53.4% |
| Grade 7 or above | 290 / 30.7% | 33.0% | 49 / 73.1% | 80.8% |
| Urban formal settlement | 284 / 30.0% | 36.2% | 38 / 56.7% | 66.2% |
| Welfare office ≥5 km/unavailable | 717 / 75.8% | 72.0% | 34 / 50.7% | 40.3% |

NOTE: Recipient n = 946; non-recipient n = 67. The age row reports unweighted and person-weighted means in years. Other rows report unweighted counts and within-group percentages, followed by person-weighted within-group percentages; weighted percentages are not weighted counts or non-receipt rates. Denominators retain missing predictor values: schooling is unassigned for three recipients, and welfare access is missing for 14 recipients and four non-recipients. These descriptive summaries precede predictive imputation and have no inferential intervals. Source: output/runs/primary/rq1_characteristics.csv.

TABLE: Primary held-out predictive performance and uncertainty
| Metric | Logistic estimate | 95% interval | Intercept-only estimate | 95% interval |
| --- | --- | --- | --- | --- |
| ROC area | 0.752 | 0.687–0.814 | — | — |
| Average precision | 0.203 | 0.139–0.292 | — | — |
| Brier score | 0.0578 | 0.0448–0.0706 | 0.0618 | 0.0467–0.0758 |
| Calibration-in-the-large | 0.020 | −0.316–0.273 | 0.0001 | — |
| Calibration slope | 0.836 | 0.591–1.133 | — | — |

NOTE: Estimates use pooled unweighted household-held-out probabilities for 1,013 people and 67 events; prevalence is 6.61%. Intervals are the 2.5th and 97.5th percentiles of 1,000 household resamples around fixed predictions, with zero invalid resamples for the reported intervals. Models and imputation are not refitted, so these intervals omit repeated development and fitting uncertainty. The intercept-only reference assigns each held-out adult the corresponding training-fold prevalence. Dashes denote metrics or intervals absent from the frozen output; they do not assert zero, chance performance or an estimated confidence bound. Sources: output/runs/primary/metrics.csv and output/runs/primary/bootstrap_intervals.csv.

## Interpretation and methodological justification

The weighted summaries describe the composition of each reported-receipt group; they do not estimate a characteristic's causal effect or determine entitlement. Non-recipients are more often men, more educated and urban formal residents in this screened sample. The differences can reflect resources and selection into the observable denominator, rather than a measured access mechanism. Household-grouped validation avoids placing co-resident adults in both training and testing [22]. Average precision 0.203 must be interpreted beside 6.61% prevalence [20], while the Brier reduction from 0.0618 to 0.0578 is small. The calibration slope interval includes 1 and values substantially below it, supporting cautious probability interpretation [19]. With 67 events, uncertainty remains material [21]. These descriptive and held-out results concern the historical screened cohort; the frozen full-data scores displayed by Streamlit are a separate inference output.

## Numeric audit

All 47 displayed numeric values passed comparison against the three stated CSV sources, without refitting or altering the original model. Group denominators, predictor missingness, event prevalence and bootstrap counts were checked separately and also agreed. The intervals are the current frozen primary run, not the alternative historical export. This audit note can remain outside the submitted paper.
