# APRE402 Submission 2 — Targeted Revision Plan for a 90%+ Standard

**Working manuscript:** `Jawe_OPG_nonreceipt_KZN (1).docx`

**Study:** *Interpretable Prediction of Reported Older Person’s Grant Non-Receipt Among Apparently Eligible Adults in KwaZulu-Natal*

**Prepared:** 11 October 2026

**Final deadline:** 23 October 2026

**Constraint:** IEEE format, **maximum eight pages including references**, subject to lecturer/portal confirmation.

**Scope of this plan:** Improve the manuscript **without relying on participant usability testing** or retraining a new model. The goal of 90%+ is a target, **not a predicted grade**.

## 1. Current position and decision

The earlier attempt received **87%**. The current draft is a substantially more complete study, but there is no fresh lecturer mark for this version. The first lecturer feedback praised the rigorous methodology and requested improvements to (1) conceptual grounding, (2) documented eligibility rules, (3) separation of survey description from prediction, (4) systematic sensitivity analysis, (5) actual artefact correctness/reproducibility/usability evidence, (6) cautious causal/legal interpretation and (7) external validity.

The current manuscript addresses most of these substantively. It adds a conceptual measurement framework (Fig. 1; Table II), explicit rules (Section III.B), distinct weighted descriptive and held-out predictive analyses (Sections III.C–D), screening and modelling sensitivity tables (Tables VI and VIII), and detailed software-verification evidence (Table IX). **Independent participant usability remains untested and must stay labelled as such.**

**Primary decision:** Spend the remaining revision time on *interpretation, theory-to-results synthesis, transparent limitations and claim-to-output verification*. Do not add predictors, algorithms, or new research questions merely to increase perceived complexity.

## 2. Priorities and acceptance criteria

| Priority | Task | Manuscript location | Evidence already in paper | Finished when… |
|---|---|---|---|---|
| **P1** | Deepen discussion and direct engagement with prior studies | VI.A–D; II.A–B | Tables IV–VIII; references [1]–[15] | Each research question has a concise, evidence-linked interpretation and direct, appropriately qualified comparisons with relevant studies. |
| **P2** | Connect theoretical framework to actual findings | II.B–C; Fig. 1; Table II; VI.B | Administrative-burden theory [13]; observable proxies | The discussion distinguishes *construct*, *proxy*, *association*, and *unmeasured mechanism* without causal overclaims. |
| **P3** | Sharpen predictive interpretation | V.C; Table VII; Fig. 4; VI.B | AUC, AP, Brier, calibration, event count | Interpretation states what each metric adds and what it does **not** demonstrate. |
| **P4** | Interpret sensitivity results, rather than only list them | V.B–C; Tables VI and VIII; VI.A–B | S0–S11 outputs | The paper identifies the most consequential assumptions, separating denominator/prevalence changes from changes in model evaluation. |
| **P5** | Verify evidence, references, ethics language and submission details | Entire paper, especially title block, III, IV, V, VII and references | Source outputs, decision log, tests, cited publications | Every number and verification claim traces to a saved artefact; citations, labels, page limit and data-handling claims are checked. |

> **Important scope boundary:** This plan does not mark the lecturer’s usability recommendation “resolved.” It preserves the truthful statement that participant usability has not been evaluated. If participant testing later becomes possible, document it as a separate evidence-based addition rather than inventing results now.

---

## 3. P1 — Deepen the Discussion: from results to scholarly argument

### 3.1 Section VI.A — Denominator and grant access (RQ1)

**Currently established:** Among 1,013 screen-PASS adults with resolved receipt, 67 report non-receipt (6.61% unweighted; 7.49% person-weighted). The screen also leaves 187 adults unresolved, exceeding the 67 non-recipients. Table VI reports alternative assumptions.

**Revisions:**

1. Open with the **estimand**: non-receipt *among apparently eligible, screened, resolved respondents in the historical KZN LCS*, not a prevalence of unlawful grant denial or all legally entitled people.
2. Explain why **187 unresolved** is substantively important: exclusion from the denominator can affect interpretation even where sensitivity variants barely change point estimates.
3. Compare the *definition and measurement* of your cohort with **Ralston et al. [3]** (rural age-eligible individuals) and **Godfrey et al. [4]** (household-level grant receipt). State that percentages are **not directly comparable** because programme/unit, screen and geography differ; only make numerical comparisons after verifying the exact estimates in those articles.
4. Explain which screen decisions matter most (see P4): disability-grant compatibility produces the largest weighted prevalence shift in the reported variants; alternative partnership assumptions tend to alter the denominator more than the weighted rate.
5. Retain the important qualification that receipt can coexist with administrative burden; low observed non-receipt does **not** prove low access costs.

