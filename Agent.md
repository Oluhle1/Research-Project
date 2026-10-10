I am completing Submission 2 of my ICT Honours research project. Submission 1 has already been submitted and must be treated as the approved baseline/specification for the study.
Submission 2 requirements
- Format: IEEE conference paper
- Maximum length: 8 pages
- Content: complete research paper, including Results and Discussion
- Weight: 60% of the final module mark
My submitted Submission 1 is attached. Read it carefully before proposing or implementing anything. Do not redesign the research project unnecessarily. Preserve the established aim, research questions, terminology, study population, outcome definition and methodological logic unless the empirical data makes part of the proposed methodology impossible. If a change becomes necessary, explain and document it rather than silently changing the methodology.
The study investigates reported Older Person's Grant (OPG) non-receipt among apparently eligible adults aged 60+ in KwaZulu-Natal using Statistics South Africa's Living Conditions Survey 2014/2015.
The project is not intended to determine official legal eligibility or make grant decisions. "Apparently eligible" must retain the definition established in Submission 1: people who satisfy eligibility conditions observable in the survey.
Main objective for Submission 2
Move the research from proposed methodology to completed empirical study.
The work must answer the three existing research questions:
RQ1: What proportion of the study population reports OPG non-receipt, and how does this estimate change under alternative eligibility assumptions?
RQ2: How well does a small logistic regression model distinguish recipients from non-recipients and estimate non-receipt probabilities in held-out households?
RQ3: Can the proposed computational artefact reproduce the analysis and clearly explain screening decisions and model outputs?
Do not begin by rewriting the paper. First complete and validate the research work. The paper should be written around verified outputs from the analysis.
PHASE 1 — Audit Submission 1 and create an implementation specification
Extract from Submission 1:
- aim;
- RQ1–RQ3;
- study population;
- unit of analysis;
- eligibility rules;
- definition of "apparently eligible";
- OPG receipt/non-receipt outcome definition;
- treatment of unresolved observations;
- proposed predictors;
- survey weighting;
- logistic-regression specification;
- household-grouped cross-validation;
- evaluation metrics;
- sensitivity analyses;
- artefact requirements;
- artefact evaluation;
- limitations;
- MVP versus secondary components.
Turn these into a checklist with three statuses: Proposed / Implemented / Verified.
Do not add methodological components simply because they are common in machine-learning projects. Every major analytical step should trace back to the submitted methodology or be explicitly documented as a justified revision.
PHASE 2 — Dataset audit and reproducible data pipeline
Before modelling, inspect the actual LCS files and documentation.
Establish:
- which file contains each required variable;
- household identifier;
- person identifier;
- age;
- sex;
- marital/partner information;
- spouse identifier if available;
- schooling;
- settlement/geographic variables;
- OPG receipt variables;
- general social-grant receipt variables;
- income variables;
- social-assistance income;
- survey person weights;
- strata/PSU variables if available;
- welfare-office/access variables if available.
Create a variable mapping/data dictionary showing:
Research concept → LCS file → variable → coding → transformation → purpose
Verify joins before proceeding. Report duplicate keys, unmatched records, missing values, unexpected row-count changes and any variables proposed in Submission 1 that cannot actually be constructed from the available data.
Do not silently substitute variables.
PHASE 3 — Construct the study cohort
Implement the cohort construction proposed in Submission 1.
Start with KZN respondents aged 60+ and sequentially apply the observable eligibility rules.
Every person must ultimately have a documented screening status such as:
PASS / FAIL / UNRESOLVED
and a reason code explaining the decision.
Specifically investigate:
- age;
- applicant resources;
- spouse/partner resources where applicable;
- income thresholds appropriate to the LCS period;
- incompatible grants;
- missing income;
- missing/non-resident spouse information;
- contradictory grant responses;
- unresolved receipt;
- disagreement between current reported receipt and historical OPG income.
Produce a cohort-flow table showing:
KZN sample → age 60+ → eligibility screening → fails → unresolved → passes → resolved OPG outcome → recipients → non-recipients → final analysis cohort
Record both people and households where appropriate.
This cohort must be frozen and validated before predictive modelling begins.
PHASE 4 — RQ1: Descriptive analysis
Calculate the observed extent of OPG non-receipt among the apparently eligible population.
Report:
- total analysis population;
- recipient count;
- non-recipient count;
- unweighted non-receipt proportion;
- survey-weighted non-receipt proportion;
- unresolved cases;
- relevant uncertainty estimates where supported by the survey design.
Describe recipients and non-recipients using the variables established in Submission 1.
Do not treat descriptive differences as causal relationships.
Then perform the planned eligibility sensitivity analyses.
Each scenario must report:
- eligibility rule changed;
- resulting cohort size;
- recipients;
- non-recipients;
- non-receipt rate;
- weighted estimate where applicable;
- change relative to the primary specification.
Use these results to answer RQ1 directly.
PHASE 5 — RQ2: Predictive modelling
Implement the proposed parsimonious logistic-regression model.
Begin with the predictor specification from Submission 1 rather than automatically performing feature selection.
Check:
- sample size;
- number of non-receipt events;
- category frequencies;
- missingness;
- multicollinearity where relevant;
- separation;
- convergence;
- support for the proposed number of model parameters.
If the data cannot support the proposed model, simplify it transparently and document why.
Prevent outcome leakage. Variables directly identifying OPG receipt or derived from the outcome must not become predictors.
Implement the proposed five-fold stratified household-grouped cross-validation, ensuring members of the same household never appear in both training and validation portions of a fold.
Any fitted preprocessing or imputation must be learned from training data only.
Generate held-out predictions for every eligible observation.
Evaluate using the metrics proposed in Submission 1, including where feasible:
- non-receipt prevalence;
- Average Precision;
- ROC AUC;
- Brier score;
- calibration-in-the-large;
- calibration slope;
- calibration plot;
- intercept-only reference model.
Use household-level resampling for uncertainty estimates where feasible.
Interpret predictive performance conservatively. Do not turn associations into explanations of why a person did not receive OPG.
Use these findings to answer RQ2 directly.
PHASE 6 — Sensitivity analysis
Run the sensitivity analyses committed to in Submission 1 where the data permits them.
Examine changes involving:
- income threshold assumptions;
- partner-resource treatment;
- grant compatibility;
- income definitions;
- current receipt versus historical OPG income;
- predictor missingness/complete cases;
- alternative predictor specification where justified;
- survey-weighted modelling where feasible.
Keep sensitivity results clearly separate from the primary analysis.
The exploratory random forest is secondary. Only implement it after the logistic model, validation, sensitivity analysis and artefact evaluation are complete and only if sample size supports it.
PHASE 7 — Build the computational artefact
Implement the MVP defined in Submission 1.
The core artefact must contain:
Raw/released LCS data → validation/linkage → eligibility rule engine → screened cohort → descriptive analysis → predictive analysis → reproducible outputs
The rule engine must record both the decision and reason for screening decisions.
Preserve:
- rule/configuration version;
- variable mappings;
- random seed;
- validation folds;
- model specification;
- output files;
- execution/run information necessary for reproducibility.
Build the research workflow so another researcher can rerun the analysis from the documented inputs.
Do not prioritise Streamlit over the research pipeline. Streamlit is secondary and should only be developed after the core analytical artefact is working.
PHASE 8 — RQ3: Evaluate the artefact
Do not merely demonstrate that the program runs.
Evaluate:
Correctness: Create synthetic test cases for important screening conditions, including income boundaries, missing partner resources, incompatible grants, unresolved receipt and caregiver-linked grants. Compare expected versus actual decisions.
Data integrity: Verify that joins preserve the intended person-level unit and that cohort counts remain traceable.
Leakage prevention: Confirm that receipt/outcome variables cannot enter predictor preparation.
Reproducibility: Run the same configuration repeatedly and verify identical cohort membership, screening reasons, validation partitions and numerical outputs within appropriate tolerance.
Transparency: Demonstrate that screening decisions, active rule versions and model outputs can be inspected and interpreted.
Record pass/fail results for these tests.
Use this evidence to answer RQ3 directly.
PHASE 9 — Results
Only after the analysis is complete, construct the Results section.
Results should present evidence rather than repeat methodology.
Prioritise approximately:
1. cohort construction;
2. descriptive OPG non-receipt findings;
3. sensitivity of the estimate to eligibility assumptions;
4. logistic-model performance;
5. calibration/performance figures;
6. artefact evaluation results.
Every table and figure must have a research purpose and contribute to RQ1, RQ2 or RQ3.
Do not overload the eight-page paper with diagnostic outputs that can instead be retained in the project repository.
PHASE 10 — Discussion
Build the Discussion around the research questions rather than simply repeating numerical results.
For RQ1, discuss what was learned about reported OPG non-receipt and how strongly the estimate depends on observable eligibility assumptions.
For RQ2, discuss whether the proposed characteristics contain useful predictive information, what calibration/discrimination show, and what the model cannot establish.
For RQ3, discuss whether the artefact successfully makes cohort construction and analysis reproducible and transparent.
Compare the empirical findings with the literature already used in Submission 1. Only add new literature where a result genuinely requires additional interpretation or where the existing review has a clear OPG-specific gap.
Explicitly discuss unexpected or weak results rather than trying to make the project appear more successful.
PHASE 11 — Final IEEE paper
Transform Submission 1 into the final eight-page paper rather than writing an unrelated paper from scratch.
Target structure:
Abstract
I. Introduction
II. Related Work / Literature Review
III. Methods
IV. Computational Artefact
V. Results
VI. Discussion
VII. Limitations and Ethics
VIII. Conclusion
References
Compress the Submission 1 literature review and proposed-method sections to make room for Results and Discussion.
Replace future tense such as "will be analysed" with completed-study language only when that work has actually been performed.
Do not fabricate results to complete the manuscript.
Keep a traceability matrix:
Research Question → Method → Evidence/Output → Result → Discussion → Conclusion
Before finalising the paper, verify that every RQ has a direct evidence-based answer.
Working rules
Work sequentially. Do not jump ahead to writing Results before the analysis producing those results has been completed.
At the end of every phase, provide:
Completed: what we actually accomplished.
Evidence: files, tables, tests or outputs demonstrating completion.
Problems: data or methodological problems discovered.
Decisions: methodological decisions made and why.
Next step: the exact next task.
Maintain a running research decision log so deviations from Submission 1 are documented.
When writing code, explain what the code is doing and organise it into a reproducible project structure rather than relying on invisible notebook state or temporary code.
Our priority order is:
valid research → reproducible implementation → verified results → interpretation → final paper → optional interface improvements.
Start with Phase 1 only. Read Submission 1 and produce the implementation specification and checklist. Do not begin modelling or rewrite the paper yet.