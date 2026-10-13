# Discussion — professional-language working section

This section mirrors Section VI of the current manuscript. Edit `manuscript.md` for the build; this working copy records the same discussion.

### A. Scope of measured non-receipt

RQ1 measures non-receipt among historical KwaZulu-Natal adults who pass the screen and resolve receipt: 67/1,013, or 6.61% unweighted and 7.49% person-weighted. This does not measure unlawful denial or non-receipt among everyone legally entitled. The 187 unresolved adults outnumbered the 67 events. Excluding them changes the population described, regardless of sampling uncertainty. Stable estimates cannot reveal their receipt.

S2d added 68 people but only two events, reducing weighted non-receipt to 7.12%. Partnership rules mainly changed the denominator. S3 retained adults with incompatible grants, added 19 people/15 events and raised non-receipt to 9.06%, the largest tested change. Similar AUC cannot justify screening rules or establish equivalent populations. Ralston studies rural age-eligible people [2]; Godfrey studies households' grants [6]. Different units, programmes, screens and places prevent direct comparison of their percentages. This study adds a provincial estimate with an explicit resource screen. High receipt can involve access costs [12], [16]; it cannot prove low burden.

### B. Predictive performance and interpretation

RQ2 assesses four properties. AUC 0.752 describes ranking held-out non-recipients above recipients, not classification accuracy. AP 0.203 summarises precision–recall ranking across cutoffs against a 6.61% event rate, not precision at one cutoff [20]. Brier fell from 0.0618 to 0.0578: a modest 0.0040 reduction in squared probability error. An intercept correction, with calibration slope fixed at 1, checks average bias. The ideal correction is zero. The estimate 0.020 and interval spanning zero do not prove perfect agreement. Slope 0.836 suggests predictions may be too extreme, but its 0.591–1.133 interval includes the ideal 1 [19]. Only 67 events informed these checks [21]. Most adults in even the highest-risk bin reported receipt.

Table II separates concepts from measured predictors. Schooling suggests learning costs; distance/settlement suggest compliance costs [12], [16]. The odds ratios describe the screened group, not OOF effects or measured burden. Lower schooling accompanied receipt, contrary to a simple information-barrier expectation. Fewer other resources or screening selection could explain this; the analysis tested neither explanation. Uncertain office/settlement associations neither confirm nor rule out compliance costs. The survey does not measure psychological costs. Without awareness, visits, document demands or administrative decisions, this analysis cannot explain non-receipt.

Table VIII separates sample, predictor and evaluation changes. S7 removed 21 people/four events (992/63). Its lower Brier concerns a different sample and cannot establish whether filling missing values is better. S8 substituted marriage for welfare access and performed similarly. S9 weighted fitting but not evaluation; it does not model the full survey design. S10 reweighted the same primary OOF predictions without retraining, raising Brier to 0.0641. S11 grouped folds by derived PSU and also performed similarly. S8–S11 retained 1,013 people/67 events. These checks expose internal assumptions; they do not establish model superiority or reliability elsewhere [22], [23].

### C. Reproducibility and usability

RQ3 has six evidence layers. Synthetic cases check rule decisions; matching file contents check repeatability; UI–CLI agreement checks software paths; JSON reload checks saved-model predictions. The owner walkthrough checks a synthetic workflow; participant testing would assess human usability. Table IX supports the first five within tested conditions. Automated agreement cannot establish independent user ease, acceptance or field success. Saved sources and run/validation reports document versions, checksums and test conditions.

The app separates historical OOF results from uploaded scores; uploads may overlap training data. Matching saved scores checks reloading, not new predictive accuracy. The software exposes its computations, but representative user clarity remains untested. The task sheet supports future testing.

### D. Transfer to other settings

This study analysed screened KwaZulu-Natal adults in LCS 2014/2015. Provinces and periods differ in settlement, services, policy and reporting. Application, award and payment records measure different events from reported receipt and can contain linking errors. The study did not test the model on an independent province, period or administrative sample. Transfer requires comparable populations/outcomes, justified period-specific rules and independent ranking/calibration checks [22], [23]. Making the app available cannot establish suitability for today's applicants.