**Suggested paragraph architecture (not paste-ready results):** 1 sentence with RQ1 finding → 2 sentences on population definition/unresolved cases → 2 sentences on sensitivity → 2 sentences comparing the scope of previous OPG research → 1 cautious implication.

**Do not write:** “Only 7.5% of eligible pensioners in KwaZulu-Natal are excluded.” That substitutes legal entitlement and exclusion for measured research-screen status and reported receipt.

### 3.2 Section VI.B — Meaning and limits of prediction (RQ2)

**Currently established:** Household-held-out model performance: AUC **0.752** [0.687, 0.814], AP **0.203** [0.139, 0.292], Brier **0.0578** [0.0448, 0.0706] versus intercept-only **0.0618**, calibration-in-the-large **0.020**, slope **0.836** [0.591, 1.133]. There are **67 events**.

**Revisions:**

1. Treat **ranking**, **precision–recall**, **probability error** and **calibration** as four distinct questions (detailed in P3).
2. Interpret the full-fit odds ratios cautiously: female vs male **0.39** (Wald interval 0.23–0.66); schooling below Grade 7 vs higher **0.24** (0.13–0.43). These are conditional *screened-cohort* associations, not causal effects, not out-of-fold effects and not administrative-burden measures.
3. Engage with unexpected directions. Lower schooling is associated with reported **receipt** rather than the hypothesised access disadvantage within the selected cohort. Discuss plausible screening/selection or resource-composition explanations as **hypotheses**, not findings.
4. Explain why office-distance and settlement associations are imprecise and cannot resolve the presence or absence of actual compliance costs.
5. End with the appropriate research contribution: a transparent **internal prediction** benchmark rather than a deployable present-day benefit decision system.

### 3.3 Section VI.C — Artefact evaluation (RQ3)

**Currently established:** Table IX reports 26/26 original checks (including 22 synthetic screening cases), 220 automated tests passed, 15,388/15,388 native UI–CLI agreement, JSON reload score difference about 5.55 × 10⁻¹⁷, and 50/50 checks on extracted synthetic Windows walkthrough report files.

**Revisions:**

1. Distinguish clearly between **rule correctness**, **repeatability**, **software-path parity**, **inference serialization**, **owner-operated functional workflow**, and **human usability**.
2. Make explicit that automated tests and one owner walkthrough substantiate correctness/reproducibility **within their tested conditions**, not independent real-user ease or field deployment.
3. Keep the separation between historical **out-of-fold evaluation** and **frozen full-data app predictions**; frozen app outputs are not externally validated accuracy measures.
4. Describe app risk controls only if demonstrated in test evidence: synthetic sample use, session-memory uploads, schema validation, suppressed identifiers and audit exports.
5. If space allows, retain one evidence-rich sentence on where the versioned rules, hashes and validation outputs can be inspected, **without promising a public repository or link that is not available**.

**Do not write:** “User-friendly interface validated by users.” The paper explicitly says participant evaluation was not conducted.

### 3.4 Section VI.D — External validity

Retain the current differentiation among **other provinces**, **later time periods**, and **administrative systems**. Strengthen with one brief sentence specifying what transfer would require: comparable population and outcome definitions, justified target-period screen rules, and an independent test of discrimination and calibration. Avoid suggesting that software deployment itself establishes transferability.

---

## 4. P2 — Make the theory–measurement–finding connection explicit

### 4.1 Preserve and sharpen existing framework

The manuscript already includes **administrative-burden theory** (learning, compliance, psychological costs), **Fig. 1**, and **Table II** mapping five domains to measurable LCS proxies. This addresses the lecturer’s central theoretical criticism in structure. The remaining task is *analytic integration*—return to those distinctions when discussing empirical findings.

