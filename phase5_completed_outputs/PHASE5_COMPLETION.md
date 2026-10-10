# Phase 5 Completion Record

## Status
Phase 5 is complete.

## Diagnostic finding
The originally proposed seven-slope model was not fully supported in household-grouped validation. In the fold-4 training data, the rural-formal settlement category contained 30 people and 0 non-receipt events. This produced non-convergence and an extreme rural-formal coefficient. The failure is therefore attributable to sparse outcome support/separation rather than general multicollinearity.

## Documented model revision
Following the contingency stated in Submission 1, settlement was simplified. Traditional and rural-formal settlement were combined into a single non-urban category, while urban formal remained the reference category and urban informal remained separate. This reduces the model from seven to six slopes. All five revised household-grouped logistic fits converged.

## Revised primary out-of-fold performance
- N = 1013; non-receipt events = 67; prevalence = 0.0661
- ROC AUC = 0.752 (household-bootstrap 95% interval 0.685–0.811)
- Average precision = 0.203 (95% interval 0.132–0.300)
- Brier score = 0.0578; intercept-only Brier = 0.0618
- Calibration-in-the-large = 0.020
- Calibration slope = 0.836 (95% interval 0.592–1.094)

## Weighted metric sensitivity
- Weighted prevalence = 0.0749
- Weighted ROC AUC = 0.763
- Weighted average precision = 0.222
- Weighted Brier score = 0.0641
- Weighted calibration slope = 0.935

## Complete-case sensitivity
After removing observations with missing model predictors, N = 992 with 63 events. All five folds converged.
- ROC AUC = 0.757
- Average precision = 0.202
- Brier score = 0.0557
- Calibration slope = 0.811

The complete-case results are close to the revised primary analysis, so the small amount of predictor missingness does not materially change the Phase 5 conclusion.

## RQ2 evidence statement
The revised parsimonious logistic model shows useful but imperfect predictive information for reported OPG non-receipt in held-out households. Discrimination is moderate, average precision is substantially above the event prevalence, and probability error improves on the intercept-only reference. Calibration-in-the-large is close to zero, while the calibration slope below one indicates some remaining over-extremity/instability. These results support cautious interpretation as an internally validated research model, not an operational eligibility or grant-decision tool.
