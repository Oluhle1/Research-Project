# Discussion — plain-language working section

This section mirrors the current manuscript. Edit `manuscript.md` to change the paper build.

### A. Whose non-receipt does the study measure?

RQ1 measures non-receipt among historical KwaZulu-Natal adults who pass the screen and resolve receipt: 67/1,013, or 6.61% unweighted and 7.49% person-weighted. This does not measure unlawful denial or non-receipt among everyone legally entitled. The 187 unresolved adults outnumber the 67 events. Excluding them changes the population I describe, regardless of sampling uncertainty. Stable estimates cannot reveal their receipt.

S2d adds 68 people but only two events, reducing weighted non-receipt to 7.12%. Partnership rules mainly change the denominator. S3 retains adults with incompatible grants, adds 19 people/15 events and raises non-receipt to 9.06%, the largest tested change. Similar AUC cannot justify rules or establish equivalent populations. Ralston studies rural age-eligible people [2]; Godfrey studies households' grants [6]. Different units, programmes, screens and places prevent direct comparison of their percentages. I add a provincial estimate with an explicit resource screen. High receipt can involve access costs [12], [16]; it cannot prove low burden.

### B. What do the predictions tell you?

RQ2 assesses four properties. AUC 0.752 describes ranking held-out non-recipients above recipients, not classification accuracy. AP 0.203 summarises precision–recall ranking across cutoffs against a 6.61% event rate, not precision at one cutoff [20]. Brier falls from 0.0618 to 0.0578: a modest 0.0040 reduction in squared probability error. To check average bias, I estimate an intercept correction while fixing the calibration slope at 1. The ideal is zero. The estimate 0.020 and interval spanning zero do not prove perfect agreement. Slope 0.836 suggests that predictions may be too extreme, but its 0.591–1.133 interval includes the ideal 1 [19]. 67 events inform these checks [21]. Most adults in even the highest-risk bin report receipt.

Table II separates concepts from measured predictors. Schooling suggests learning costs; distance/settlement suggest compliance costs [12], [16]. These odds ratios describe the screened group, not OOF effects or burden. Lower schooling accompanies receipt, against a simple information-barrier expectation. Fewer other resources or screening selection could explain this; I test neither explanation. Uncertain office/settlement associations neither confirm nor rule out compliance costs. I do not measure psychological costs. Without awareness, visits, document demands or administrative decisions, I cannot explain non-receipt.

Table VIII separates sample, predictor and evaluation changes. S7 removes 21 people/four events (992/63). Its lower Brier concerns a different sample and cannot establish whether filling missing values is better. S8 substitutes marriage for welfare access and performs similarly. S9 weights fitting but not evaluation; it does not model the full survey design. S10 reweights the same primary OOF predictions without retraining, raising Brier to 0.0641. S11 groups folds by derived PSU and also performs similarly. S8–S11 keep 1,013 people/67 events. These checks expose internal assumptions, rather than establish model superiority or reliability elsewhere [22], [23].

### C. What does RQ3 establish?

RQ3 has six evidence layers. Synthetic cases check rule decisions; matching file contents check repeatability; UI–CLI agreement checks software paths; JSON reload checks saved-model predictions. The owner walkthrough checks a synthetic workflow; participant testing would assess human usability. Table IX supports the first five within tested conditions. Automated agreement cannot establish independent user ease, acceptance or field success. Saved sources and run/validation reports expose versions, checksums and test conditions.

I separate historical OOF results from uploaded scores; uploads may overlap training data. Matching saved scores checks reloading, not new predictive accuracy. You can inspect the computations, but representative user clarity remains untested. The task sheet supports future testing.

### D. Could this work elsewhere?

I study screened KwaZulu-Natal adults in LCS 2014/2015. Provinces and periods differ in settlement, services, policy and reporting. Application, award and payment records measure different events from reported receipt and can contain linking errors. I have tested no independent province, period or administrative sample. Transfer needs comparable populations/outcomes, justified period-specific rules and independent ranking/calibration checks [22], [23]. Making the app available cannot establish suitability for today's applicants.