| Theoretical or conceptual category | What the manuscript actually measures | Safe inference | Not supported by these data |
|---|---|---|---|
| Observable eligibility | Age, person-income proxy, partnership/resource rules, grant compatibility | A reproducible research screen | Full statutory qualification, asset/deemed-income assessment |
| Learning costs | Schooling category as possible information-resource proxy | A predictor association within the screened cohort | Awareness of the application process or literacy level |
| Compliance costs | Welfare-office distance ≥5 km/unavailable, settlement contrasts | Geographic/service-context association | Number of visits, queue time, transport spend, document demands |
| Psychological costs | **No direct variable** | A theoretical explanation motivating future measurement | Actual stigma, stress or perceived treatment |
| Outcome | Combined reported grant/OPG receipt response | Historical reported non-receipt among PASS and resolved | Rejection, failure to apply, non-payment cause, wrongful denial |
| Prediction | Six-slope logistic model, held-out probabilities | Internal discrimination/probability assessment | Causal pathway or reliable contemporary applicant scoring |

### 4.2 Concrete edits

- In **II.C**, add or strengthen a bridge sentence: these proxies are motivated by access concepts, but none directly records the full experience of applying for OPG.
- In **VI.B**, refer back to this table/framework when discussing schooling, office distance and settlement—particularly unexpected associations.
- Keep Figure 1 labelled as a **conceptual measurement and workflow** diagram, **not a causal directed acyclic graph** with estimated effects.
- Avoid conflating screening inputs with predictors: income, partnership and grant codes define the screen, while age, sex, schooling, settlement and welfare-office distance define model feature domains.

**Acceptance test:** A reader can answer: “What social theory motivates the variables, what is observable in LCS, what did the model find, and which proposed mechanisms remain untested?”

---

## 5. P3 — Make the predictive-evaluation interpretation more precise

Use **Table VII** and **Figure 4**, without changing their numeric values unless source outputs show an error.

| Finding in current paper | Proper interpretation | Overclaim to avoid |
|---|---|---|
| ROC AUC **0.752** | Moderate discrimination among this cohort’s recipient/non-recipient pairs in household-held-out predictions | “75.2% accuracy” or transportable performance |
| Average precision **0.203** vs event prevalence **0.0661** | Precision–recall ranking is more informative than prevalence reference in an uncommon-event setting | “20.3% of flagged cases will be non-recipients” at any chosen threshold |
| Brier **0.0578** vs baseline **0.0618** | Absolute reduction ≈ **0.0040**, a modest improvement in squared probability error | “Large predictive improvement” |
| Calibration-in-the-large **0.020** with reported interval | Evaluate overall mean probability agreement using the paper's calibration convention | “Perfect calibration” |
| Calibration slope **0.836**, interval **0.591–1.133** | Possible tendency to overly extreme predictions, but interval includes 1 | Definitive evidence of poor calibration |
| Top quantile bin: **35/203** events; mean prediction **0.188** | Concentration of some events at higher predictions, though **most in that bin report receipt** | A decision threshold validated for field use |
| **67** non-receipt events | Sparse outcomes make some associations and calibration estimates uncertain | Robust high-confidence conclusions for every subgroup |

### Edits to implement

1. In **V.C**, present concise results and sample sizes; minimise interpretation there.
2. In **VI.B**, provide the interpretive explanation: AUC answers pairwise ranking; AP is more informative for event prevalence than ROC alone; Brier captures probability error; calibration assesses probability agreement.
3. Make **no threshold-based operational recommendations** unless a threshold analysis has actually been performed.
4. Preserve your model’s unweighted household-held-out basis; do not merge weighted sensitivity metrics with the unweighted primary model as if identical estimands.
5. Recheck that abstract, Section V, Discussion and Conclusion all state the **same primary results** (AUC .752, AP .203, Brier .0578), not older model-run metrics.

**Acceptance test:** An examiner cannot plausibly mistake AP for precision at a deployment cutoff, AUC for classification accuracy, or an odds ratio for a causal effect.

---

## 6. P4 — Explain sensitivity results as robustness and measurement choices

### 6.1 Screening sensitivity (Table VI)

The current manuscript contains usable comparative evidence. The narrative should identify **what changed and why that matters**:

| Scenario | Cohort/events | Weighted non-receipt | Main interpretation |
|---|---:|---:|---|
| **S0 primary** | **1,013 / 67** | **7.49%** | Reference screen |
| **S1b,d threshold alternatives** | 1,015 / 69 | 7.68% | Small shift under those threshold variants |
| **S2a: living together treated as couple** | 1,072 / 71 | 7.42% | More adults included; similar weighted proportion |
| **S2b: living together treated as single** | 1,073 / 69 | 7.17% | Partnership assumption changes denominator |
| **S2c: separated treated as single** | 1,021 / 67 | 7.43% | Small change |
| **S2d: both as single** | 1,081 / 69 | **7.12%** | Lowest reported weighted estimate |
| **S3: retain own disability/war-veterans grants** | 1,032 / 82 | **9.06%** | Largest reported shift; compatibility rule materially affects result |
| **S4b: include social-assistance income** | 1,007 / 67 | 7.55% | Small change in this variant |

**Narrative to add:** Screening assumptions are not interchangeable. The most consequential tested alternative for weighted non-receipt is grant compatibility; partnership treatments often add people without similarly large rate changes. A close AUC across scenarios does not prove equivalence of the underlying populations or correctness of screening assumptions.

### 6.2 Modelling/validation sensitivity (Table VIII)

- **S7 complete-case:** N=992/events=63; AUC .758, Brier .0556. Interpret as a different analytic sample, not necessarily proof imputation is superior/inferior.
- **S8 married indicator:** AUC .755, Brier .0578; comparison is specification sensitivity.
- **S9 person-weighted fit:** AUC .750, Brier .0583; frequency weighting in fitting is **not** a fully survey-design-adjusted model.
- **S10 weighted evaluation:** AUC .763, Brier .0641; same primary OOF predictions with different evaluation weights, **not a new trained model**.
- **S11 derived-PSU folds:** AUC .758, Brier .0575; a grouping alternative, not external validation.

### Implementation rule

For each reported scenario, explain **(a)** what assumption changed, **(b)** whether N/events changed, **(c)** what happened to weighted prevalence or performance, and **(d)** which interpretation is justified. Do not add a new sensitivity analysis unless an evidence discrepancy requires a rerun.

---

## 7. P5 — Evidence, citations, ethics and IEEE final audit

### 7.1 Build a claim-to-source register

Create a small local checklist or spreadsheet with columns:

`Paper section | Claim/number | Underlying output file and row/field | Rule/model version | Rechecked? | Notes`

At minimum independently confirm:

- **Cohort flow:** 15,388 KZN records; 1,317 aged 60+; FAIL 117; UNRESOLVED 187; PASS/resolved 1,013; recipients 946; non-recipients 67; household counts in Table IV.
- **RQ1:** 67/1,013 = 6.61%; person-weighted 7.49%; approximation based on 345 derived PSUs, SE 1.3 percentage points and approximate 95% interval 4.9%–10.0% (not a full design-based CI).
- **RQ2:** all primary metrics, confidence intervals, five household-held-out folds, fold seed, baseline and Figure 4 quantile-bin totals.
- **Sensitivities:** all S0–S11 scenario definitions, denominators, events and metrics; distinguish unchanged scenarios.
- **RQ3:** 26 original checks, 22 synthetic cases, 220 automated tests, 15,388 native UI–CLI agreement, JSON reload difference, 50 Windows report-file checks; evidence record for each.
- **Review numbers:** 511 found → 136 duplicates → 375 screened → 222 excluded → 153 full-text assessed → 98 excluded → 55 retained. Verify against the original review log; do **not** imply 55 studies specifically about OPG.

**Important:** Some prior research runs had **different** primary scores. Do not substitute them for the values in the present six-slope manuscript without verifying the exact run version and determining whether all dependent tables/claims require updating.

### 7.2 Source validation

- Open the primary studies and confirm the sentence citing each genuinely matches its **population, outcome, study design and findings**.
- Prioritise [3] Ralston et al., [4] Godfrey et al., [13] Moynihan et al., [16] Saito & Rehmsmeier, [17] Van Calster et al., [18] Riley et al., [19] Roberts et al., and the 2014–2015 government notices [24]–[25].
- Check year, authors, DOI, page range and claims. The draft's publication entries must be **verified, not treated as verified simply because they appear in the references**.
- Check references appear in first-citation order under the required IEEE style.

### 7.3 Ethics and governance

The current Section VII says **no DUT ethics determination is documented**. Confirm status with the supervisor/official records; record the exact determination or retain the truthful limitation. Do not imply approval, exemption or consent where none is documented. Check licensing/access and small-cell disclosure requirements before public release of code, data or sample output. Keep using synthetic demonstration records unless specific data-release conditions permit otherwise.

### 7.4 Document and formatting checks

- **Fix the title block:** the current file shows **PRIC401**, while the working final-submission requirement is **APRE402**. Verify the module identifier before editing.
- Confirm title, author affiliation, assignment naming, student number and date follow portal guidance.
- Stay within **eight actual PDF pages**, including references. Revise by replacement/consolidation, **not simply adding paragraphs**.
- Check Figure 1 conceptual legend; Figure 2 application/research distinction; Figure 3 cohort flow; Figure 4 calibration labels. Ensure each figure is discussed in text and readable at actual-size print.
- Check Tables I–IX for readable cells, aligned headers, consistent decimal places, correct footnotes, non-overflow and correct cross-references.
- Verify no text, lines or labels overflow table boundaries and all references are legible in two columns.
- Run a final read-through specifically for inconsistent phrases: **apparently eligible**, **reported non-receipt**, **research screen**, **household-held-out**, **unweighted vs person-weighted**, **internal validation**, **historical LCS**.

---

## 8. Practical revision order (11–22 October)

| Dates | Work | Concrete deliverable |
|---|---|---|
| **11–13 Oct** | Rewrite VI.A and VI.B with direct literature comparison, denominator/screen analysis, and nuanced model interpretation. | Clearer RQ1/RQ2 Discussion paragraphs without new numeric claims. |
| **14–15 Oct** | Reconnect II.C/Table II/Fig. 1 to VI.B; refine V.B/VI.A sensitivity interpretation. | Consistent theoretical and robustness argument. |
| **16–17 Oct** | Refine VI.C–D and conclusion; preserve explicit usability and transport limits. | All three RQs accurately answered and bounded. |
| **18–20 Oct** | Verify claims with saved outputs and original source documents; confirm ethics/disclosure status; proof references. | Completed claim-to-source register and corrected bibliography. |
| **21–22 Oct** | Export actual IEEE PDF; inspect each of eight pages; check module code, captions, tables, headings, final metrics and portal requirements. | Submission-ready PDF and reproducibility evidence pack. |
| **23 Oct** | Submit before the confirmed portal cutoff. | Submission confirmation. |

## 9. Suggested word/page-space strategy

Because the current manuscript already runs to eight pages:

- **Replace** repetitive statements of limitations with one deeper explanatory sentence linked to a result.
- Prefer **two or three direct literature comparisons** over a longer generic literature summary.
- Use existing **Tables VI–VIII** rather than adding graphs whose insight duplicates the tables.
- Keep the **existing main figures** if legible; fix captions and interpretation before redesigning visuals.
- If more discussion space is needed, shorten duplicated Methods or repeated uncertainty disclaimers—**never remove essential screen rules or validation details**.
- Preserve references to the original sources supporting all claims. Never force compliance by shrinking IEEE fonts below required settings.

## 10. Final pass/fail checklist

- [ ] RQ1 explains **which population** the 7.49% refers to and what unresolved records mean.
- [ ] RQ1 compares the study cautiously with at least two relevant previous studies using correctly verified source claims.
- [ ] RQ2 explains **AUC vs AP vs Brier vs calibration** and the significance of **67 events**.
- [ ] RQ2 distinguishes proxies from theory and interpretation from causation.
- [ ] RQ2 does not portray odds ratios from the full fit as out-of-fold or causal evidence.
- [ ] Sensitivity discussion prioritises **S3's 9.06% vs S0's 7.49%** and correctly characterises S2, S7–S11.
- [ ] RQ3 reports actual tests, and clearly says **participant usability remains untested**.
- [ ] App's frozen full-data scores are **never confused** with OOF validation performance.
- [ ] External validity explicitly excludes unsupported 2026 or cross-province operational claims.
- [ ] Every headline figure is traceable to a saved output and correct run version.
- [ ] References and historical legal thresholds have been checked against originals.
- [ ] Ethics/access/disclosure claims are accurate and documented.
- [ ] Correct module code and final-assignment labels appear.
- [ ] Eight-page IEEE PDF has been visually checked at normal reading size.

## 11. Definition of completion

This revision is complete when **the paper's empirical claims are all verifiable, each RQ is answered with interpretation anchored in evidence, theory and measurement remain conceptually distinct, sensitivity results are explained rather than merely displayed, and the final format complies with the eight-page requirement**.

This work can strengthen the submission substantially. **No responsible review can guarantee a 90%+ grade without the final rubric and lecturer assessment.**
